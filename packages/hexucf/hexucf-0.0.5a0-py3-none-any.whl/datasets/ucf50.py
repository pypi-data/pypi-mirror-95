import urllib.request
import os
import patoolib
import pandas as pd
import numpy as np
import math
import datasets.utils as utils


def __download_ucf50(data_dir_path):
    ucf_rar = data_dir_path + '/UCF50.rar'

    URL_LINK = 'https://www.crcv.ucf.edu/data/UCF50.rar'

    if not os.path.exists(data_dir_path):
        os.makedirs(data_dir_path)

    if not os.path.exists(ucf_rar):
        print('ucf file does not exist, downloading from Internet')
        urllib.request.urlretrieve(url=URL_LINK, filename=ucf_rar,
                                   reporthook=utils.reporthook)

    print('unzipping ucf file')
    patoolib.extract_archive(ucf_rar, outdir=data_dir_path)


def __scan_ucf50(data_dir_path, limit):
    input_data_dir_path = data_dir_path + '/UCF50'

    result = dict()

    dir_count = 0
    for f in os.listdir(input_data_dir_path):
        __help_scan_ucf50(input_data_dir_path, f, dir_count, result)
        if dir_count == limit:
            break
    return result


def __help_scan_ucf50(input_data_dir_path, f, dir_count, result):
    file_path = input_data_dir_path + os.path.sep + f
    if not os.path.isfile(file_path):
        dir_count += 1
        for ff in os.listdir(file_path):
            video_file_path = file_path + os.path.sep + ff
            result[video_file_path] = f


def __scan_ucf50_with_labels(data_dir_path, labels):
    input_data_dir_path = data_dir_path + '/UCF50'

    result = dict()

    dir_count = 0
    for label in labels:
        __help_scan_ucf50(input_data_dir_path, label, dir_count, result)
    return result


def load_data(data_dist_path):
    UFC50_data_dir_path = data_dist_path + "/UCF50"
    if not os.path.exists(UFC50_data_dir_path):
        __download_ucf50(data_dist_path)

    videos = []
    labels = []
    name_class_labels = dict()

    dir_count = 0
    for f in os.listdir(UFC50_data_dir_path):
        file_path = UFC50_data_dir_path + os.path.sep + f
        print(file_path)
        if not os.path.isfile(file_path):
            dir_count += 1
            for video in os.listdir(file_path):
                videos.append(file_path + os.path.sep + video)
                labels.append(dir_count - 1)
                name_class_labels[dir_count - 1] = f

    videos = pd.DataFrame(videos, labels).reset_index()
    videos.columns = ["labels", "video_name"]
    videos.groupby('labels').count()

    train_set = pd.DataFrame()
    test_set = pd.DataFrame()
    for i in set(labels):
        vs = videos.loc[videos["labels"] == i]
        vs_range = np.arange(len(vs))
        np.random.seed(12345)
        np.random.shuffle(vs_range)

        vs = vs.iloc[vs_range]
        last_train = len(vs) - len(vs) // 3
        train_vs = vs.iloc[:last_train]
        train_set = train_set.append(train_vs)
        test_vs = vs.iloc[last_train:]
        test_set = test_set.append(test_vs)

    train_set = train_set.reset_index().drop("index", axis=1)
    test_set = test_set.reset_index().drop("index", axis=1)

    train_videos_dir = os.path.join(UFC50_data_dir_path, "Train_Videos")
    test_videos_dir = os.path.join(UFC50_data_dir_path, "Test_Videos")
    try:
        os.mkdir(train_videos_dir)
    except FileExistsError as ae:
        print("Folder Already Created")
    try:
        os.mkdir(test_videos_dir)
    except FileExistsError as ae:
        print("Folder Already Created")

    utils.video_capturing_function(UFC50_data_dir_path, train_set, "Train_Videos")
    utils.video_capturing_function(UFC50_data_dir_path, test_set, "Test_Videos")

    train_dir_path = UFC50_data_dir_path + os.path.sep + 'Train_Videos'
    test_dir_path = UFC50_data_dir_path + os.path.sep + 'Test_Videos'

    train_frames = []
    for i in np.arange(len(train_set.video_name)):
        vid_file_name = os.path.basename(train_set.video_name[i]).split(".")[0]
        train_frames.append(len(os.listdir(os.path.join(train_dir_path, vid_file_name))))

    test_frames = []
    for i in np.arange(len(test_set.video_name)):
        vid_file_name = os.path.basename(test_set.video_name[i]).split('.')[0]
        test_frames.append(len(os.listdir(os.path.join(test_dir_path, vid_file_name))))

    utils.frame_generating_function(train_set, train_dir_path)
    utils.frame_generating_function(test_set, test_dir_path)

    train_vid_dat = pd.DataFrame()
    validation_vid_dat = pd.DataFrame()
    for label in set(labels):
        label_dat = train_set.loc[train_set["labels"] == label]
        train_len_label = math.floor(len(label_dat) * 0.80)

        train_dat_label = label_dat.iloc[:train_len_label]
        validation_dat_label = label_dat.iloc[train_len_label:]

        train_vid_dat = train_vid_dat.append(train_dat_label, ignore_index=True)
        validation_vid_dat = validation_vid_dat.append(validation_dat_label, ignore_index=True)

    train_dataset = utils.data_load_function_frames(train_vid_dat, train_dir_path)
    test_dataset = utils.data_load_function_frames(test_set, test_dir_path)
    validation_dataset = utils.data_load_function_frames(validation_vid_dat, train_dir_path)

    train_labels = np.array(train_vid_dat.labels)
    test_labels = np.array(test_set.labels)
    validation_labels = np.array(validation_vid_dat.labels)

    return (train_dataset, train_labels), (test_dataset, test_labels), (validation_dataset, validation_labels)


if __name__ == '__main__':
    (train_x, train_y), (test_x, test_y), (validation_x, validation_y) = load_data('/tmp')
