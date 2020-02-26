import pandas as pd


resource_path = "Datasets/"
dataset_file = "dataset_virtuale.csv"
dataset = pd.read_csv(resource_path + dataset_file)


def split_dataset():
    till_survey_dataset = pd.DataFrame()
    till_survey_dataset["Anemia"] = dataset["Anemia"]
    till_survey_dataset["Osteopenia"] = dataset["Osteopenia"]
    till_survey_dataset["Diarrea Cronica"] = dataset["Diarrea Cronica"]
    till_survey_dataset["Mancata Crescita"] = dataset["Mancata Crescita"]
    till_survey_dataset["Disturbi Genetici"] = dataset["Disturbi Genetici"]
    till_survey_dataset["Madre Celiaca"] = dataset["Madre Celiaca"]
    till_poct_dataset = pd.DataFrame(till_survey_dataset)
    till_poct_dataset["POCT"] = dataset["POCT"]
    till_blood_tests_dataset = pd.DataFrame(dataset).dropna(subset=["Esami del sangue"])
    return till_survey_dataset, till_poct_dataset, till_blood_tests_dataset


till_survey_dataset, till_poct_dataset, till_blood_tests_dataset = split_dataset()
