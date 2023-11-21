**DeepTalk**

**Deciphering cell-cell communication from spatially resolved transcriptomic data at single-cell resolution with subgraph-based attentional graph neural network**

![Fig1-3](D:\Desktop\SPA\Fig1\Fig1-3.png)

Recent advancements in spatial transcriptomics (ST) and single-cell RNA sequencing (scRNA-seq) have revolutionized the study of cell-cell communication (CCC) dynamics in tissue homeostasis, development, and disease mechanisms. However, deciphering spatially resolved CCC at the single-cell resolution remains a significant challenge, impeding the comprehensive understanding of intercellular dynamics and biochemical processes. Here, we present DeepTalk, a novel deep learning model that harnesses cell-specific gene expression data and spatial distances to predict spatially resolved CCC at the single-cell resolution. DeepTalk utilizes attentional graph neural network (AGNN) to efficiently integrate scRNA-seq and ST data, enabling the identification of spatial cell types. Additionally, leveraging subgraph-based AGNN, DeepTalk achieves outstanding accuracy in predicting spatial CCC at the single-cell resolution. Extensive evaluations using diverse publicly available datasets validate the exceptional performance and robustness of DeepTalk in identifying spatial CCC. Furthermore, DeepTalk discovers meaningful CCC patterns between various conditions, enabling exploration of context-specific cell cooperation and signaling.

## Installation

Start by grabbing this source codes:

```
git clone https://github.com/JiangBioLab/DeepTalk.git
cd DeepTalk
```

### (Recommended) Use python virutal environment with conda（https://anaconda.org/）

```
conda create -n deeptalkEnv python=3.9.13 pip
conda activate deeptalkEnv
pip install -r requirements.txt
```

**Tutorial**

If you want to analysis your own data, the [doc/Tutorial.ipynb](https://github.com/QuKunLab/SpatialBenchmarking/blob/main/doc/Tutorial.ipynb) is an example showing how to use them to predict new spatial gene patterns and cell locations.

You also can run the jupyter notebook of `Adult_Mouse_Brain.ipynb` and VISP_MER.ipynb` to reproduce the results of figure2&4 in our paper.

For more details, please see the `SpatialGenes.py` & `Deconvolution.py` in Benchmarking directory.

## Contact

Feel free to submit an issue or contact us at [wenyiyang22@163.com](mailto:wenyiyang22@163.com) for problems about the package.