import os
import argparse
import numpy as np
import hcprep

# AWS S3 access key, AWS S3 secret key
ACCESS_KEY = 'AKIAXO65CT57MJFTUIFK'
SECRET_KEY = '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'

# path to store data
root_path = './data/'

# number of subjects to download per HCP task (1-500) (default: 3)
n = 3

def main():
    np.random.seed(13089)

    hcprep.paths.make_sure_path_exists(root_path)

    hcp_info = hcprep.info.basics()

    print('Downloading data of {} subjects to {}'.format(n, root_path))
    for task in hcp_info.tasks:
        for subject in hcp_info.subjects[task][:n]:
            for run in hcp_info.runs:
                hcprep.download.download_subject_data(
                    ACCESS_KEY=ACCESS_KEY,
                    SECRET_KEY=SECRET_KEY,
                    subject=subject,
                    task=task,
                    run=run,
                    output_path=root_path
                )


if __name__ == '__main__':
    main()

