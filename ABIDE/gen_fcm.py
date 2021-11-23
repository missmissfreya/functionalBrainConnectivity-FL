import os
import shutil
import scipy.io as sio
from utils_abide import *

num_subjects = 871

atlas = 'ho'

connectivity = 'correlation'

files = ['rois_ho', 'conn_mat']

filemapping = {'func_preproc': 'func_preproc.nii.gz',
               'rois_ho': 'rois_ho.1D',
               'conn_mat': '_' + atlas + '_' + connectivity + '.mat'}

def main():
    subject_IDs = get_ids(num_subjects).tolist()

    # Create a folder for each subject
    '''
    for s, fname in zip(subject_IDs, fetch_filenames(subject_IDs, files[0])):
        time_series = get_timeseries(fname)

        # Compute and save functional connectivity matrices
        connectivity_mat = subject_connectivity(time_series, s, connectivity)
        sio.savemat(s + filemapping['conn_mat'], {'connectivity': connectivity_mat})

        subject_folder = os.path.join('./', s)
        if not os.path.exists(subject_folder):
            os.makedirs(subject_folder)

        # Get the base filename for each subject
        base = fname.split(files[0])[0]

        # Move each subject file to the subject folder
        if not os.path.exists(os.path.join(subject_folder, base + filemapping['rois_ho'])):
            shutil.move(base + filemapping['rois_ho'], subject_folder)
        if not os.path.exists(os.path.join(subject_folder, s + filemapping['conn_mat'])):
            shutil.move(s + filemapping['conn_mat'], subject_folder)
    '''
    # Generate features and labels
    features = get_networks(subject_IDs, kind=connectivity, atlas_name=atlas)
    labels = get_subject_score(subject_IDs, score='DX_GROUP')

    # Get international brain imaging laboratories for collecting data
    sites = get_subject_score(subject_IDs, score='SITE_ID')

    return features, labels, sites

if __name__ == '__main__':
    features, labels, sites = main()
