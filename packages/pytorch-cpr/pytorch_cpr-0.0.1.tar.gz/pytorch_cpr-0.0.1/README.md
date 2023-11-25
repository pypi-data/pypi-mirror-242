
# Constrained Parameter Regularization



This repository contains the PyTorch implementation for "Constrained Parameter Regularization".

Please use a system with at least 1 GPU (for the GPT2 experiments: Ampere, Ada, or Hopper and 8 GPUs)

## Install conda environment

#### If conda is not installed:
```bash
bash install_conda.sh
```

#### Install conda env:
```bash
bash setup_env.sh
```

#### Install conda env with flash attention (for Ampere, Ada, or Hopper GPUs, takes about 1h)
```bash
bash setup_env_with_flash_attn.sh
```

### Activate conda env:
```bash
conda activate pytorch-cpr
```

## Grokking Experiment

The grokking experiment should run within a few minutes. The results will be saved in the `grokking` folder.
To replicate the results in the paper, run variations with the following arguments:

####  For AdamW:
```bash
python train_grokking_task.py --optimizer adamw --weight_decay 0.1
```

####  For Adam + Rescaling:
```bash
python train_grokking_task.py --optimizer adamw --weight_decay 0.0 --rescale 0.8
```

####  For AdamCPR with L2 norm as regularization function:
```bash
python train_grokking_task.py --optimizer adamcpr --kappa_init_method dependent --kappa_init_param 0.8
```



## Image Classification Experiment
The CIFAR-100 experiment should run within 20-30 minutes. The results will be saved in the `cifar100` folder.

####  For AdamW:
```bash
python train_resnet.py --optimizer adamw --lr 0.001 --weight_decay 0.001
```

####  For Adam + Rescaling:
```bash
python train_resnet.py --optimizer adamw --lr 0.001 --weight_decay 0 --rescale_alpha 0.8
```

####  For AdamCPR with L2 norm as regularization function and kappa initialization depending on the parameter initialization:
```bash
python train_resnet.py --optimizer adamcpr --lr 0.001 --kappa_init_method dependent --kappa_init_param 0.8
```

####  For AdamCPR with L2 norm as regularization function and kappa initialization with warm start:
```bash
python train_resnet.py --optimizer adamcpr --lr 0.001 --kappa_init_method warm_start --kappa_init_param 1000
```


