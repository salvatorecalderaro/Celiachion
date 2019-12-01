import pandas as pd
import numpy as np
import FuzzyClassificator as FC
import fylearn.fuzzylogic as ff
from sklearn.model_selection import train_test_split
from fylearn.fuzzylogic import TriangularSet
from FCLogger import SetLevel
from itertools import islice



def prepare_dataset(data_path):
    data = pd.read_csv(data_path)
    data = data.drop("referral_source", axis=1)
    data = data.replace(["F", "M", "t", "f", "?", "negative", "sick"], [0, 1, 1, 0, np.nan, 0, 1])

    for i in range(len(data.columns)):
        data[data.columns[i]] = pd.to_numeric(data[data.columns[i]])

    for i in range(len(data.columns)):
        name_column = data.columns[i]
        replace_with = data[name_column].mean()
        data[name_column].fillna(replace_with, inplace=True)

    return data



def to_fuzzy(data):
    for i in range(len(data.columns) - 1):
        max = ff.max(data[data.columns[i]])
        mean = ff.mean(data[data.columns[i]])
        min = ff.min(data[data.columns[i]])
        t = TriangularSet(min, mean, max)
        data[data.columns[i]] = t(np.array(data[data.columns[i]]))

    return data



def split_dataset(data):
    train, test = train_test_split(data, test_size=0.3, random_state=1)

    train.to_csv("ethalons.dat",index=False)

    x_test = test.drop("Class", axis=1)
    y_test = test["Class"]
    x_test.to_csv("candidates.dat",index=False)
    y_test.to_csv("realClass.dat", index=False)



def train_classifier():
    FC.EthalonDataFile ="ethalons.dat"
    FC.candidatesDataFile ="candidates.dat"
    FC.neuroNetworkFile = "network.xml"
    FC.sepSymbol=","
    SetLevel("DEBUG")

    parameters = {
        "config": "28,3,2,1",
        "epochs": 100,
        "rate": 0.5,
        "momentum": 0.5,
        "epsilon": 0.05,
        "stop": 1
    }
    FC.Main(learnParameters=parameters)



def classify():
    FC.reportDataFile = "report.txt"
    FC.sepSymbol=","
    FC.showExpected
    SetLevel("DEBUG")

    parameters = {
        "config": "28,3,2,1",
        "epochs": 100,
        "rate": 0.5,
        "momentum": 0.5,
        "epsilon": 0.05,
        "stop": 1
    }
    FC.Main(classifyParameters=parameters)



def evaluate_classifier(realClass_path, report_path):
    Y_test = []
    Y_pred = []
    count0 = 0
    count1 = 0

    with open(realClass_path, 'rt') as myfile:
        for line in myfile:
            Y_test.append(line.rstrip('\n'))

    for i in range(len(Y_test)):
        Y_test[i] = pd.to_numeric(Y_test[i])

    index = 0
    with open(report_path, 'r') as searchfile:
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

    with open(report_path, 'r') as searchfile:
        for line in islice(searchfile, 13, None):
            if "Min" in line:
                Y_pred.append(0)
            elif "Low" in line:
                Y_pred.append(0)
            elif "Med" in line:
                Y_pred.append(valMed)
            elif "High" in line:
                Y_pred.append(1)
            elif "Max" in line:
                Y_pred.append(1)
            else:
                continue

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

    return accuracy, precision, specificity, recall



def print_report(acc, prec, spec, rec):
    print("Accuracy: {0}%".format(acc))
    print("Precision: {0}%".format(prec))
    print("Specificity: {0}%".format(spec))
    print("Recall: {0}%\n".format(rec))



def menu():
    print("\n\n-----------------------")
    print("1. Learning Mode")
    print("2. Classifying Mode")
    print("3. Results")
    print("0. Exit")
    print("-----------------------")
    c = int(input())
    print("\n")
    return c



def op1():
    data_path = "Dataset/sick.csv"
    data = prepare_dataset(data_path)
    data = to_fuzzy(data)
    split_dataset(data)
    train_classifier()



def op2():
    classify()



def op3():
    realClass_path = 'realClass.dat'
    report_path = 'report.txt'
    acc,prec,spec,rec=evaluate_classifier(realClass_path, report_path)
    print_report(acc, prec, spec, rec)



c = -1
while(c != 0):
    c = menu()
    if(c == 1):
        op1()
    elif(c == 2):
        op2()
    elif(c == 3):
        op3()
    elif(c == 0):
        break
    else:
        print("Unknown command")
