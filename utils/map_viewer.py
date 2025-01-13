import torch
import sys
import os
import numpy as np
import cv2, copy

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from scene import GaussianModel
from gaussian_renderer import render, render_3
from scene.cameras import ViewerCam
from utils.graphics_utils import focal2fov, fov2focal

class Pipe():
    def __init__(self):
        self.convert_SHs_python = False
        self.compute_cov3D_python = False
        self.debug = False

class Map_viewer:
    def __init__(self, data_path, H, W, fx, fy, cx, cy):
        
        self.data_path = data_path
        self.gaussians = GaussianModel(0)
        self.pipe = Pipe()
        self.bg_color = [1, 1, 1]
        self.background = torch.tensor(self.bg_color, dtype=torch.float32, device="cuda")
        
        # load 3dgs map
        self.load_3dgs_map(os.path.join(data_path, "scene.ply"))
        
        # load estimated poses
        self.est_poses = self.read_est_poses(os.path.join(data_path, "est_poses.txt"))
        
        #
        self.cam = ViewerCam(0, R=self.est_poses[-1][:3,:3], t=self.est_poses[-1][:3,3],
                             FoVx=focal2fov(fx, W), FoVy=focal2fov(fy,H),
                             W=W, H=H, cx=cx, cy=cy,
                             fx=fx,fy=fy)
        self.visibility_filter = None
        
    def load_3dgs_map(self, path):
        self.gaussians.load_ply(path)
    
    def read_est_poses(self, path):
        poses = []
        with open(path, "r") as f:
            lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i]
            c2w = np.array(list(map(float, line.split()))).reshape(4, 4)
            # c2w[:3, 1] *= -1
            # c2w[:3, 2] *= -1
            # c2w = torch.from_numpy(c2w).float()
            poses.append(c2w)
        return np.array(poses)
    
    def render_img(self, pose):
        # pose: c2w
        cam_pose = np.linalg.inv(pose)
        cam_pose[:3,:3] = cam_pose[:3,:3].T
        with torch.no_grad():
            self.cam.setup_cam(cam_pose)
            render_pkg = render_3(self.cam, self.gaussians, self.pipe, self.background, training_stage=0)
            # depth_image = render_pkg["render_depth"]
            image = render_pkg["render"]
            rgb_np = image.cpu().numpy().transpose(1,2,0)
            rgb_np = np.clip(rgb_np, 0., 1.0)
            rgb_np = cv2.cvtColor(rgb_np, cv2.COLOR_BGR2RGB)
            self.visibility_filter = render_pkg['visibility_filter']
        return rgb_np
    
    def render_depth(self, pose):
        cam_pose = np.linalg.inv(pose)
        cam_pose[:3,:3] = cam_pose[:3,:3].T
        with torch.no_grad():
            self.cam.setup_cam(cam_pose)
            render_pkg = render_3(self.cam, self.gaussians, self.pipe, self.background, training_stage=0)
            depth_image = render_pkg["render_depth"]
            depth_np = depth_image.cpu().numpy().transpose(1,2,0)
        return depth_np

    def get_visibility_filter(self):
        return self.visibility_filter

    def get_gaussians(self):
        return self.gaussians