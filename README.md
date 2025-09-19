# AUDDT: Audio Unified Deepfake Detection Benchmark Toolkit

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/License-CC_BY--NC_4.0-orange.svg">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.8+-green.svg">
  <img alt="Paper" src="https://img.shields.io/badge/arXiv-xxxx.xxxxx-b31b1b.svg">
  <img alt="Issues" src="https://img.shields.io/github/issues/your_username/AUDIT">
</p>

**AUDDT** is a benchmark toolkit for audio deepfake detection. The landscape of audio deepfake detection is fragmented with numerous datasets, each having its own data format and evaluation protocol. AUDIT addresses this by providing a unified platform to seamlessly benchmark pretrained models against a wide variety of public datasets.

The current version includes standardized preparation scripts for **27+ datasets**.

![AUDiT Workflow Diagram](assets/audit_workflow.png)
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

The full list of 27+ supported datasets is maintained in a public Google Sheet for easy viewing and filtering.

➡️ **[View Full Dataset List on Google Sheets](https://docs.google.com/spreadsheets/d/1amUSrwiUk3DpiuxcxNuSE-xB77aPApSug2A0FTuvwD4/edit?usp=sharing)**

## Update Log
We are actively developing AUDIT. See below for the latest updates.
* **2025-09-19**
    * Birth of AUDIT
    * Added 27 datasets to the benchmark
    * Added an examplar baseline model

## Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/your_username/AUDIT.git](https://github.com/your_username/AUDIT.git)
    cd AUDIT
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

### Step-2: Prepare label files
Once datasets are downloaded, we use the following script to prepare manifest files:
```bash
python prep_all_datasets.py --config dataset_list.yaml
```
You can change the list of datasets you need in the `dataset_list.yaml` file.

### Step-3: Migrate the pretrained model
Put your model script inside of `models` folder, and have the hyperparams defined in `benchmark/evaluate_setup.yaml`. See an examplar pretrained model in `models/baseline_model.py`, its hyperparams are defined in the `model` section in `benchmark/evaluate_setup.yaml`.

### Step-4: Run evaluation
```bash
python evaluate.py --config benchmark/evaluate_setup.yaml
```

## Contributing
While the team will keep updating the benchmark coverage, it is highly encouraged to suggest dataset addition via creating an issue and point us to the source link and paper.

## Citation
```
@inproceedings{yourname2025audit,
  title={{AUDiT: An Open Benchmark Toolkit for Audio Deepfake Detection}},
  author={Your Name and Co-authors},
  booktitle={Conference Name},
  year={2025}
}
```

## License
This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.

## Disclaimer
We do not include any proprietary datasets or the ones with unknown sources for transparency. We also encourage users to be careful with the potential training/test overlap, e.g., some datasets like ASVspoof2019 / ASVspoof5 are widely used as training sets. Results obtained with this toolkit should solely be used for research purposes instead of advertisement for commercial usage.
