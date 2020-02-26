import numpy as np
import scipy.stats
import constant


class patient:
    def __init__(self):
        self.anemia = np.NaN
        self.osteopenia = np.NaN
        self.chronic_diarrhea = np.NaN
        self.growth_failure = np.NaN
        self.genetic_disorders = np.NaN
        self.celiac_mother = np.NaN
        self.POCT = np.NaN
        self.total_IGA = np.NaN
        self.TTG_igg = np.NaN
        self.TTG_iga = np.NaN
        self.blood_tests = np.NaN
        #self.biopsy = np.NaN
        self.Class = np.NaN

    def is_POCT_negative(self):
        if self.POCT is constant.NEGATIVE_POCT:
            return True
        else:
            return False

    def is_test_negative(self):
        if (self.anemia is 0) and (self.osteopenia is 0) and (self.chronic_diarrhea is 0) and \
                (self.growth_failure is 0) and (self.genetic_disorders is 0) and (self.celiac_mother is 0):
            return True
        else:
            return False

    def set_total_IGA_above_threshold_for_negative_patient(self):
        mu, sigma = 0.7, 2.00
        self.total_IGA = np.random.normal(mu, sigma)
        if self.total_IGA < constant.IGA_THRESHOLD:
            self.total_IGA = constant.IGA_THRESHOLD
        self.total_IGA = round(self.total_IGA, 2)

    def set_total_IGA_above_threshold_for_positive_patient(self):
        mu, sigma = 0.8, 2.00
        self.total_IGA = np.random.normal(mu, sigma)
        if self.total_IGA < constant.IGA_THRESHOLD:
            self.total_IGA = constant.IGA_THRESHOLD
        self.total_IGA = round(self.total_IGA, 2)

    def set_total_IGA_below_threshold_for_negative_patient(self):
        self.total_IGA = np.random.uniform(0, 0.25)
        self.total_IGA = round(self.total_IGA, 2)

    def set_total_IGA_below_threshold_for_positive_patient(self):
        mu, sigma = 0.125, 1.00
        self.total_IGA = np.random.normal(mu, sigma)
        if self.total_IGA < 0:
            self.total_IGA = 0.00
        self.total_IGA = round(self.total_IGA, 2)

    def set_TTG_igg_for_negative_patient(self):
        mu, sigma = 2.00, 2.00
        self.TTG_igg = np.random.normal(mu, sigma)
        if self.TTG_igg < 0:
            self.TTG_igg = 0.00
        self.TTG_igg = round(self.TTG_igg, 2)

    def set_TTG_igg_for_positive_patient(self):
        mu, sigma = 14.00, 2.00
        self.TTG_igg = np.random.normal(mu, sigma)
        if self.TTG_igg < 0:
            self.TTG_igg = 0.00
        self.TTG_igg = round(self.TTG_igg, 2)

    def set_TTG_iga_for_negative_patient(self):
        mu, sigma = 4.50, 2.00
        self.TTG_iga = np.random.normal(mu, sigma)
        if self.TTG_iga < 0:
            self.TTG_iga = 0.00
        self.TTG_iga = round(self.TTG_iga, 2)

    def set_TTG_iga_for_positive_patient(self):
        a, mu, sigma = 0.50, 24.00, 2.00
        self.TTG_iga = scipy.stats.skewnorm.rvs(a, mu, sigma)
        if self.TTG_iga < 0:
            self.TTG_iga = 0.00
        self.TTG_iga = round(self.TTG_iga, 2)

    def set_blood_tests_from_TTG_igg(self):
        if self.TTG_igg < constant.TTG_IGG_THRESHOLD:
            self.blood_tests = constant.NEGATIVE_BLOOD_TEST
        else:
            self.blood_tests = constant.POSITIVE_BLOOD_TEST

    def set_blood_tests_from_TTG_iga(self):
        if self.TTG_iga < constant.TTG_IGA_NEGATIVE_THRESHOLD:
            self.blood_tests = constant.NEGATIVE_BLOOD_TEST
        elif self.TTG_iga < constant.TTG_IGA_POSITIVE_THRESHOLD:
            # borderline value
            self.blood_tests = constant.NEGATIVE_BLOOD_TEST
        else:
            self.blood_tests = constant.POSITIVE_BLOOD_TEST

    def values(self):
        values = list()
        values.append(self.anemia)
        values.append(self.osteopenia)
        values.append(self.chronic_diarrhea)
        values.append(self.growth_failure)
        values.append(self.genetic_disorders)
        values.append(self.celiac_mother)
        values.append(self.POCT)
        values.append(self.total_IGA)
        values.append(self.TTG_igg)
        values.append(self.TTG_iga)
        values.append(self.blood_tests)
        #values.append(self.biopsy)
        values.append(self.Class)
        return values
