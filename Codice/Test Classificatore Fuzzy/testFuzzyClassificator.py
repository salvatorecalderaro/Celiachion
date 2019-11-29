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
from itertools import islice



############################
# Importazione del dataset #
############################
data = pd.read_csv("Dataset/sick.csv")



########################################
# Gestione delle variabili del dataset #
########################################
data = data.drop("referral_source", axis=1)
data = data.replace(["F", "M", "t", "f", "?", "negative", "sick"], [0, 1, 1, 0, np.nan, 0, 1])


# Converto i valori (visti come stringhe) in valori numerici
for i in range(len(data.columns)):
    data[data.columns[i]] = pd.to_numeric(data[data.columns[i]])



#################################
# Creazione dei parametri fuzzy #
#################################
for i in range(len(data.columns) - 1):
    max = ff.max(data[data.columns[i]])
    mean = ff.mean(data[data.columns[i]])
    min = ff.min(data[data.columns[i]])
    t = TriangularSet(min, mean, max)
    data[data.columns[i]] = t(np.array(data[data.columns[i]]))



#####################
# Split del dataset #
#####################
train, test = train_test_split(data, test_size=0.3, random_state=1)


# TrainSet
train.to_csv("ethalons.dat",index=False)


# TestSet (x_test: parametri, y_test: target)
x_test = test.drop("Class", axis=1)
y_test = test["Class"]
x_test.to_csv("candidates.dat",index=False)
y_test.to_csv("realClass.dat", index=False) # Contiene le classi reali del test set



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



####################################################
# Confronto tra i target predetti e i target reali #
####################################################
Y_test = []
Y_pred = []
count0 = 0
count1 = 0


# Inserisco i valori reali del testSet situati in realClass.dat in un array Y_test
with open('realClass.dat', 'rt') as myfile:
    for line in myfile:
        Y_test.append(line.rstrip('\n'))


# Converto i valori di Y_test (visti come stringhe) in valori numerici
for i in range(len(Y_test)):
    Y_test[i] = pd.to_numeric(Y_test[i])


# Stabilisco se valutare 'Med' come valore 0 o come valore 1
index = 0
with open('report.txt', 'r') as searchfile:
    for line in islice(searchfile, 13, None):
        if "Med" in line:
            if(Y_test[index] == 0):
                count0 += 1
                index += 1
            else:
                count1 += 1
                index += 1
        else:
            index += 1
            continue

if(count0 > count1):
    valMed = 0
else:
    valMed = 1


# Confronto risultati predetti con risultati reali
index = 0
with open('report.txt', 'r') as searchfile:
    for line in islice(searchfile, 13, None):
        if "Min" in line:
            Y_pred.append(0)
            index += 1
        elif "Low" in line:
            Y_pred.append(0)
            index += 1
        elif "Med" in line:
            Y_pred.append(valMed)
            index += 1
        elif "High" in line:
            Y_pred.append(1)
            index += 1
        elif "Max" in line:
            Y_pred.append(1)
            index += 1
        else:
            index += 1
            continue



###########################
# Valutazione del modello #
###########################
TP = 0.0
TN = 0.0
FP = 0.0
FN = 0.0
accuracy = 0.0
errorRate = 0.0
precision = 0.0
specificity = 0.0
recall= 0.0

confusionMatrix = np.zeros((2,2))

for i in range(len(Y_pred)):
    if(Y_pred[i] == 0):
        if(Y_test[i] == 0):
            confusionMatrix[0][0] += 1.0
        else:
            confusionMatrix[1][0] += 1.0
    else:
        if(Y_test[i] == 0):
            confusionMatrix[0][1] += 1.0
        else:
            confusionMatrix[1][1] += 1.0

'''
TP FN
FP TN
'''

TP = confusionMatrix[0][0]
FN = confusionMatrix[0][1]
FP = confusionMatrix[1][0]
TN = confusionMatrix[1][1]

accuracy = (TP + TN) / (TP + TN + FP + FN)
precision = TP / (TP + FP)
specificity = TN / (TN + FP)
recall = TP / (TP + FN)

print("\n-Risultati-")
print("Accuracy: {0}%".format(accuracy))
print("Precision: {0}%".format(precision))
print("Specificity: {0}%".format(specificity))
print("Recall: {0}%\n".format(recall))
