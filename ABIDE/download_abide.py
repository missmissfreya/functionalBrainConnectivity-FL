from nilearn import datasets

# Selected pipeline
pipeline = 'cpac'

# Input data variables
num_subjects = 871

# Files to fetch
files = ['rois_ho']

# Download database files
abide = datasets.fetch_abide_pcp(data_dir="./", n_subjects=num_subjects, pipeline=pipeline, derivatives=files,
                                 band_pass_filtering=True, global_signal_regression=False)
