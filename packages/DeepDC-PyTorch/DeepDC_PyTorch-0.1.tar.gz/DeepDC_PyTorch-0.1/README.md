# DeepDC: Deep Distance Correlation as a Perceptual Image Quality Evaluator

This is the repository of paper [DeepDC: Deep Distance Correlation as a Perceptual Image Quality Evaluator](https://arxiv.org/abs/***).


### Highlights:

* A novel FR-IQA model that fully utilizes the *texture-sensitiv*e of pre-trained DNN features, which computes **distance correlation** in the deep feature domain 
* The model is **exclusively** based on the features of the pre-trained DNNs and does not rely on fine-tuning with MOSs
* Extensive experiments achieve superior performance on five standard IQA datasets, one perceptual similarity dataset, two texture similarity datasets, and one geometric transformation dataset.
* It can be employed as an objective function in texture synthesis and neural style transfer
   



### ====== Pytorch Implementation ======
**Installation:** 
- ```pip install DeepDC```

### Requirements: 
- Python >= 3.6
- PyTorch >= 1.0

**Usage:** 
```python
from DeepDC_PyTorch import DeepDC
model = DeepDC()
# calculate DeepDC between X, Y (a batch of RGB images, data range: 0~1) 
deepdc_score = model(X, Y)
```
or

```bash
git clone https://github.com/h4nwei/DeepDC
python DeepDC.py --ref <ref_path> --dist <dist_path>
```


## Reference

- R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang, “The unreasonable effectiveness of deep features as a perceptual metric,” in *IEEE Conference on Computer Vision and Pattern Recognition*, 2018, pp. 586–595.
- K. Ding, K. Ma, S. Wang, and E. P. Simoncelli, “Image quality assessment: Unifying structure and texture similarity,” *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 44, no. 5, pp. 2567–2581, 2020.
- I. Kligvasser, T. Shaham, Y. Bahat, and T. Michaeli, “Deep selfdissimilarities as powerful visual fingerprints,” in *Neural Information Processing Systems*, 2021, pp. 3939–3951.

## Citation
```bibtex
@inproceedings{fang2020cvpr,
title={Perceptual Quality Assessment of Smartphone Photography},
author={Fang, Yuming and Zhu, Hanwei and Zeng, Yan and Ma, Kede and Wang, Zhou},
booktitle={IEEE Conference on Computer Vision and Pattern Recognition},
pages={3677-3686},
year={2020}
}
