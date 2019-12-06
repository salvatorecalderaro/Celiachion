import pandas as pd
import numpy as np
import FuzzyClassificator as FC
import fylearn.fuzzylogic as ff
from sklearn.model_selection import train_test_split
from fylearn.fuzzylogic import TriangularSet
from fylearn.fuzzylogic import TrapezoidalSet
from FCLogger import SetLevel


resource_path = "../resource/"
data = pd.read_csv(resource_path + "dataset_virtuale.csv")

"""
# for sick.csv #
data = data.drop("referral_source", axis=1)
data = data.drop("TBG", axis=1)
data = data.drop("TBG_measured", axis=1)
data = data.replace(["F", "M", "t", "f", "?", "negative", "sick"], [0, 1, 1, 0, np.NaN, 0, 1])
"""

num_columns = data.shape[1] - 1


def prepare_dataset():
    for column in data.columns:
        data[column] = pd.to_numeric(data[column])
        replace_with = data[column].mean()
        data[column].fillna(replace_with, inplace=True)
    data.to_csv(resource_path + "without_nan.csv")


def to_fuzzy():
    for column in data.columns[0:-1]:
        x = np.unique(data[column])
        if 1 < len(x) < 4 and x.__contains__(1) and x.__contains__(0):
            t = TriangularSet(0, 1, 1)
            data[column] = t(np.array(data[column]))
        else:
            max = ff.max(data[column])
            mean = ff.mean(data[column])
            min = ff.min(data[column])
            t = TriangularSet(min, mean, max)
            data[column] = t(np.array(data[column]))
    data.to_csv(resource_path + "to_fuzzy.csv")


def split_dataset():
    train, test = train_test_split(data, test_size=0.3, random_state=0)
    train.to_csv("ethalons.dat", index=False)
    test.to_csv("candidates.dat", index=False)


def train_classifier():
    FC.EthalonDataFile = "ethalons.dat"
    FC.candidatesDataFile = "candidates.dat"
    FC.neuroNetworkFile = "network.xml"
    FC.sepSymbol = ","
    SetLevel("DEBUG")
    parameters = {
        "config": str(num_columns) + ",3,2,1",
        "epochs": 100,
        "rate": 0.5,
        "momentum": 0.5,
        "epsilon": 0.05,
        "stop": 1
    }
    FC.Main(learnParameters=parameters)


def classify():
    FC.reportDataFile = "report.txt"
    FC.sepSymbol = ","
    FC.showExpected = True
    SetLevel("DEBUG")
    parameters = {
        "config": str(num_columns) + ",3,2,1",
        "epochs": 100,
        "rate": 0.5,
        "momentum": 0.5,
        "epsilon": 0.05,
        "stop": 1
    }
    FC.Main(classifyParameters=parameters)


def evaluate_classifier(report_path):
    TN = 0
    TP = 0
    FN = 0
    FP = 0
    counter = 0
    med_counter = 0
    med_positive = 0
    med_negative = 0
    with open(report_path, 'r') as report_file:
        for line in report_file:
            if line.__contains__("Output"):
                counter += 1
                line = line[line.find("Output"):]
                if line.__contains__("Min") or line.__contains__("Low"):
                    if line.__contains__("0"):
                        TN += 1
                    else:
                        FN += 1
                elif line.__contains__("Max") or line.__contains__("High"):
                    if line.__contains__("1"):
                        TP += 1
                    else:
                        FP += 1
                else:
                    med_counter += 1
                    if line.__contains__("0"):
                        med_negative += 1
                    else:
                        med_positive += 1
    if med_negative > med_positive:
        # consideriamo i valori med come target negativo
        TN += med_negative
        FN += med_positive
    else:
        TP += med_positive
        FP += med_negative

    print("Tot values classified " + str(counter))
    print("Number of med values " + str(med_counter))
    print("TN " + str(TN))
    print("TP " + str(TP))
    print("FN " + str(FN))
    print("FP " + str(FP))

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP)
    specificity = TN / (TN + FP)
    recall = TP / (TP + FN)
    print_report(accuracy, precision, specificity, recall)


def print_report(acc, prec, spec, rec):
    print("Accuracy: {0}%".format(acc * 100))
    print("Precision: {0}%".format(prec * 100))
    print("Specificity: {0}%".format(spec * 100))
    print("Recall: {0}%\n".format(rec * 100))


def menu():
    print("\n\n-----------------------")
    print("1. Learning Mode")
    print("2. Classifying Mode")
    print("3. Results")
    print("0. Exit")
    print("-----------------------")
    temp = int(input())
    print("\n")
    return temp


def op1():
    prepare_dataset()
    to_fuzzy()
    split_dataset()
    train_classifier()


def op2():
    classify()


def op3():
    evaluate_classifier("report.txt")


c = -1
while c != 0:
    c = menu()
    if c == 1:
        op1()
    elif c == 2:
        op2()
    elif c == 3:
        op3()
    elif c == 0:
        break
    else:
        print("Unknown command")


"""
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
                if Y_test[index] == 0:
                    count0 += 1
                    index += 1
                else:
                    count1 += 1
                    index += 1
            else:
                index += 1
                continue

    if count0 > count1:
        val_med = 0
    else:
        val_med = 1

    with open(report_path, 'r') as searchfile:
        for line in islice(searchfile, 13, None):
            if "Min" in line:
                Y_pred.append(0)
            elif "Low" in line:
                Y_pred.append(0)
            elif "Med" in line:
                Y_pred.append(val_med)
            elif "High" in line:
                Y_pred.append(1)
            elif "Max" in line:
                Y_pred.append(1)
            else:
                continue

    confusion_matrix = np.zeros((2, 2))

    for i in range(len(Y_pred)):
        if Y_pred[i] == 0:
            if Y_test[i] == 0:
                confusion_matrix[0][0] += 1.0
            else:
                confusion_matrix[1][0] += 1.0
        else:
            if Y_test[i] == 0:
                confusion_matrix[0][1] += 1.0
            else:
                confusion_matrix[1][1] += 1.0

    '''
    TP FN
    FP TN
    '''

    TP = confusion_matrix[0][0]
    FN = confusion_matrix[0][1]
    FP = confusion_matrix[1][0]
    TN = confusion_matrix[1][1]

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP)
    specificity = TN / (TN + FP)
    recall = TP / (TP + FN)

    return accuracy, precision, specificity, recall
"""
