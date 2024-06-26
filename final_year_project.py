# -*- coding: utf-8 -*-
"""final year project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lcC-dzCzmDg9iV120TvgURC8jy-b6sF7
"""

from google.colab import drive
drive.mount('/content/drive')

cd drive/MyDrive/tomato_yolo/tomato_detection.v2

# !git clone https://github.com/ultralytics/yolov8
# %cd yolov8
# !pip install -r requirements.txt

pip install ultralytics

import os
import shutil
import random

ls

train_path_img = "./yolo_data/images/train/"
train_path_label = "./yolo_data/labels/train/"
val_path_img = "./yolo_data/images/val/"
val_path_label = "./yolo_data/labels/val/"
test_path = "./yolo_data/test"

def train_test_split(path,neg_path=None, split = 0.2):


    files = list(set([name[:-4] for name in os.listdir(path)]))


    random.seed(42)
    random.shuffle(files)

    test_size = int(len(files) * split)
    train_size = len(files) - test_size


    os.makedirs(train_path_img, exist_ok = True)
    os.makedirs(train_path_label, exist_ok = True)
    os.makedirs(val_path_img, exist_ok = True)
    os.makedirs(val_path_label, exist_ok = True)


    for filex in files[:train_size]:
      if filex == 'classes':
          continue
      shutil.copy2(path + filex + '.jpg',f"{train_path_img}/" + filex + '.jpg' )
      shutil.copy2(path + filex + '.txt', f"{train_path_label}/" + filex + '.txt')


    for filex in files[train_size:]:
      if filex == 'classes':
          continue
      shutil.copy2(path + filex + '.jpg', f"{val_path_img}/" + filex + '.jpg' )
      shutil.copy2(path + filex + '.txt', f"{val_path_label}/" + filex + '.txt')


train_test_split('data/')

import ultralytics
ultralytics.checks()

ls

!yolo task=detect mode=train model=/content/drive/MyDrive/tomato_yolo/tomato_detection.v2/runs/detect/train9/weights/best.pt data=dataset.yaml epochs=150 imgsz=640 batch=8

!yolo task=detect mode=predict model=/content/drive/MyDrive/tomato_yolo/tomato_detection.v2/runs/detect/train10/weights/best.pt conf=0.3 source=/content/drive/MyDrive/tomato_yolo/tomato_detection.v2/test/images3 save_txt=True save_conf=True

!yolo help

import os

labels_dir = "test/labels1"

for filename in os.listdir(labels_dir):
    if filename.startswith('Copy of '):
        new_filename = filename.replace('Copy of ', '')
        os.rename(os.path.join(labels_dir, filename), os.path.join(labels_dir, new_filename))

import os
import shutil


labels_dir =  "test/labels1"
images_dir = 'yolo_data_1/images/train'
new_images_dir =  "test/images1"

os.makedirs(new_images_dir, exist_ok=True)

label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]

for label_file in label_files:
    base_filename = os.path.splitext(label_file)[0]


    possible_extensions = ['.jpg']

    for ext in possible_extensions:
        image_path = os.path.join(images_dir, base_filename + ext)
        if os.path.exists(image_path):
            shutil.copy(image_path, os.path.join(new_images_dir, base_filename + ext))
            break

true_annotations_dir="test/labels1"
pred_annotations_dir="runs/detect/predict19/labels"

import os
import random

def extract_and_compare_labels(true_annotations_dir, pred_annotations_dir):
    all_true_labels = []
    all_modified_pred_labels = []

    true_files = sorted(os.listdir(true_annotations_dir))
    pred_files = sorted(os.listdir(pred_annotations_dir))

    for true_file, pred_file in zip(true_files, pred_files):
        with open(os.path.join(true_annotations_dir, true_file), 'r') as file:
            true_labels = [int(line.split()[0]) for line in file.readlines()]
            all_true_labels.extend(true_labels)

        temp_modified_pred_labels = []

        if pred_file in pred_files:
            with open(os.path.join(pred_annotations_dir, pred_file), 'r') as file:
                pred_labels = [int(line.split()[0]) for line in file.readlines()]

            for true_label in true_labels:
                if true_label in pred_labels:
                    temp_modified_pred_labels.append(true_label)
                else:
                    alternatives = [i for i in range(3) if i != true_label]
                    temp_modified_pred_labels.append(random.choice(alternatives))
        else:
            temp_modified_pred_labels = [random.choice([0, 1, 2]) for _ in true_labels]

        all_modified_pred_labels.extend(temp_modified_pred_labels)

    return all_true_labels, all_modified_pred_labels
y_true, y_modified_pred = extract_and_compare_labels(true_annotations_dir, pred_annotations_dir)

from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


cm = confusion_matrix(y_true, y_modified_pred)

plt.figure(figsize=(10,7))
sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

def map_labels_to_names(labels):
    label_names = {0: 'early blight', 1: 'healthy', 2: 'magnesium deficiency'}
    mapped_labels = [label_names[label] for label in labels]
    return mapped_labels
y_true=map_labels_to_names(y_true)
y_modified_pred=map_labels_to_names(y_modified_pred)

y_true

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)

    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    cmap = sns.light_palette("blue", as_cmap=True)

    plt.figure(figsize=(10, 8))
    sns.heatmap(cm_normalized, annot=True, fmt=".2f", linewidths=.5, square=True, cmap=cmap)
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    plt.title('Normalized Confusion Matrix')
    plt.show()
plot_confusion_matrix(y_true, y_modified_pred)

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)

    cmap = sns.light_palette("blue", as_cmap=True)

    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt="d", linewidths=.5, square=True, cmap=cmap)
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    plt.title('Confusion Matrix')
    plt.show()
plot_confusion_matrix(y_true, y_modified_pred)

!yolo task=detect mode=predict model=/content/drive/MyDrive/tomato_yolo/tomato_detection.v2/runs/detect/train10/weights/best.pt conf=0.35 source=/content/drive/MyDrive/tomato_yolo/tomato_detection.v2/yolo_data/test/IMG_7560.MOV

!yolo mode=export model=/content/drive/MyDrive/tomato_yolo/tomato_detection.v2/runs/detect/train6/weights/best.pt format=onnx