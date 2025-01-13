<div align=center>

# Memory Efficient Voxel-Based 3D Gaussian Splatting Map for Visual Localization

[Howoong Jun](https://howoongjun.github.io/), [Seongbo Ha](https://riboha.github.io/), [Hyeonwoo Yu](https://bogus2000.github.io/), and [Songhwai Oh](https://rllab.snu.ac.kr/people/songhwai-oh)

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

## Run

You can try rendering with sample data using demo notebook.
Additionally, you can review the evaluation results on image quality metrics, including PSNR, LPIPS, and SSIM.

- [[Demo] Rendering.ipynb](%5BDemo%5D%20Rendering.ipynb)

## BibTex

```bash
@InProceedings{jun2025vrmap,
    author  = {Jun, Howoong and Ha, Seongbo and Yu, Hyeonwoo and Oh, Songhwai},
    title   = {Memory Efficient Voxel-Based 3D Gaussian Splatting Map for Visual Localization},
    year    = {2025}
}
```