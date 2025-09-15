# AUDiT: An Open Benchmark Toolkit for Audio Deepfake Detection
AUDiT is a toolkit that allows to easily benchmark pretrained audio deepfake detection models on a wide variety of publicly available audio deepfake datasets. The current version includes 27 datasets.

## Start Benchmarking
Follow the steps below to benchmark your pre-trained deepfake detector:
### Step-1: Download datasets
We provide shell scripts to download datasets from the original source links. These scripts can be found in the `download` folder. 

Run `chmod +x download/*.sh`. Then edit the data root folder in `config.sh`, this ROOT path will be the parent folder of all evaluation data. Then either run `get_everything.sh` to download all datasets (pls check if you have enough disk space here), OR run individual `.sh` files to download the ones you need.

### Step-2: Prepare label files
Since each of these datasets have slightly different label file format, we provide interface scripts to translate them into the desired format, which are ingested by the evaluation script. These label preparation scripts can be found in the `prepare_datasets` folder.

### Step-3: Load your model and start evaluation


## Addition of new datasets
While the team will keep updating the benchmark coverage, it is highly encouraged to suggest dataset addition via creating an issue and point us to the source link and paper.  

## Disclaimer
We do not include any proprietary datasets or the ones with unknown sources for transparency. We also encourage users to be careful with the potential training/test overlap, e.g., some datasets like ASVspoof2019 / ASVspoof5 are widely used as training sets. Results obtained with this toolkit should solely be used for research purposes instead of advertisement for commercial usage.

## License
