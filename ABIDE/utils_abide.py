import os
import csv
import numpy as np
import scipy.io as sio
import glob

from nilearn import connectome

data_folder = 'ABIDE_pcp/cpac/filt_noglobal'
phenotypic_folder = './ABIDE_pcp/Phenotypic_V1_0b_preprocessed1.csv'
sid_folder = './subject_IDs.txt'

def fetch_filenames(subject_IDs, file_type):
    """
        subject_list : list of short subject IDs in string format
        file_type    : must be one of the available file types

    returns:
        filenames    : list of filetypes (same length as subject_list)
    """
    # Specify file mappings for the possible file types
    filemapping = {'func_preproc': '_func_preproc.nii.gz',
                   'rois_ho': '_rois_ho.1D'}

    # The list to be filled
    filenames = []

    os.chdir(data_folder)
    # Fill list with requested file paths
    for i in range(len(subject_IDs)):
        try:
            filenames.append(glob.glob('*' + subject_IDs[i] + filemapping[file_type])[0])
        except IndexError:
            # Return N/A if subject ID is not found
            filenames.append('N/A')

    return filenames

def get_timeseries(fl):
    """
        subject      : the subject IDs
        atlas_name   : the atlas based on which the timeseries are generated e.g. aal, cc200
        fl           : timeseries file name

    returns:
        time_series  : timeseries arrays (timepoints x regions)
    """

    print("Reading timeseries file %s" % fl)
    timeseries = np.loadtxt(fl, skiprows=0)

    return timeseries

def subject_connectivity(timeseries, subject, kind):
    """
        timeseries   : timeseries table for subject (timepoints x regions)
        subject      : the subject ID
        atlas_name   : name of the parcellation atlas used
        kind         : the kind of connectivity to be used, e.g. lasso, partial correlation, correlation
        save         : save the connectivity matrix to a file
        save_path    : specify path to save the matrix if different from subject folder

    returns:
        connectivity : functional connectivity matrix (regions x regions)
    """

    print("Estimating %s matrix for subject %s" % (kind, subject))
    try:
        if kind in ['tangent', 'partial correlation', 'correlation']:
            conn_measure = connectome.ConnectivityMeasure(kind=kind)
            connectivity = conn_measure.fit_transform([timeseries])[0]

            return connectivity
    except Exception as e:
        print("kind error: {}".format(e))

def get_ids(num_subjects=None):
    """
    return:
        subject_IDs    : list of all subject IDs
    """

    subject_IDs = np.genfromtxt(sid_folder, dtype=str)

    if num_subjects is not None:
        subject_IDs = subject_IDs[:num_subjects]

    return subject_IDs

def get_subject_score(subject_list, score):
    """
    :param subject_list:    list of subject IDs
    :param score:           the kind of phenotypic value, e.g. SITE_ID, DX_GROUP
    :return:                dict where the key is the subject id and the value is phenotypic value
    """
    scores_dict = {}

    with open(phenotypic_folder) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row['SUB_ID'] in subject_list:
                scores_dict[row['SUB_ID']] = row[score]

    return scores_dict

def site_percentage(train_ind, perc, subject_list):
    """
        train_ind    : indices of the training samples
        perc         : percentage of training set used
        subject_list : list of subject IDs
    return:
        labeled_indices      : indices of the subset of training samples
    """

    train_list = subject_list[train_ind]
    sites = get_subject_score(train_list, score='SITE_ID')
    unique = np.unique(list(sites.values())).tolist()
    site = np.array([unique.index(sites[train_list[x]]) for x in range(len(train_list))])

    labeled_indices = []

    for i in np.unique(site):
        id_in_site = np.argwhere(site == i).flatten()

        num_nodes = len(id_in_site)
        labeled_num = int(round(perc * num_nodes))
        labeled_indices.extend(train_ind[id_in_site[:labeled_num]])

    return labeled_indices

def get_networks(subject_list, kind, atlas_name="aal", variable='connectivity'):
    """
        subject_list : list of subject IDs
        kind         : the kind of connectivity to be used, e.g. lasso, partial correlation, correlation
        atlas_name   : name of the parcellation atlas used
        variable     : variable name in the .mat file that has been used to save the precomputed networks
    return:
        matrix      : feature matrix of connectivity networks (num_subjects x network_size)
    """

    all_networks = []
    for subject in subject_list:
        fl = os.path.join(data_folder, subject,
                          subject + "_" + atlas_name + "_" + kind + ".mat")
        matrix = sio.loadmat(fl)[variable]
        all_networks.append(matrix)

    idx = np.triu_indices_from(all_networks[0], 1)
    with np.errstate(divide='ignore', invalid='ignore'):
        norm_networks = [np.arctanh(mat) for mat in all_networks]
    vec_networks = [mat[idx] for mat in norm_networks]
    matrix = np.vstack(vec_networks)

    return matrix
