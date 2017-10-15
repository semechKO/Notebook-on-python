import unittest
from selenium import webdriver
from Utils import json_load, loggingGetter
from HH import searchForCompany, checkExictenceOfCompany, goToCompanyPage, numberOfVacancies, findVacancyInThisRegion


# Class contains tests for HH site
class HeadHunterSearchTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger = loggingGetter()
        logger.info("SET UP STARTED...")
        data = json_load("json_ex.json")
        cls.user = data["HH"]["username"]
        cls.password = data["HH"]["password"]
        cls.company = data["HH"]["company"]
        cls.search = data["HH"]["search_input"]
        cls.site = data["HH"]["site"]
        cls.vacancy = data["HH"]['vacancy']
        cls.driver = webdriver.Chrome()
        logger.info("SET UP FINISHED")

    def setUp(cls):
        cls.driver.get(cls.site)

    # Method checks if company can be found by given search input.
    def test_NCT_search(cls):
        searchForCompany(cls.driver, cls.search)
        cls.assertTrue(checkExictenceOfCompany(cls.driver, cls.company),
                       "Company with given search input wasn't found.")

    # Method checks if company has vacancies.
    def test_numberOfVacancies(cls):
        goToCompanyPage(cls.driver, cls.company)
        # print numberOfVacancies(cls.driver) - use if you want to get number
        cls.assertTrue(numberOfVacancies(cls.driver), "Company doesn't have vacancies.")

    # Method checks for given vacancy in this region
    def test_findVacancyInThisRegion(cls):
        goToCompanyPage(cls.driver, cls.company)
        cls.assertTrue(findVacancyInThisRegion(cls.driver, cls.vacancy),
                       "Company doesn't have given vacancy in this region.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == '__main__':
    unittest.main()
