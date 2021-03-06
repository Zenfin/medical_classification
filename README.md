# ML Datasets

# Setup

1. Get the dataset from Vivek or Myself and place it in the root folder of this project.
Expects this file structure

`(ALL FILES FROM GIT)` next to `I2B2_data/track_2_training/TRAINING_FILES`

2. Create a virtualenv if desired.
3. Install the requirements. `pip install -r reqs.txt`

# Usage

To run classification of data `python run.py CLASSIFICATION_METHOD`
This will take the csv data in the file identified in `run.py`'s  `METHODS` dictionary
and make prediction using all the various algorithms in `ml.py`'s `ALL_CLASSIFIERS` dictionary.

If you wish to re-extract the data into the csvs you can run `python run.py CLASSIFICATION_METHOD extract`

# Adding additional fields.

Fields are stored in an ordered dictionary in the `fields.py` file.
The key is name of the column to be created, the `func` key's value is a function that does the extraction and
returns the value for that field.
`BPRS` keys identify the BPRS category from `rating_scales.py`'s `BPRS` dictionary.

# Changing the train/test percentage

You can change the `TRAIN_PERCENT` variable in the `ml.py` file.
