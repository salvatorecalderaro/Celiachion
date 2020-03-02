import os
import constant
import pandas as pd
import numpy as np
import FuzzyClassificator as fc
import fylearn.fuzzylogic as fl
from FCLogger import SetLevel
from sklearn.model_selection import train_test_split


resource_path = "../Datasets/"
dataset_file = "dataset_virtuale.csv"
dataframe = pd.read_csv(resource_path + dataset_file, index_col=False)

till_survey_dataset_file = "till_survey_virtual_dataset.csv"
till_survey_dataset_name = "survey"
till_poct_dataset_file = "till_poct_virtual_dataset.csv"
till_poct_dataset_name = "poct"
till_blood_tests_dataset_file = "till_blood_tests_virtual_dataset.csv"
till_blood_tests_dataset_name = "blood_tests"
complete_dataset_file = "complete_virtual_dataset.csv"
complete_dataset_name = "complete"


def split_dataset(till_survey_dataset_file, till_poct_dataset_file, till_blood_tests_dataset_file, complete_dataset_file):
    # survey dataset
    till_survey_dataframe = pd.DataFrame()
    till_survey_dataframe["Anemia"] = dataframe["Anemia"]
    till_survey_dataframe["Osteopenia"] = dataframe["Osteopenia"]
    till_survey_dataframe["Diarrea Cronica"] = dataframe["Diarrea Cronica"]
    till_survey_dataframe["Mancata Crescita"] = dataframe["Mancata Crescita"]
    till_survey_dataframe["Disturbi Genetici"] = dataframe["Disturbi Genetici"]
    till_survey_dataframe["Madre Celiaca"] = dataframe["Madre Celiaca"]
    till_survey_dataframe["Class"] =dataframe["Class"]
    till_survey_dataframe.to_csv("../Datasets/" + till_survey_dataset_file, index=False)
    # survey and poct dataset
    till_poct_dataframe = pd.DataFrame()
    till_poct_dataframe["Anemia"] = dataframe["Anemia"]
    till_poct_dataframe["Osteopenia"] = dataframe["Osteopenia"]
    till_poct_dataframe["Diarrea Cronica"] = dataframe["Diarrea Cronica"]
    till_poct_dataframe["Mancata Crescita"] = dataframe["Mancata Crescita"]
    till_poct_dataframe["Disturbi Genetici"] = dataframe["Disturbi Genetici"]
    till_poct_dataframe["Madre Celiaca"] = dataframe["Madre Celiaca"]
    till_poct_dataframe["POCT"] = dataframe["POCT"]
    till_poct_dataframe["Class"] = dataframe["Class"]
    till_poct_dataframe.to_csv("../Datasets/" + till_poct_dataset_file, index=False)
    # survey, poct and blood tests dataset
    till_blood_tests_dataframe = pd.DataFrame(columns=dataframe.columns)
    for index, row in dataframe.iterrows():
        if not np.isnan(row["Esami del sangue"]):
            till_blood_tests_dataframe = till_blood_tests_dataframe.append(row, ignore_index=True)
    for column in ["TTG IGG", "TTG IGA"]:
        till_blood_tests_dataframe[column] = pd.to_numeric(till_blood_tests_dataframe[column])
        replace_with = float(till_blood_tests_dataframe[column].sum()) / till_blood_tests_dataframe.shape[0]
        till_blood_tests_dataframe[column].fillna(replace_with, inplace=True)
    for column in ["Anemia", "Osteopenia", "Diarrea Cronica", "Mancata Crescita", "Disturbi Genetici",
                   "Madre Celiaca", "POCT", "Esami del sangue", "Class"]:
        till_blood_tests_dataframe[column] = pd.to_numeric(till_blood_tests_dataframe[column], downcast="integer")
    till_blood_tests_dataframe.to_csv("../Datasets/" + till_blood_tests_dataset_file, index=False, na_rep=np.nan)
    # complete dataset
    complete_dataframe = pd.DataFrame(columns=dataframe.columns)
    for index, row in dataframe.iterrows():
        complete_dataframe = complete_dataframe.append(row, ignore_index=True)
    for column in ["TTG IGG", "TTG IGA", "Esami del sangue"]:
        complete_dataframe[column] = pd.to_numeric(complete_dataframe[column])
        replace_with = float(complete_dataframe[column].sum()) / complete_dataframe.shape[0]
        complete_dataframe[column].fillna(replace_with, inplace=True)
    for column in ["Anemia", "Osteopenia", "Diarrea Cronica", "Mancata Crescita", "Disturbi Genetici",
                   "Madre Celiaca", "POCT", "Esami del sangue", "Class"]:
        complete_dataframe[column] = pd.to_numeric(complete_dataframe[column], downcast="integer")
    complete_dataframe.to_csv("../Datasets/" + complete_dataset_file, index=False, na_rep=np.nan)


def prepare_classificator(dataset_name):
    fc.ethalonsDataFile = "Neuro Networks/ethalons_" + dataset_name + ".csv"
    fc.candidatesDataFile = "Neuro Networks/candidates_" + dataset_name + ".csv"
    fc.neuroNetworkFile = "Neuro Networks/network_" + dataset_name + ".xml"
    fc.reportDataFile = "Neuro Networks/report_" + dataset_name + ".txt"
    fc.bestNetworkFile = "Neuro Networks/best_nn_" + dataset_name + ".xml"
    fc.bestNetworkInfoFile = "Neuro Networks/best_nn_" + dataset_name + ".txt"
    fc.sepSymbol = ","
    fc.showExpected = True
    SetLevel("DEBUG")


def prepare_dataset(dataset_file, dataset_name):
    dataset = pd.read_csv("../Datasets/" + dataset_file, index_col=False)
    for column in dataset.columns[0:-1]:
        if column == "POCT":
            triangular_set = fl.TriangularSet(constant.POCT_MIN, constant.POCT_MEAN, constant.POCT_MAX)
            dataset[column] = triangular_set(np.array(dataset[column]))
        elif column == "IGA totali":
            triangular_set = fl.TriangularSet(constant.MIN_IGA, constant.MEAN_IGA, constant.MAX_IGA)
            dataset[column] = triangular_set(np.array(dataset[column]))
        elif column == "TTG IGG":
            triangular_set = fl.TriangularSet(constant.TTG_IGG_MIN, constant.TTG_IGG_MEAN, constant.TTG_IGG_MAX)
            dataset[column] = triangular_set(np.array(dataset[column]))
        elif column == "TTG IGA":
            triangular_set = fl.TriangularSet(constant.TTG_IGA_MIN, constant.TTG_IGA_MEAN, constant.TTG_IGA_MAX)
            dataset[column] = triangular_set(np.array(dataset[column]))
    train, test = train_test_split(dataset, test_size=0.3, random_state=0)
    train.to_csv("Neuro Networks/ethalons_" + dataset_name + ".csv", index=False)
    test.to_csv("Neuro Networks/candidates_" + dataset_name + ".csv", index=False)


def learning_mode(num_columns, num_neurons_first_hidden_layer, num_neurons_second_hidden_layer):
    os.system("clear")
    parameters = {
        "config": str(num_columns) + ","
        + str(num_neurons_first_hidden_layer) + ","
        + str(num_neurons_second_hidden_layer) + ",1",
        "epochs": 100,
        "rate": 0.5,
        "momentum": 0.5,
        "epsilon": 0.05,
        "stop": 1
    }
    fc.Main(learnParameters=parameters)


def classifying_mode(num_columns, num_neurons_first_hidden_layer, num_neurons_second_hidden_layer):
    os.system("clear")
    parameters = {
        "config": str(num_columns) + ","
        + str(num_neurons_first_hidden_layer) + ","
        + str(num_neurons_second_hidden_layer) + ",1",
        "epochs": 100,
        "rate": 0.5,
        "momentum": 0.5,
        "epsilon": 0.05,
        "stop": 1
    }
    fc.Main(classifyParameters=parameters)


def evaluate_classifier():
    confusion_matrix = np.zeros((2, 2))
    counter = 0
    med_counter = 0
    med_positive = 0
    med_negative = 0
    with open(fc.reportDataFile) as report:
        for line in report:
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
    print_report(confusion_matrix)


def print_report(confusion_matrix):
    print("\nConfusion Matrix")
    print("TN\t\tFP\nFN\t\tTP")
    print(confusion_matrix)
    print()
    tn = confusion_matrix[0][0]
    fp = confusion_matrix[0][1]
    fn = confusion_matrix[1][0]
    tp = confusion_matrix[1][1]
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    specificity = tn / (tn + fp)
    recall = tp / (tp + fn)
    print(str(int(tn)) + "\t\t" + str(int(fp)) + "\n" + str(int(fn)) + "\t\t" + str(int(tp)))
    print()
    print("Accuracy: {0} %".format(round(accuracy * 100, 2)))
    print("Precision: {0} %".format(round(precision * 100, 2)))
    print("Specificity: {0} %".format(round(specificity * 100, 2)))
    print("Recall: {0} %\n".format(round(recall * 100, 2)))


def menu():
    os.system("clear")
    print("--------------------------------")
    print("1. Survey")
    print("2. Survey and POCT")
    print("3. Survey, POCT and blood tests")
    print("4. Complete")
    print("0. Exit")
    print("--------------------------------")
    print()
    temp = int(input())
    print()
    return temp


def sub_menu():
    os.system("clear")
    print("--------------------------------")
    print("1. Train classifier")
    print("2. Classify")
    print("3. Evaluate classifier")
    print("0. Main menu")
    print("--------------------------------")
    print()
    temp = int(input())
    print()
    return temp


split_dataset(till_survey_dataset_file, till_poct_dataset_file, till_blood_tests_dataset_file, complete_dataset_file)
prepare_dataset(till_survey_dataset_file, till_survey_dataset_name)
prepare_dataset(till_poct_dataset_file, till_poct_dataset_name)
prepare_dataset(till_blood_tests_dataset_file, till_blood_tests_dataset_name)
prepare_dataset(complete_dataset_file, complete_dataset_name)
c = -1
while c != 0:
    c = menu()
    if c > 0 and c < 5:
        num_params = -1
        num_neurons_first_hidden_layer = int(input("Number of neurons in first hidden layer: "))
        num_neurons_second_hidden_layer = int(input("Number of neurons in second hidden layer: "))
        if c == 1:
            prepare_classificator(till_survey_dataset_name)
            num_params = 6
        elif c == 2:
            prepare_classificator(till_poct_dataset_name)
            num_params = 7
        elif c == 3:
            prepare_classificator(till_blood_tests_dataset_name)
            num_params = 11
        elif c == 4:
            prepare_classificator(complete_dataset_name)
            num_params = 11
        sc = -1
        while sc != 0:
            sc = sub_menu()
            if sc > 0 and sc < 4:
                if sc == 1:
                    learning_mode(num_params, num_neurons_first_hidden_layer, num_neurons_second_hidden_layer)
                elif sc == 2:
                    classifying_mode(num_params, num_neurons_first_hidden_layer, num_neurons_second_hidden_layer)
                elif sc == 3:
                    evaluate_classifier()
                input("\nPress enter to continue")
            elif sc != 0:
                print("Unknown command. Please, try again: ", end="")
    elif c != 0:
        print("Unknown command. Please, try again: ", end="")
