#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

from pathlib import Path
import os
from PIL import Image
import torch
import torchvision.transforms.functional as tf
from utils.loss_utils import ssim
from evaluation.lpipsPyTorch import lpips
import json
from tqdm import tqdm
from utils.image_utils import psnr

def readImages(renders_dir, gt_dir):
    renders = []
    gts = []
    image_names = []
    for fname in os.listdir(renders_dir):
        render = Image.open(renders_dir + "/" + fname)
        gt = Image.open(gt_dir + "/" + fname)
        renders.append(tf.to_tensor(render).unsqueeze(0)[:, :3, :, :].cuda())
        gts.append(tf.to_tensor(gt).unsqueeze(0)[:, :3, :, :].cuda())
        image_names.append(fname)
    return renders, gts, image_names

def readImage(renders_dir, gt_dir, idx, method="vr"):
    if(method == "vr"):
        render = Image.open(renders_dir + "/frame" + str(idx).zfill(6) + ".jpg")
    elif(method == "niceslam" or method == "imap"):
        render = Image.open(renders_dir + "/rgb_" + str(idx).zfill(6) + ".png")
    gt = Image.open(gt_dir + "/frame" + str(idx).zfill(6) + ".jpg")
    render = tf.to_tensor(render).unsqueeze(0)[:, :3, :, :].cuda()
    gt = tf.to_tensor(gt).unsqueeze(0)[:, :3, :, :].cuda()
    image_name = "frame" + str(idx).zfill(6) + ".jpg"
    return render, gt, image_name

def evaluate(model_paths, save_dir, scene="all", dataset="replica"):

    full_dict = {}
    per_view_dict = {}
    full_dict_polytopeonly = {}
    per_view_dict_polytopeonly = {}

    for scene_dir in model_paths:
        print("Scene:", scene_dir)
        full_dict[scene_dir] = {}
        per_view_dict[scene_dir] = {}
        full_dict_polytopeonly[scene_dir] = {}
        per_view_dict_polytopeonly[scene_dir] = {}

        for method in os.listdir(scene_dir):
            if(scene == "all"):
                pass
            else:
                if(method != scene):
                    continue
            print("Method:", method)
            if(method[-4:] == ".ply"): continue
            full_dict[scene_dir][method] = {}
            per_view_dict[scene_dir][method] = {}
            full_dict_polytopeonly[scene_dir][method] = {}
            per_view_dict_polytopeonly[scene_dir][method] = {}
            method_dir = scene_dir + "/" + method
            gt_dir = method_dir + "/results"
            if(dataset == "tum"):
                gt_dir = gt_dir + "/gt/"

            if(not os.path.exists(gt_dir) or not os.path.exists(save_dir)):
                print("Skipping method", method, "as it does not have the required directories.")
                continue
            # renders, gts, image_names = readImages(renders_dir, gt_dir)

            ssims = []
            psnrs = []
            lpipss = []
            image_names = []

            image_files = [f for f in os.listdir(save_dir) if f.startswith("frame") or f.startswith("rgb_")]
            for idx in tqdm(range(len(image_files)), desc="Metric evaluation progress"):
                render, gt, image_name = readImage(save_dir, gt_dir, idx)
                ssims.append(ssim(render, gt)[1])
                psnrs.append(psnr(render, gt))
                lpipss.append(lpips(render, gt, net_type='vgg'))
                image_names.append(image_name)

            print("  SSIM : {:>12.7f}".format(torch.tensor(ssims).mean(), ".5"))
            print("  PSNR : {:>12.7f}".format(torch.tensor(psnrs).mean(), ".5"))
            print("  LPIPS: {:>12.7f}".format(torch.tensor(lpipss).mean(), ".5"))
            print("")

            full_dict[scene_dir][method].update({"SSIM": torch.tensor(ssims).mean().item(),
                                                    "PSNR": torch.tensor(psnrs).mean().item(),
                                                    "LPIPS": torch.tensor(lpipss).mean().item()})
            per_view_dict[scene_dir][method].update({"SSIM": {name: ssim for ssim, name in zip(torch.tensor(ssims).tolist(), image_names)},
                                                        "PSNR": {name: psnr for psnr, name in zip(torch.tensor(psnrs).tolist(), image_names)},
                                                        "LPIPS": {name: lp for lp, name in zip(torch.tensor(lpipss).tolist(), image_names)}})

        with open(scene_dir + "/results.json", 'w') as fp:
            json.dump(full_dict[scene_dir], fp, indent=True)
        with open(scene_dir + "/per_view.json", 'w') as fp:
            json.dump(per_view_dict[scene_dir], fp, indent=True)
