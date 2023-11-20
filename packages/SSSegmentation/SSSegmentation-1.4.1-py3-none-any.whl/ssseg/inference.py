'''
Function:
    Implementation of Inferencer
Author:
    Zhenchao Jin
'''
import os
import cv2
import copy
import torch
import warnings
import argparse
import numpy as np
import torch.nn.functional as F
from tqdm import tqdm
from configs import BuildConfig
from modules import (
    BuildDataset, BuildSegmentor, Logger, touchdir, loadckpts
)
warnings.filterwarnings('ignore')


'''parse arguments in command line'''
def parsecmdargs():
    parser = argparse.ArgumentParser(description='SSSegmentation is an open source supervised semantic segmentation toolbox based on PyTorch')
    parser.add_argument('--imagedir', dest='imagedir', help='image directory, which means we let the segmentor inference on the images existed in the given image directory', type=str)
    parser.add_argument('--imagepath', dest='imagepath', help='image path, which means we let the segmentor inference on the given image', type=str)
    parser.add_argument('--outputdir', dest='outputdir', help='directory to save output image(s)', type=str, default='inference_outputs')
    parser.add_argument('--cfgfilepath', dest='cfgfilepath', help='config file path you want to use', type=str, required=True)
    parser.add_argument('--ckptspath', dest='ckptspath', help='checkpoints you want to resume from', type=str, required=True)
    args = parser.parse_args()
    return args


'''Inferencer'''
class Inferencer():
    def __init__(self):
        self.cmd_args = parsecmdargs()
        self.cfg, self.cfg_file_path = BuildConfig(self.cmd_args.cfgfilepath)
        assert self.cmd_args.imagepath or self.cmd_args.imagedir, 'imagepath or imagedir should be specified'
        # open full fp32
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
    '''start'''
    def start(self):
        cmd_args, cfg, cfg_file_path = self.cmd_args, self.cfg, self.cfg_file_path
        # touch work dir and output dir
        touchdir(cfg.SEGMENTOR_CFG['work_dir'])
        touchdir(cmd_args.outputdir)
        # cuda detect
        use_cuda = torch.cuda.is_available()
        # initialize logger_handle
        logger_handle = Logger(cfg.SEGMENTOR_CFG['logfilepath'])
        # build segmentor
        cfg.SEGMENTOR_CFG['backbone']['pretrained'] = False
        segmentor = BuildSegmentor(segmentor_cfg=cfg.SEGMENTOR_CFG, mode='TEST')
        if use_cuda: segmentor = segmentor.cuda()
        # build dataset
        cfg.SEGMENTOR_CFG['dataset']['evalmode'] = 'server'
        dataset = BuildDataset(mode='TEST', logger_handle=logger_handle, dataset_cfg=cfg.SEGMENTOR_CFG['dataset'])
        # build palette
        palette = dataset.palette
        # load ckpts
        cmd_args.local_rank = 0
        ckpts = loadckpts(cmd_args.ckptspath)
        try:
            segmentor.load_state_dict(ckpts['model'])
        except Exception as e:
            logger_handle.warning(str(e) + '\n' + 'Try to load ckpts by using strict=False')
            segmentor.load_state_dict(ckpts['model'], strict=False)
        # set eval
        segmentor.eval()
        # start to test
        inference_cfg = copy.deepcopy(cfg.SEGMENTOR_CFG['inference'])
        FloatTensor = torch.cuda.FloatTensor if use_cuda else torch.FloatTensor
        if not cmd_args.imagedir:
            imagepaths = [cmd_args.imagepath]
        else:
            imagenames = os.listdir(cmd_args.imagedir)
            imagepaths = [os.path.join(cmd_args.imagedir, name) for name in imagenames]
        pbar = tqdm(range(len(imagepaths)))
        for idx in pbar:
            imagepath = imagepaths[idx]
            if imagepath.split('.')[-1] not in ['jpg', 'jpeg', 'png']: 
                continue
            pbar.set_description('Processing %s' % imagepath)
            infer_tricks = inference_cfg['tricks']
            cascade_cfg = infer_tricks.get('cascade', {'key_for_pre_output': 'memory_gather_logits', 'times': 1, 'forward_default_args': None})
            sample_meta = dataset.read(imagepath)
            image = sample_meta['image']
            sample_meta = dataset.synctransforms(sample_meta)
            image_tensor = sample_meta['image'].unsqueeze(0).type(FloatTensor)
            for idx in range(cascade_cfg['times']):
                forward_args = None
                if idx > 0: 
                    output_list = [
                        F.interpolate(outputs, size=output_list[-1].shape[2:], mode='bilinear', align_corners=segmentor.align_corners) for outputs in output_list
                    ]
                    forward_args = {cascade_cfg['key_for_pre_output']: sum(output_list) / len(output_list)}
                    if cascade_cfg['forward_default_args'] is not None: 
                        forward_args.update(cascade_cfg['forward_default_args'])
                output_list = self.auginference(
                    segmentor=segmentor,
                    images=image_tensor,
                    inference_cfg=inference_cfg,
                    num_classes=cfg.SEGMENTOR_CFG['num_classes'],
                    FloatTensor=FloatTensor,
                    align_corners=segmentor.align_corners,
                    forward_args=forward_args,
                )
            output_list = [
                F.interpolate(output, size=(sample_meta['height'], sample_meta['width']), mode='bilinear', align_corners=segmentor.align_corners) for output in output_list
            ]
            output = sum(output_list) / len(output_list)
            pred = (torch.argmax(output[0], dim=0)).cpu().numpy().astype(np.int32)
            mask = np.zeros((pred.shape[0], pred.shape[1], 3), dtype=np.uint8)
            for clsid, color in enumerate(palette):
                mask[pred == clsid, :] = np.array(color)[::-1]
            image = image * 0.5 + mask * 0.5
            image = image.astype(np.uint8)
            if cmd_args.outputdir:
                cv2.imwrite(os.path.join(cmd_args.outputdir, imagepath.split('/')[-1].split('.')[0] + '.png'), image)
            else:
                cv2.imwrite(os.path.join(cfg.SEGMENTOR_CFG['work_dir'], imagepath.split('/')[-1].split('.')[0] + '.png'), image)
    '''inference with augmentations'''
    def auginference(self, segmentor, images, inference_cfg, num_classes, FloatTensor, align_corners, forward_args=None):
        infer_tricks, outputs_list = inference_cfg['tricks'], []
        for scale_factor in infer_tricks['multiscale']:
            images_scale = F.interpolate(images, scale_factor=scale_factor, mode='bilinear', align_corners=align_corners)
            outputs = self.inference(
                segmentor=segmentor, 
                images=images_scale.type(FloatTensor), 
                inference_cfg=inference_cfg, 
                num_classes=num_classes, 
                forward_args=forward_args,
            ).cpu()
            outputs_list.append(outputs)
            if infer_tricks['flip']:
                images_flip = torch.from_numpy(np.flip(images_scale.cpu().numpy(), axis=3).copy())
                outputs_flip = self.inference(
                    segmentor=segmentor, 
                    images=images_flip.type(FloatTensor), 
                    inference_cfg=inference_cfg, 
                    num_classes=num_classes, 
                    forward_args=forward_args,
                )
                fixed_seg_target_pairs = inference_cfg.get('fixed_seg_target_pairs', None)
                if fixed_seg_target_pairs is None:
                    for data_pipeline in self.cfg.SEGMENTOR_CFG['dataset']['train']['data_pipelines']:
                        if 'RandomFlip' in data_pipeline: 
                            fixed_seg_target_pairs = data_pipeline[-1].get('fixed_seg_target_pairs', None)
                if fixed_seg_target_pairs is not None:
                    outputs_flip_clone = outputs_flip.data.clone()
                    for (pair_a, pair_b) in fixed_seg_target_pairs:
                        outputs_flip[:, pair_a, :, :] = outputs_flip_clone[:, pair_b, :, :]
                        outputs_flip[:, pair_b, :, :] = outputs_flip_clone[:, pair_a, :, :]
                outputs_flip = torch.from_numpy(np.flip(outputs_flip.cpu().numpy(), axis=3).copy()).type_as(outputs)
                outputs_list.append(outputs_flip)
        return outputs_list
    '''inference'''
    def inference(self, segmentor, images, inference_cfg, num_classes, forward_args=None):
        assert inference_cfg['mode'] in ['whole', 'slide']
        use_probs_before_resize = inference_cfg['tricks']['use_probs_before_resize']
        if inference_cfg['mode'] == 'whole':
            if forward_args is None:
                outputs = segmentor(images)
            else:
                outputs = segmentor(images, **forward_args)
            if use_probs_before_resize: 
                outputs = F.softmax(outputs, dim=1)
        else:
            align_corners = segmentor.align_corners
            opts = inference_cfg['opts']
            stride_h, stride_w = opts['stride']
            cropsize_h, cropsize_w = opts['cropsize']
            batch_size, _, image_h, image_w = images.size()
            num_grids_h = max(image_h - cropsize_h + stride_h - 1, 0) // stride_h + 1
            num_grids_w = max(image_w - cropsize_w + stride_w - 1, 0) // stride_w + 1
            outputs = images.new_zeros((batch_size, num_classes, image_h, image_w))
            count_mat = images.new_zeros((batch_size, 1, image_h, image_w))
            for h_idx in range(num_grids_h):
                for w_idx in range(num_grids_w):
                    x1, y1 = w_idx * stride_w, h_idx * stride_h
                    x2, y2 = min(x1 + cropsize_w, image_w), min(y1 + cropsize_h, image_h)
                    x1, y1 = max(x2 - cropsize_w, 0), max(y2 - cropsize_h, 0)
                    crop_images = images[:, :, y1:y2, x1:x2]
                    if forward_args is None:
                        outputs_crop = segmentor(crop_images)
                    else:
                        outputs_crop = segmentor(crop_images, **forward_args)
                    outputs_crop = F.interpolate(outputs_crop, size=crop_images.size()[2:], mode='bilinear', align_corners=align_corners)
                    if use_probs_before_resize: 
                        outputs_crop = F.softmax(outputs_crop, dim=1)
                    outputs += F.pad(outputs_crop, (int(x1), int(outputs.shape[3] - x2), int(y1), int(outputs.shape[2] - y2)))
                    count_mat[:, :, y1:y2, x1:x2] += 1
            assert (count_mat == 0).sum() == 0
            outputs = outputs / count_mat
        return outputs


'''debug'''
if __name__ == '__main__':
    with torch.no_grad():
        client = Inferencer()
        client.start()