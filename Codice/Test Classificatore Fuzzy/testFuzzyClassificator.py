############
# Librerie #
############
import pandas as pd
import numpy as np
import FuzzyClassificator as FC
import fylearn.fuzzylogic as ff
from sklearn.model_selection import train_test_split
from fylearn.fuzzylogic import TriangularSet
from FCLogger import SetLevel



############################
# Importazione del dataset #
############################
#data = pd.read_csv("Datasets/sick.csv")
data = pd.read_csv("Dataset/sick.csv")


############################################
# Conversione  delle variabili del dataset #
############################################
data = data.drop("referral_source", axis=1)
data = data.replace(["F", "M", "t", "f", "?", "negative", "sick"], [0, 1, 1, 0, np.nan, 0, 1])

# Converto i valori (visti come stringhe) in valori numerici
for i in range(len(data.columns)):
    data[data.columns[i]] = pd.to_numeric(data[data.columns[i]])



#################################
# Creazione dei parametri fuzzy #
#################################
data.columns
for i in range(len(data.columns) - 1):
    max = ff.max(data[data.columns[i]])
    mean = ff.mean(data[data.columns[i]])
    min = ff.min(data[data.columns[i]])
    t = TriangularSet(min, mean, max)
    data[data.columns[i]] = t(np.array(data[data.columns[i]]))



#####################
# Split del dataset #
#####################
train = data[0:3017]
train.to_csv("ethalons.dat",index=False)

x_test = data[3017:-1].drop("Class",axis=1)
y_test = data[3017:-1]['Class']

x_test.to_csv("candidates.dat",index=False)
y_test.to_csv("ytest.dat", index=False) # Contiene le classi reali del test set



#########################
# Classificazione Fuzzy #
#########################
FC.ethalonDataFile = "ethalons.dat"
FC.candidatesDataFile = "candidates.dat"
FC.neuroNetworkFile = "network.xml"
FC.reportDataFile = "report.txt"
FC.sepSymbol = ","
SetLevel("DEBUG")

parameters = {
    "config": "28,3,2,1",
    "epochs": 100,
    "rate": 0.5,
    "momentum": 0.5,
    "epsilon": 0.05,
    "stop": 1
}

FC.Main(learnParameters=parameters) # Learning mode
FC.Main(classifyParameters=parameters)  # Classifying mode
