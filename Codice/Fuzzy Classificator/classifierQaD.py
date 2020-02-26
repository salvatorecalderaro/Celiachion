import pandas as pd
import numpy as np
import FuzzyClassificator as fc
import fylearn.fuzzylogic as ff
from sklearn.model_selection import train_test_split
from fylearn.fuzzylogic import TriangularSet
from FCLogger import SetLevel
import constant



resource_path = "Dataset/"
dataset_file = "dataset_virtuale.csv"
data = pd.read_csv(resource_path + dataset_file)
num_columns = data.shape[1] - 1


for column in data.columns:
    data[column] = pd.to_numeric(data[column])
    replace_with = float(data[column].sum()) / data.shape[0]
    data[column].fillna(replace_with, inplace=True)
data.to_csv(resource_path + "without_nan.csv")


train, test = train_test_split(data, test_size=0.3, random_state=0)
#test["Class"].replace({0: "", 1: ""}, inplace=True)
train.to_csv("ethalons.dat", index=False)
test.to_csv("candidates.dat", index=False)


fc.EthalonDataFile = "ethalons.dat"
fc.candidatesDataFile = "candidates.dat"
fc.neuroNetworkFile = "network.xml"
fc.sepSymbol = ","
SetLevel("DEBUG")
parameters = {
        "config": str(num_columns) + ",3,2,1", 
        "epochs": 120, 
        "rate": 0.6, 
        "momentum": 0.38, 
        "epsilon": 0.044, 
        "stop": 1}
fc.Main(learnParameters=parameters)


fc.reportDataFile = "report.txt"
fc.sepSymbol = ","
fc.showExpected = True
SetLevel("DEBUG")
parameters = {
        "config": str(num_columns) + ",3,2,1",
        "epochs": 100,
        "rate": 0.5,
        "momentum": 0.5,
        "epsilon": 0.05,
        "stop": 1}
fc.Main(classifyParameters=parameters)


confusion_matrix = np.zeros((2, 2))
counter = 0
med_counter = 0
med_positive = 0
med_negative = 0
with open('report.txt', 'r') as report_file:
    for line in report_file:
        index = line.find("Output")
        if index != -1:
            counter += 1
            line = line[index:]
            if line.__contains__("Min") or line.__contains__("Low"):
                if line.__contains__("0"):
                    confusion_matrix[0][0] += 1
                else:
                    confusion_matrix[1][0] += 1
            elif line.__contains__("Max") or line.__contains__("High"):
                if line.__contains__("1"):
                    confusion_matrix[1][1] += 1
                else:
                    confusion_matrix[0][1] += 1
            else:
                med_counter += 1
                if line.__contains__("0"):
                    med_negative += 1
                else:
                    med_positive += 1
if med_negative > med_positive:
    # consideriamo i valori med come target negativo
    confusion_matrix[0][0] += med_negative
    confusion_matrix[1][0] += med_positive
    med_value = "negative"
else:
    confusion_matrix[1][1] += med_positive
    confusion_matrix[0][1] += med_negative
    med_value = "positive"

print("Tot values classified: " + str(counter))
print("Number of med values: " + str(med_counter))
print("Negative Med correspondence: " + str(med_negative))
print("Positive Med correspondence: " + str(med_positive))
print("Med value chosen: " + str(med_value))
print("\nConfusion Matrix")
print("\tTN\t\tFP\n\tFN\t\tTP")
print(confusion_matrix)
print()

'''
TN FP
FN TP
'''
tn = confusion_matrix[0][0]
tp = confusion_matrix[1][1]
fn = confusion_matrix[1][0]
fp = confusion_matrix[0][1]

accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp)
specificity = tn / (tn + fp)
recall = tp / (tp + fn)

print("Accuracy: {0} %".format(round(accuracy * 100, 2)))
print("Precision: {0} %".format(round(precision * 100, 2)))
print("Specificity: {0} %".format(round(specificity * 100, 2)))
print("Recall: {0} %\n".format(round(recall * 100, 2)))