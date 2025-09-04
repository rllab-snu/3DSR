<div align=center>

# Memory Efficient Voxelized Renderable Neural 3D Spatial Representation for Vision-Based Robotics

[Howoong Jun](https://howoongjun.github.io/), [Seongbo Ha](https://riboha.github.io/), [Jaewon Lee](https://rllab.snu.ac.kr/people/jaewon-lee/jaewon-lee), [Hyeonwoo Yu](https://bogus2000.github.io/), and [Songhwai Oh](https://rllab.snu.ac.kr/people/songhwai-oh)

</div>

## Environments

We provide docker repository for this work. 

```bash
docker pull howoongjun/3dgs:habitat
```

## Datasets
- Replica

    - Download
    ```bash
    bash download_replica.sh
    ```

    - Folder structure
    ```bash
    Replica
        - office0
            - results (contain rgbd images)
                - frame000000.jpg
                - depth000000.jpg
                ...
            traj.txt
        ...
    ```

- TUM

    - Download
    ```bash
    bash download_tum.sh
    ```

- HM3D

    - The sample data for HM3D will be uploaded soon

## Prerequisites

Before running the code, please [download the checkpoint](https://drive.google.com/drive/folders/1R3NPaD1-Mu-WvbaE8aQbcifBN1CWzzgR?usp=sharing) for the upsampling network and save it in the ```super_resolution/checkpoints``` folder. 
 The link provides checkpoints for the Replica and TUM datasets.

- Folder structure
```bash
3dsr
    - super_resolution
        - checkpoints
            - checkpoint_srresnet_voxel_x4_office0_300x170.pth.tar
            - checkpoint_srresnet_voxel_x4_office1_300x170.pth.tar
            ...

```

## Run

You can try rendering with sample data using demo notebook.
Additionally, you can review the evaluation results on image quality metrics, including PSNR, LPIPS, and SSIM.

- [[Demo] Rendering.ipynb](%5BDemo%5D%20Rendering.ipynb)

## BibTex

```bash
@InProceedings{jun20253dsr,
    author  = {Jun, Howoong and Ha, Seongbo and Yu, Hyeonwoo and Oh, Songhwai},
    title   = {Memory Efficient Voxelized Renderable Neural 3D Spatial Representation for Vision-Based Robotics},
    year    = {2025}
}
```
