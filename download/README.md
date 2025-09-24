As of Sep 2025, the following datasets need to be manually downloaded and put inside of data folder:
- HABLA (we provide .sh script for downloading but have noticed errors for some networks)
- MSceneSpeech
- EnhanceDataset

### HABLA

### MSceneSpeech

### EnhanceDataset
For EnhanceDataset, follow the steps below to download it and put inside of your data folder:

First, download the dataset (only the test folder) from the Google Drive repository
by following: http://hguimaraes.me/DiTSE
Insert the zip file in a folder called "enhancespeech/raw" inside your data root
Unzip the compressed file and insert in a folder called "enhancespeech/processed" inside your data root.
In the end, your folder structure should be like this:

data_root/
 ├── enhancespeech/
 │   ├── raw/
 │   │   └── DiTSE_Results-download_datetime.zip
 │   ├── processed/
 │   │   └── DiTSE_Results/
 │   │       └── **/*.wav
 │   └── manifest_enhancespeech.csv
 └── ...