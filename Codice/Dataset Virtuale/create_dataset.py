import numpy
import csv
import constant
import dataset_row


def generate_negative_patient():
    patient = dataset_row.patient()
    generate_test_for_negative_patient(patient)
    generate_POCT_for_negative_patient(patient)
    if not (patient.is_test_negative() and patient.is_POCT_negative()):
        if patient.POCT is constant.INCONCLUSIVE_POCT:
            patient.set_total_IGA_below_threshold_for_negative_patient()
            patient.set_TTG_igg_for_negative_patient()
            patient.set_blood_tests_from_TTG_igg()
        else:
            # patient.POCT is constant.NEGATIVE_POCT
            patient.set_total_IGA_above_threshold_for_negative_patient()
            patient.set_TTG_iga_for_negative_patient()
            patient.set_blood_tests_from_TTG_iga()
        if patient.blood_tests == constant.POSITIVE_BLOOD_TEST:
            patient.biopsy = constant.NEGATIVE_BIOPSY
    return patient


def generate_test_for_negative_patient(patient):
    anemia_random_number = numpy.random.randint(1, 5)
    patient.anemia = test_checker(anemia_random_number)
    osteopenia_random_number = numpy.random.randint(1, 4)
    patient.osteopenia = test_checker(osteopenia_random_number)
    chronic_diarrhea_random_number = numpy.random.randint(1, 21)
    patient.chronic_diarrhea = test_checker(chronic_diarrhea_random_number)
    growth_failure_random_number = numpy.random.randint(1, 141)
    patient.growth_failure = test_checker(growth_failure_random_number)
    genetic_disorders_random_number = numpy.random.randint(1, 1001)
    patient.genetic_disorders = test_checker(genetic_disorders_random_number)
    celiac_mother_random_number = numpy.random.randint(1, 101)
    patient.celiac_mother = test_checker(celiac_mother_random_number)


def generate_POCT_for_negative_patient(patient):
    poct_random_number = numpy.random.randint(1, 601)
    # positive POCT is highly unlikely
    if poct_random_number is 1:
        patient.POCT = constant.INCONCLUSIVE_POCT
    else:
        patient.POCT = constant.NEGATIVE_POCT


def generate_positive_patient():
    patient = dataset_row.patient()
    generate_test_for_positive_patient(patient)
    generate_POCT_for_positive_patient(patient)
    if patient.POCT is constant.INCONCLUSIVE_POCT:
        patient.set_total_IGA_below_threshold_for_positive_patient()
        patient.set_TTG_igg_for_positive_patient()
        patient.set_blood_tests_from_TTG_igg()
    else:
        patient.set_total_IGA_above_threshold_for_positive_patient()
        if patient.POCT is constant.POSITIVE_POCT:
            patient.set_TTG_iga_for_positive_patient()
        if patient.POCT is constant.NEGATIVE_POCT:
            patient.set_TTG_iga_for_negative_patient()
        patient.set_blood_tests_from_TTG_iga()
    patient.biopsy = constant.POSITIVE_BIOPSY
    return patient


def generate_test_for_positive_patient(patient):
    anemia_random_number = numpy.random.randint(1, 3)
    patient.anemia = test_checker(anemia_random_number)
    osteopenia_random_number = numpy.random.randint(1, 6)
    if osteopenia_random_number < 3:
        patient.osteopenia = constant.POSITIVE
    else:
        patient.osteopenia = constant.NEGATIVE
    chronic_diarrhea_random_number = numpy.random.randint(1, 4)
    patient.chronic_diarrhea = test_checker(chronic_diarrhea_random_number)
    growth_failure_random_number = numpy.random.randint(1, 6)
    patient.growth_failure = test_checker(growth_failure_random_number)
    genetic_disorders_random_number = numpy.random.randint(1, 21)
    patient.genetic_disorders = test_checker(genetic_disorders_random_number)
    celiac_mother_random_number = numpy.random.randint(1, 19)
    patient.celiac_mother = test_checker(celiac_mother_random_number)


def generate_POCT_for_positive_patient(patient):
    poct_random_number = numpy.random.randint(1, 601)
    if poct_random_number is 1:
        patient.POCT = constant.INCONCLUSIVE_POCT
    elif patient.is_test_negative():
        patient.POCT = constant.POSITIVE_POCT
    else:
        poct_random_number = numpy.random.randint(1, 11)
        if poct_random_number is 1:
            patient.POCT = constant.NEGATIVE_POCT
        else:
            patient.POCT = constant.POSITIVE_POCT


def test_checker(num):
    if num is 1:
        return constant.POSITIVE
    else:
        return constant.NEGATIVE


def create_dataset():
    columns = ["Anemia", "Osteopenia", "Diarrea Cronica", "Mancata Crescita", "Disturbi Genetici", "Madre Celiaca",
               "POCT", "IGA totali", "TTG igg", "TTG_iga", "Esami del sangue", "Biopsia"]
    with open("dataset.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(columns)
        for _ in range(0, 10000):
            writer.writerow(generate_positive_patient().values())
            mu, sigma = 100.00, 2.00
            num_negative_patients = int(numpy.round(numpy.random.normal(mu, sigma)))
            for _ in range(0, num_negative_patients):
                writer.writerow(generate_negative_patient().values())


if __name__ == '__main__':
    create_dataset()
