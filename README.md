# AUDDT: Audio Unified Deepfake Detection Benchmark Toolkit

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/License-Research--Use--Only-blue.svg">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.8+-green.svg">
  <img alt="Paper" src="https://img.shields.io/badge/arXiv-xxxx.xxxxx-b31b1b.svg">
  <a href="https://github.com/MUSAE/AUDDT/issues">
    <img alt="Issues" src="https://img.shields.io/github/MUSAE/zhu00121/AUDDT">
  </a>
</p>

**AUDDT** is a benchmark toolkit for audio deepfake detection. The landscape of audio deepfake detection is fragmented with numerous datasets, each having its own data format and evaluation protocol. AUDDT addresses this by providing a unified platform to seamlessly benchmark pretrained models against a wide variety of public datasets. We make a dedicated effort to update it regularly to include more recent datasets. Please see below for current coverage.

The current version includes **28+ datasets**.

![AUDDT Workflow Diagram](assets/auddt_new.png)
---

## Table of Contents
- [Supported Datasets](#supported-datasets)
- [Update log](#update-log)
- [Installation](#installation)
- [Benchmarking Your Detector](#benchmarking-your-detector)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [Citation](#citation)
- [License](#license)

## Supported Datasets

The full list of 28+ supported datasets is maintained in a public Google Sheet for easy viewing and filtering.

➡️ **[View Full Dataset List on Google Sheets](https://docs.google.com/spreadsheets/d/1RVUrnBqSarKIwsHcjXvTcLxHyop7eAUzsBhvAexyR80/edit?usp=sharing)**

## Update Log
We are actively developing AUDDT. See below for the latest updates.
* **2025-09-19**
    * Birth of AUDDT
    * Added 28 datasets to the benchmark
    * Added an examplar baseline model

## Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/MUSAE/AUDDT.git](https://github.com/MUSAE/AUDDT.git)
    cd AUDDT
    ```

2.  Create a virtual environment (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Benchmarking Your Detector
Follow the steps below to benchmark your pre-trained deepfake detector.

### Step-1: Download datasets
Change root folder in `download/config.sh` to your own. This is where all the data will be downloaded and stored.

Use the following scripts for downloading dataset:
```bash
chmod +x download/*.sh
./download_XXX.sh # change XXX to dataset name
```
By default, a `data` folder will be created under `AUDDT/` with the following folder structure:
```bash
data/
  DATASET_X/
    processed/
      audio/ # audio files extracted from the compressed raw file
      manifest_X.csv # manifest file created in step-2
    raw/
      X.zip # raw compressed files downloaded from source. some time this could be several files.
```

### Step-2: Prepare label files
Once datasets are downloaded, we use the following script to prepare manifest files:
```bash
python prep_all_datasets.py --config dataset_list.yaml
```
You can change the list of datasets you need in the `dataset_list.yaml` file.

### Step-3: Migrate the pretrained model
Put your model script inside of `models` folder, and have the hyperparams defined in `benchmark/evaluate_setup.yaml`:

```bash
model:
  # Path to the model's .py file. Now points to the wrapper script.
  path: models/detector_wrapper.py
  # Name of the model class within the .py file. Now points to the wrapper class.
  class_name: AudioDeepfakeDetector
  # The checkpoint path remains the same as it's passed through the wrapper.
  checkpoint: models/Best_LA_model_for_DF.pth # Ckpt for the exemplar W2V-ASSIST
  device: 'cuda:0'

  # These key-value pairs will be passed directly to the model's __init__ method.
  # This section now holds the configuration for the *raw* model that the wrapper uses.
  model_args:
    raw_model_path: models/baseline_model.py
    raw_model_class_name: Model
    raw_model_args: # Arguments for the raw model's __init__
      args: null
      model_device: 'cuda:0'
```

### Step-4: Run evaluation
```bash
python evaluate.py --config benchmark/evaluate_setup.yaml
```
By default, benchmarking is performed on all datasets. If you want to select a few to benchmark on, please define a new group in `benchmark/dataset_group.yaml`, for example:
```bash
asvspoof-series:
all:
  - name: ASVspoof2019
    manifest_path: asvspoof2019/processed/manifest_asvspoof2019.csv
  - name: ASVspoof2021-LA
    manifest_path: asvspoof2021_la/processed/manifest_asvspoof2021_la.csv
  - name: ASVspoof5
    manifest_path: asvspoof5/processed/manifest_asvspoof5.csv
```
then in the `evaluate_setup.yaml`, set `group_name: avspoof-series`. 

You likely need to change the batch size accordingly based on the type of GPU used.

## Contributing
While the team will keep updating the benchmark coverage, it is highly encouraged to suggest dataset addition via creating an issue and point us to the source link and paper.

## Citation
```
@inproceedings{yourname2025AUDDT,
  title={{AUDDT: An Open Benchmark Toolkit for Audio Deepfake Detection}},
  author={Your Name and Co-authors},
  booktitle={Conference Name},
  year={2025}
}
```

## License
This project is licensed for **academic and research use only**.  
Commercial use is **strictly prohibited** without prior written permission.  
See the full [LICENSE](./LICENSE) file for details.

## Disclaimer
We do not include any proprietary datasets or the ones with unknown sources for transparency. We also encourage users to be careful with the potential training/test overlap, e.g., some datasets like ASVspoof2019 / ASVspoof5 are widely used as training sets. Results obtained with this toolkit should solely be used for research purposes instead of advertisement for commercial usage.
