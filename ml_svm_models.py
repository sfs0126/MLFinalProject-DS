# -*- coding: utf-8 -*-
"""ML SVM Models

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1paqp0-gY7yxema3WNP2YkPfUc9QVX1wI

# SVM 
### Radial and Polynomial
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
import os
from torchvision.utils import make_grid
from torch.utils.data.dataloader import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.transforms import ToTensor
from torchvision import datasets, transforms
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib
import matplotlib.pyplot as plt
# %matplotlib inline

from sklearn import svm
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification
from sklearn.preprocessing import MinMaxScaler
import cv2
from tqdm import tqdm
import random
from random import sample
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report



drive.mount('/content/drive')

data_dir = ('/content/drive/MyDrive/MLData/dataset/dataset_updated')

print(os.listdir(data_dir))
print(os.listdir(data_dir + "/training_set"))

CATEGORIES = ['painting', 'engraving', 'drawings', 'iconography', 'sculpture']
for category in CATEGORIES:
    path=os.path.join(data_dir + "/training_set", category)
    for img in os.listdir(path):
        img_array=cv2.imread(os.path.join(path,img))
        plt.imshow(img_array)
        plt.show()
        break
    break

"""We uploaded the image data from a google drive folder. From here we were able to join the image data and category information. Now we can split the data into an X (the image) and Y (the category) to use the SVM on our dataset.

##### Training/Test Set
"""

training_data=[]
IMG_SIZE = 128

def create_training_data():
  for category in CATEGORIES:
    path=os.path.join(data_dir + "/training_set", category)
    class_num=CATEGORIES.index(category)
    for img in os.listdir(path):
      try:
        img_array=cv2.imread(os.path.join(path,img))
        new_array=cv2.resize(img_array,(IMG_SIZE,IMG_SIZE))
        training_data.append([new_array,class_num])
      except Exception as e:
        pass      
create_training_data() 

print(len(training_data))
lenofimage_training = len(training_data)

X=[]
Y=[]

for categories, label in training_data:
  X.append(categories)
  Y.append(label)
X= np.array(X).reshape(lenofimage_training,-1)

X.shape

Y=np.array(Y)
Y.shape

X_train, X_test, Y_train, Y_test = train_test_split(X,Y)

"""##### Sample Training Set"""

random.seed(1)
sample_data = sample(training_data, 700)
 
print(len(sample_data))
lenofimage_sample = len(sample_data)

x=[]
y=[]

for categories, label in sample_data:
  x.append(categories)
  y.append(label)
x= np.array(x).reshape(lenofimage_sample,-1)

x.shape

y=np.array(y)
y.shape

"""##### Validation Set"""

validation_data=[]
IMG_SIZE = 128

def create_validation_data():
  for category in CATEGORIES:
    path=os.path.join(data_dir + "/validation_set", category)
    class_num=CATEGORIES.index(category)
    for img in os.listdir(path):
      try:
        img_array=cv2.imread(os.path.join(path,img))
        new_array=cv2.resize(img_array,(IMG_SIZE,IMG_SIZE))
        validation_data.append([new_array,class_num])
      except Exception as e:
        pass  
create_validation_data() 

print(len(validation_data))
lenofimage_validation = len(validation_data)

X_val=[]
Y_val=[]

for categories, label in validation_data:
  X_val.append(categories)
  Y_val.append(label)
X_val= np.array(X_val).reshape(lenofimage_validation,-1)

X_val.shape

Y_val=np.array(Y_val)
Y_val.shape

"""##### Scaling X sets for fitting"""

scaling = MinMaxScaler(feature_range=(-1,1)).fit(x)
x = scaling.transform(x)
scaling = MinMaxScaler(feature_range=(-1,1)).fit(X)
X = scaling.transform(X)
scaling = MinMaxScaler(feature_range=(-1,1)).fit(X_train)
X_train = scaling.transform(X_train)
scaling = MinMaxScaler(feature_range=(-1,1)).fit(X_test)
X_test = scaling.transform(X_test)
scaling = MinMaxScaler(feature_range=(-1,1)).fit(X_val)
X_val = scaling.transform(X_val)

"""The dataset contained a training set and validation set. To sets the different svm models, we will use a sample set of the training images and preform cross validation to find the best parameters to use on our data. From there, we created the train and test split to test our best preforming radial and polynomial SVM models. Once our overall best model parameters are found, we will use the training set to train the final SVM and the validation set to measure the final models preformance accuracy. 

We scaled the data to improve accuracy and runtime of the models.

### Radial SVM

##### Parameter Tuning Lists
"""

c_list = [0.1, 1, 10, 100]
gamma_list = ['auto', 'scale']
class_weight_list = ['balanced', None]

"""##### Training and Validating Radial Models using 5-Fold CV"""

best_cv = 0
best_c = 0
best_gamma = 0
best_class_weight = 0
iters = 1

print("All SVM Radial Kernal Models:")

for c_val in c_list:
    
    for gamma_val in gamma_list:

      for class_weight_val in class_weight_list:

          model = svm.SVC(kernel='rbf', C=c_val, gamma=gamma_val, class_weight =class_weight_val)

          cvs = cross_val_score(model, x, y, cv = 5)

          cv = sum(cvs)/len(cvs)
          print(f'C: {c_val}    Gamma: {gamma_val}    Class Weight: {class_weight_val}    5-Fold CV Score: {cv}')

          if cv > best_cv:
            best_cv = cv
            best_c = c_val
            best_class_value = class_weight_val
            best_gamma = gamma_val

          iters += 1

"""##### The Best Radial Model"""

print(f'The best performing Support Vector Machine with Radial Kernel, model used {best_c} C value, \nhad a gamma of {best_gamma}, \nand had a class weight of {best_class_weight}, \n\
This model had a cross validation score of {round((100*best_cv), 2)}%')

model = svm.SVC(kernel='rbf', C= best_c, gamma=best_gamma, class_weight =best_class_value).fit(X_train,Y_train)

predictions = model.predict(X_test)

score = round((100*accuracy_score(Y_test, predictions)), 2)

print(f'Our model classified art images with an accuracy of: {score}%')

"""We used the sample data to test 16 different radial kernel SVM models. We had our highest accuracy on the sample data at 73% with cross validation using a C value of 10, gamma of scale, and class weight of none. 

From here, we trained the model on the training set and used the test set to determing the model accuracy. Our model has an accuracy of 78.2% on the final fit.

### Polynomial SVM

##### Parameter Tuning Lists
"""

c_list = [0.1, 1, 10, 100]
gamma_list = ['auto', 'scale']
class_weight_list = ['balanced', None]
degrees = [1, 2, 3]

"""##### Training and Validating Polynomial Models using 5-Fold CV"""

best_cv = 0
best_c = 0
best_gamma = 0
best_class_weight = 0
best_degree = 0
iters = 1

print("All SVM Polynomial Kernal Models:")

for c_val in c_list:
    
    for gamma_val in gamma_list:

      for class_weight_val in class_weight_list:
        
        for degree in degrees:

            model = svm.SVC(kernel='poly', C=c_val, gamma=gamma_val, class_weight =class_weight_val, degree = degree)

            cvs = cross_val_score(model, x, y, cv = 5)

            cv = sum(cvs)/len(cvs)
            print(f'Degree: {degree}    C: {c_val}    Gamma: {gamma_val}    Class Weight: {class_weight_val}    5-Fold CV Score: {cv}')

            if cv > best_cv:
                best_cv = cv
                best_c = c_val
                best_class_value = class_weight_val
                best_gamma = gamma_val
                best_degree = degree

            iters += 1

"""##### The Best Polynomial Model"""

print(f'The best performing Support Vector Machine with polynomial kernel, model used {best_c} C value, \nhad a gamma of {best_gamma}, \n\
had a class weight of {best_class_weight}, \n\
and had a degree of {best_degree}. \n\
This model had a cross validation score of {round((100*best_cv), 2)}%')

model = svm.SVC(kernel='poly', C= best_c, gamma=best_gamma, class_weight =best_class_weight, degree=best_degree).fit(X_train,Y_train)

predictions = model.predict(X_test)

score = round((100*accuracy_score(Y_test, predictions)), 2)

print(f'Our model classified art images with an accuracy of: {score}%')

"""We used the sample data to test 48 different polynomial kernel SVM models. We had our highest accuracy on the sample data at 70% with cross validation using a C value of 10, gamma of auto, class weight of balanced, and degree of 1. 

From here, we trained the model on the training set and used the test set to determing the model accuracy. Our model has an accuracy of 64.79% on the final fit.

Since our radial kernel model preformed the best, we will now fit the model using the training set and then determine the final model accuracy with the validation data.

### Validation of best SVM model
"""

model = svm.SVC(kernel='rbf', C= 10, gamma = 'scale', class_weight = None).fit(X,Y)

predictions = model.predict(X_val)

score = round((100*accuracy_score(Y_val, predictions)), 2)

print(f'Our model classified art images with an accuracy of: {score}%')

mat = confusion_matrix(Y_val, predictions)
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=CATEGORIES,
            yticklabels=CATEGORIES)
plt.xlabel('true label')
plt.ylabel('predicted label');

"""### Best SVM Model Accuracy Report"""

print("Accuracy on validation data is\n",classification_report(Y_val,predictions))

"""Using the optimized parameters, we fit the radial kernel SVM with a C of 10, gamma of scale, and class weight of none. Using the valitation set, we were able to achieve an accuracy of 77.69%. 

We included the matrix of predicted/correct lables to show the exact classification/misclassification of each art medium. 

The classification report shows us that the engraving and drawings categories had low accuracy compared to the other categories. 
"""