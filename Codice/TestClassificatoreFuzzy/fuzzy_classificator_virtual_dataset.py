import pandas as pd
import numpy as np
import FuzzyClassificator as fc


resource_path = "../Datasets/"
dataset_file = "dataset_virtuale.csv"
dataset = pd.read_csv(resource_path + dataset_file, index_col=False)


def split_dataset(till_survey_dataset_file, till_poct_dataset_file, till_blood_tests_dataset_file):
    till_survey_dataset = pd.DataFrame()
    till_survey_dataset["Anemia"] = dataset["Anemia"]
    till_survey_dataset["Osteopenia"] = dataset["Osteopenia"]
    till_survey_dataset["Diarrea Cronica"] = dataset["Diarrea Cronica"]
    till_survey_dataset["Mancata Crescita"] = dataset["Mancata Crescita"]
    till_survey_dataset["Disturbi Genetici"] = dataset["Disturbi Genetici"]
    till_survey_dataset["Madre Celiaca"] = dataset["Madre Celiaca"]
    till_survey_dataset["Class"] = dataset["Class"]
    till_survey_dataset.to_csv("../Datasets/" + till_survey_dataset_file, index=False)
    till_poct_dataset = pd.DataFrame()
    till_poct_dataset["Anemia"] = dataset["Anemia"]
    till_poct_dataset["Osteopenia"] = dataset["Osteopenia"]
    till_poct_dataset["Diarrea Cronica"] = dataset["Diarrea Cronica"]
    till_poct_dataset["Mancata Crescita"] = dataset["Mancata Crescita"]
    till_poct_dataset["Disturbi Genetici"] = dataset["Disturbi Genetici"]
    till_poct_dataset["Madre Celiaca"] = dataset["Madre Celiaca"]
    till_poct_dataset["POCT"] = dataset["POCT"]
    till_poct_dataset["Class"] = dataset["Class"]
    till_poct_dataset.to_csv("../Datasets/" + till_poct_dataset_file, index=False)
    till_blood_tests_dataset = pd.DataFrame(columns=dataset.columns)
    for index, row in dataset.iterrows():
        if not np.isnan(row["Esami del sangue"]):
            till_blood_tests_dataset = till_blood_tests_dataset.append(row, ignore_index=True)
    till_blood_tests_dataset.to_csv("../Datasets/" + till_blood_tests_dataset_file, index=False, na_rep=np.nan)


def learning_mode(dataset):
    print("to do")


def classifying_mode(dataset):
    print("to do")


till_survey_dataset_file = "till_survey_virtual_dataset.csv"
till_poct_dataset_file = "till_poct_virtual_dataset.csv"
till_blood_tests_dataset_file = "till_blood_tests_virtual_dataset.csv"
split_dataset(till_survey_dataset_file, till_poct_dataset_file, till_blood_tests_dataset_file)
