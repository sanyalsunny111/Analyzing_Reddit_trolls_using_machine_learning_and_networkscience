import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
import collections
from datetime import datetime
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from clean_data_normies_1 import append_stats
from sklearn.tree import export_graphviz
import matplotlib.pyplot as plt
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from yellowbrick.classifier import ClassificationReport
import pickle
from tkinter import ttk
from tkinter import *
# Load troll+bot data
with open('lib/data/my_clean_data_training.csv', encoding = 'utf8') as f:
    my_data_training = pd.read_csv(f, sep=',')
print("Clean Dataset Shape for Training: ", my_data_training.shape)
# Load normal data
with open('lib/data/ML_data_32.csv', encoding = 'utf8') as f:
    my_data_normies = pd.read_csv(f, sep=',')
print(my_data_normies.shape)


# combine both datasets
columns_inter = set(my_data_normies.columns).intersection(set(my_data_training.columns))
print(columns_inter)
my_data = my_data_training[columns_inter].append(my_data_normies[columns_inter])
print("Clean Dataset Shape Combined: ", my_data.columns)

# drop duplicates
my_data = my_data.drop_duplicates(subset=['author','link_id','created_utc'])

# correct labeling
my_data.loc[my_data.author == 'PoliticsModeratorBot','target'] = 'bot'

# Label known bots in normies
bot_authors = my_data[my_data.target == 'bot'].author.unique()
my_data.loc[((my_data.target == 'normal') & (my_data.author.isin(bot_authors))),'target'] = 'bot'

body = my_data['body'].values.tolist()
auth = my_data['author'].values.tolist()

my_data.dropna()
print("After removing columns not considered: ", my_data.shape)

my_data[my_data['target']=='normal'].describe()

my_data[my_data['target']=='bot'].describe()

my_data[my_data['target']=='troll'].describe()

print(my_data[my_data.isin([np.nan, np.inf, -np.inf]).any(1)])
print(my_data[my_data==np.nan].shape)
# Number of targets
targets = collections.Counter(my_data['target'])
print(targets)

# Randomize the data
rand_data = my_data.sample(frac=1)
rd = rand_data.copy()

# SPlit data into train and test data. 
# train_test_split is not used because we remove comment body for train and test data but we need that for firther analysis.

columns = ['link_id', 'author', 'created_utc', 'body','over_18']
my_data.drop(columns, inplace=True, axis=1)
X_train = my_data.head(69646).drop(['target'], axis=1).values.astype('float32')
X_test = my_data.tail(29848).drop(['target'], axis=1).values.astype('float32')
y_train =  my_data.head(69646)['target'].values
y_test = my_data.tail(29848)['target'].values

#Fitting a Random Forest Classifier
Classifier = RandomForestClassifier(n_estimators=20, random_state=0)  
Classifier.fit(X_train, y_train)  
y_pred = Classifier.predict(X_test)

test_df = rd.tail(29848).copy()
test_df['predicted'] = y_pred
y_true = np.array(y_test)

matrix = pd.crosstab(y_true, y_pred, rownames=['True'], colnames=['Predicted'], margins=True)
print(matrix)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("Mcc:", metrics.matthews_corrcoef(y_test, y_pred))
print("F1 :", metrics.f1_score(y_test, y_pred, average=None))
print("Recall :", metrics.recall_score(y_test, y_pred, average=None))
print("Precision:", metrics.precision_score(y_test, y_pred, average=None))
print(my_data.columns)

# prediction on training set

# Model Accuracy
y_true = y_train

# Choose 5 samples of each set to display in GUI

troll_set = test_df[test_df['predicted']=='troll'].sample(n=5)
normal_set =test_df[test_df['predicted']=='normal'].sample(n=5)
all_set = troll_set.append(normal_set).copy()
# Randomizing the selected sampled
all_set=all_set.sample(frac=1)

print('-----------------------------------------------------------------------------------------------------------------------')

'''
The following code is used to display the GUI
'''

window = Tk()

for i in range(10):
    window.columnconfigure(i, weight=1, minsize=75)
    window.rowconfigure(i, weight=1, minsize=50)

    
    frame = Frame(master=window,relief=RAISED,borderwidth=1)
    frame.grid(row=i, column=0, padx=5, pady=5)

    label = Label(master=frame, text=all_set['author'].iloc[i],width = 25)
    label.pack(padx=5, pady=5)

    frame = Frame(master=window,relief=RAISED,borderwidth=1)
    frame.grid(row=i, column=1, padx=5, pady=5)
    #print(test_df['body'].iloc[i])

    label = Label(master=frame, text=all_set['body'].iloc[i],width = 100)
    print(i)
    label.pack(padx=5, pady=5)


    frame = Frame(master=window,relief=RAISED,borderwidth=1)
    frame.grid(row=i, column=2, padx=5, pady=5)

    label = Label(master=frame, text=all_set['predicted'].iloc[i])
    label.pack(padx=5, pady=5)


window.mainloop()















