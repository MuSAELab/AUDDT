# Description

As of Sep 2025, the following datasets need to be manually downloaded and put inside of data folder:
- HABLA (we provide .sh script for downloading but have noticed errors for some networks)
- MSceneSpeech
- EnhanceSpeech

### HABLA

### MSceneSpeech

The files for the MSceneSpeech dataset are in a Google Drive; therefore, follow the steps below to download it and put inside of your data folder:

1. First, download the dataset (only the test folder) from the Google Drive repository by following: https://speechai-demo.github.io/MSceneSpeech

2. Insert the zip file in a folder called "mscenespeech/raw" inside your data root
 
3. Lastly, run the ```./download/get_mscenespeech.sh``` script.

In the end, your folder structure should be like this:

```
data_root/
 ├── mscenespeech/
 │   ├── raw/
 │   │   └── test-download_datetime.zip
 │   └── processed/
 │       └── test/
 │           └── *.wav
 └── ...
```

### EnhanceDataset

For the EnhanceSpeech dataset, follow the steps below to download it and put inside of your data folder:

1. First, download the dataset (only the test folder) from the Google Drive repository by following: http://hguimaraes.me/DiTSE

2. Insert the zip file in a folder called "enhancespeech/raw" inside your data root

3. Now, run the ```./download/get_enhancespeech.sh``` script.

In the end, your folder structure should be like this:

```bash
data_root/
 ├── enhancespeech/
 │   ├── raw/
 │   │   └── DiTSE_Results-download_datetime.zip
 │   └── processed/
 │       └── DiTSE_Results/
 │           └── **/*.wav
 └── ...
```