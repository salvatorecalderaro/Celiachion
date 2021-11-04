import os
import pandas as pd
import numpy as np
import FuzzyClassificator as fc
import fylearn.fuzzylogic as fl
from FCLogger import SetLevel
import constant


neuro_networks_path = "Neuro Networks/Real Dataset/"
resource_path = "../Datasets/Real Dataset/"
dataset_file = "real_dataset.csv"
till_survey_dataset_file = "till_survey_real_dataset.csv"
till_survey_dataset_name = "survey"
till_poct_dataset_file = "till_poct_real_dataset.csv"
till_poct_dataset_name = "poct"
till_blood_tests_dataset_file = "till_blood_tests_real_dataset.csv"
till_blood_tests_dataset_name = "blood_tests"
complete_dataset_file = "complete_real_dataset.csv"
complete_dataset_name = "complete"
current_patient_file = "current_patient.csv"
current_patient_name = "current_patient"
ETHALONS = 0
CANDIDATES = 1

"""
def to_fuzzy(dataset):
    dataset = dataset.replace("nan", np.NaN)
    for column in ["IGA totali", "TTG IGG", "TTG_IGA"]:
        dataset[column] = pd.to_numeric(dataset[column])
        if(column == "IGA totali"):
            replace_with = constant.MEAN_IGA
            dataset[column].fillna(replace_with, inplace=True)
        if(column == "TTG IGG"):
            replace_with = constant.TTG_IGG_MEAN
            dataset[column].fillna(replace_with, inplace=True)
        # Vedere quali valori attribuire ai NaN (anche quelli di esami del sangue)
        if(column == 'TTG_IGA'):
            replace_with = constant.TTG_IGA_MEAN
            dataset[column].fillna(replace_with, inplace=True)

    for column in dataset.columns[0:-1]:
        x = np.unique(dataset[column])
        if 1 < len(x) < 4 and x.__contains__(1) and x.__contains__(0):
            t = fl.TriangularSet(constant.BINARY_MIN, constant.BINARY_MEAN, constant.BINARY_MAX)
        else:
            if column == "POCT":
                triangular_set = fl.TriangularSet(constant.POCT_MIN, constant.POCT_MEAN, constant.POCT_MAX)
                dataset[column] = triangular_set(np.array(dataset[column]))
            elif column == "IGA totali":
                triangular_set = fl.TriangularSet(constant.MIN_IGA, constant.MEAN_IGA, constant.MAX_IGA)
                dataset[column] = triangular_set(np.array(dataset[column]))
            elif column == "TTG IGG":
                triangular_set = fl.TriangularSet(constant.TTG_IGG_MIN, constant.TTG_IGG_MEAN, constant.TTG_IGG_MAX)
                dataset[column] = triangular_set(np.array(dataset[column]))
            elif column == "TTG_IGA":
                triangular_set = fl.TriangularSet(constant.TTG_IGA_MIN, constant.TTG_IGA_MEAN, constant.TTG_IGA_MAX)
                dataset[column] = triangular_set(np.array(dataset[column]))
    pazienti_fuzzy = pd.read_csv(resource_path + "pazienti_reali_fuzzy.csv")
    pazienti_fuzzy = pazienti_fuzzy.append(dataset)
    pazienti_fuzzy.to_csv(resource_path + "pazienti_reali_fuzzy.csv", index=False)
"""


def split_dataset(
    till_survey_dataset_file,
    till_poct_dataset_file,
    till_blood_tests_dataset_file,
    complete_dataset_file,
):
    # survey dataset
    till_survey_dataframe = pd.DataFrame()
    till_survey_dataframe["Anemia"] = dataframe["Anemia"]
    till_survey_dataframe["Osteopenia"] = dataframe["Osteopenia"]
    till_survey_dataframe["Diarrea Cronica"] = dataframe["Diarrea Cronica"]
    till_survey_dataframe["Mancata Crescita"] = dataframe["Mancata Crescita"]
    till_survey_dataframe["Disturbi Genetici"] = dataframe["Disturbi Genetici"]
    till_survey_dataframe["Madre Celiaca"] = dataframe["Madre Celiaca"]
    till_survey_dataframe["Class"] = dataframe["Class"]
    till_survey_dataframe.to_csv(
        resource_path + till_survey_dataset_file, index=False
    )
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
    till_poct_dataframe.to_csv(
        resource_path + till_poct_dataset_file, index=False
    )
    # survey, poct and blood tests dataset
    till_blood_tests_dataframe = pd.DataFrame(columns=dataframe.columns)
    for index, row in dataframe.iterrows():
        if not np.isnan(row["Esami del sangue"]):
            till_blood_tests_dataframe = till_blood_tests_dataframe.append(
                row, ignore_index=True
            )
    for column in ["TTG_IGG", "TTG_IGA"]:
        till_blood_tests_dataframe[column] = pd.to_numeric(
            till_blood_tests_dataframe[column]
        )
        replace_with = (
            float(till_blood_tests_dataframe[column].sum())
            / till_blood_tests_dataframe.shape[0]
        )
        till_blood_tests_dataframe[column].fillna(replace_with, inplace=True)
    for column in [
        "Anemia",
        "Osteopenia",
        "Diarrea Cronica",
        "Mancata Crescita",
        "Disturbi Genetici",
        "Madre Celiaca",
        "POCT",
        "Esami del sangue",
        "Class",
    ]:
        till_blood_tests_dataframe[column] = pd.to_numeric(
            till_blood_tests_dataframe[column], downcast="integer"
        )
    till_blood_tests_dataframe.to_csv(
        resource_path + till_blood_tests_dataset_file,
        index=False,
        na_rep=np.nan,
    )
    # complete dataset
    complete_dataframe = pd.DataFrame(columns=dataframe.columns)
    for index, row in dataframe.iterrows():
        complete_dataframe = complete_dataframe.append(row, ignore_index=True)
    for column in ["IGA_totali", "TTG_IGG", "TTG_IGA", "Esami del sangue"]:
        complete_dataframe[column] = pd.to_numeric(complete_dataframe[column])
        replace_with = (
            float(complete_dataframe[column].sum())
            / complete_dataframe.shape[0]
        )
        complete_dataframe[column].fillna(replace_with, inplace=True)
    for column in [
        "Anemia",
        "Osteopenia",
        "Diarrea Cronica",
        "Mancata Crescita",
        "Disturbi Genetici",
        "Madre Celiaca",
        "POCT",
        "Class",
    ]:
        complete_dataframe[column] = pd.to_numeric(
            complete_dataframe[column], downcast="integer"
        )
    complete_dataframe.to_csv(
        resource_path + complete_dataset_file, index=False, na_rep=np.nan
    )


def prepare_learning_mode(dataset_name):
    fc.ethalonsDataFile = (
        neuro_networks_path + "ethalons_" + dataset_name + ".csv"
    )
    fc.neuroNetworkFile = (
        neuro_networks_path + "network_" + dataset_name + ".xml"
    )
    fc.reportDataFile = neuro_networks_path + "report_" + dataset_name + ".txt"
    fc.bestNetworkFile = (
        neuro_networks_path + "best_nn_" + dataset_name + ".xml"
    )
    fc.bestNetworkInfoFile = (
        neuro_networks_path + "best_nn_" + dataset_name + ".txt"
    )
    fc.sepSymbol = ","
    fc.showExpected = True
    # SetLevel("DEBUG")
    SetLevel("ERROR")


def prepare_classify_mode(dataset_name, current_patient_name):
    fc.candidatesDataFile = (
        neuro_networks_path + "candidates_" + current_patient_name + ".csv"
    )
    fc.neuroNetworkFile = (
        neuro_networks_path + "network_" + dataset_name + ".xml"
    )
    fc.reportDataFile = neuro_networks_path + "report_" + dataset_name + ".txt"
    fc.bestNetworkFile = (
        neuro_networks_path + "best_nn_" + dataset_name + ".xml"
    )
    fc.bestNetworkInfoFile = (
        neuro_networks_path + "best_nn_" + dataset_name + ".txt"
    )
    fc.sepSymbol = ","
    fc.showExpected = False
    # SetLevel("DEBUG")
    SetLevel("ERROR")


def prepare_dataset(dataset_file, dataset_name, type):
    dataset = pd.read_csv(resource_path + dataset_file, index_col=False)
    for column in dataset.columns[0:-1]:
        if column == "POCT":
            triangular_set = fl.TriangularSet(
                constant.POCT_MIN, constant.POCT_MEAN, constant.POCT_MAX
            )
            dataset[column] = triangular_set(np.array(dataset[column]))
        elif column == "IGA_totali":
            triangular_set = fl.TriangularSet(
                constant.MIN_IGA, constant.MEAN_IGA, constant.MAX_IGA
            )
            dataset[column] = triangular_set(np.array(dataset[column]))
        elif column == "TTG_IGG":
            triangular_set = fl.TriangularSet(
                constant.TTG_IGG_MIN,
                constant.TTG_IGG_MEAN,
                constant.TTG_IGG_MAX,
            )
            dataset[column] = triangular_set(np.array(dataset[column]))
        elif column == "TTG_IGA":
            triangular_set = fl.TriangularSet(
                constant.TTG_IGA_MIN,
                constant.TTG_IGA_MEAN,
                constant.TTG_IGA_MAX,
            )
            dataset[column] = triangular_set(np.array(dataset[column]))
    if type == ETHALONS:
        dataset.to_csv(
            neuro_networks_path + "ethalons_" + dataset_name + ".csv",
            index=False,
        )
    elif type == CANDIDATES:
        dataset.to_csv(
            neuro_networks_path + "candidates_" + dataset_name + ".csv",
            index=False,
        )


def update_real_dataset(new_patients):
    patients = pd.DataFrame()
    if os.path.isfile(resource_path + dataset_file):
        patients = pd.read_csv(resource_path + dataset_file)
        pd.concat([patients, new_patients]).to_csv(
            resource_path + dataset_file, index=False, na_rep=np.nan
        )
    else:
        new_patients.to_csv(
            resource_path + dataset_file, index=False, na_rep=np.nan
        )


def learning_mode(
    num_columns,
    num_neurons_first_hidden_layer,
    num_neurons_second_hidden_layer,
):
    parameters = {
        "config": str(num_columns)
        + ","
        + str(num_neurons_first_hidden_layer)
        + ","
        + str(num_neurons_second_hidden_layer)
        + ",1",
        "epochs": 100,
        "rate": 0.5,
        "momentum": 0.5,
        "epsilon": 0.05,
        "stop": 1,
    }
    fc.Main(learnParameters=parameters)


def classifying_mode(
    num_columns,
    num_neurons_first_hidden_layer,
    num_neurons_second_hidden_layer,
):
    parameters = {
        "config": str(num_columns)
        + ","
        + str(num_neurons_first_hidden_layer)
        + ","
        + str(num_neurons_second_hidden_layer)
        + ",1",
        "epochs": 100,
        "rate": 0.5,
        "momentum": 0.5,
        "epsilon": 0.05,
        "stop": 1,
    }
    fc.Main(classifyParameters=parameters)


def print_result(dataset_name):
    with open(fc.reportDataFile) as report_file:
        for line in report_file:
            index = line.find("Output")
            if index != -1:
                line = line[index:]
                bracket_opening = line.find("[")
                bracket_closing = line.find("]")
                print(
                    "Classification for "
                    + dataset_name
                    + ":\t\t"
                    + line[bracket_opening + 2 : bracket_closing - 1]
                )


new_patients = pd.read_json("example.json")
num_neurons_first_hidden_layer = 6
num_neurons_second_hidden_layer = 4
if np.isnan(new_patients["Class"][0]):
    print(
        "---------------------------------------------------------------------"
    )
    for index, patient in new_patients.iterrows():
        patient_data = str(patient)
        print(
            "Classification patient n. "
            + str(index + 1)
            + ":\n"
            + patient_data[: patient_data.find("Class")]
        )
        pd.DataFrame(patient).transpose().to_csv(
            resource_path + current_patient_file, index=False, na_rep=np.nan
        )
        prepare_dataset(current_patient_file, current_patient_name, CANDIDATES)
        prepare_classify_mode(till_survey_dataset_name, current_patient_name)
        classifying_mode(
            6, num_neurons_first_hidden_layer, num_neurons_second_hidden_layer
        )
        print_result(till_survey_dataset_name)
        prepare_classify_mode(till_poct_dataset_name, current_patient_name)
        classifying_mode(
            7, num_neurons_first_hidden_layer, num_neurons_second_hidden_layer
        )
        print_result(till_poct_dataset_name)
        if not np.isnan(patient["Esami del sangue"]):
            prepare_classify_mode(
                till_blood_tests_dataset_name, current_patient_name
            )
            classifying_mode(
                11,
                num_neurons_first_hidden_layer,
                num_neurons_second_hidden_layer,
            )
            print_result(till_blood_tests_dataset_name)
        prepare_classify_mode(complete_dataset_name, current_patient_name)
        classifying_mode(
            11, num_neurons_first_hidden_layer, num_neurons_second_hidden_layer
        )
        print_result(complete_dataset_name)
        print(
            "---------------------------------------------------------------------"
        )
else:
    update_real_dataset(new_patients)
    dataframe = pd.read_csv(resource_path + dataset_file, index_col=False)
    split_dataset(
        till_survey_dataset_file,
        till_poct_dataset_file,
        till_blood_tests_dataset_file,
        complete_dataset_file,
    )
    prepare_dataset(
        till_survey_dataset_file, till_survey_dataset_name, ETHALONS
    )
    prepare_dataset(till_poct_dataset_file, till_poct_dataset_name, ETHALONS)
    prepare_dataset(
        till_blood_tests_dataset_file, till_blood_tests_dataset_name, ETHALONS
    )
    prepare_dataset(complete_dataset_file, complete_dataset_name, ETHALONS)
    prepare_learning_mode(till_survey_dataset_name)
    learning_mode(
        6, num_neurons_first_hidden_layer, num_neurons_second_hidden_layer
    )
    prepare_learning_mode(till_poct_dataset_name)
    learning_mode(
        7, num_neurons_first_hidden_layer, num_neurons_second_hidden_layer
    )
    prepare_learning_mode(till_blood_tests_dataset_name)
    learning_mode(
        11, num_neurons_first_hidden_layer, num_neurons_second_hidden_layer
    )
    prepare_learning_mode(complete_dataset_name)
    learning_mode(
        11, num_neurons_first_hidden_layer, num_neurons_second_hidden_layer
    )
