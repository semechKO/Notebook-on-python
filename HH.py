# coding=utf8
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

search_select_xpath = "html/body/div[1]/div[1]/div/div/div/div[2]/form[1]/div/div[2]/select"
search_company_select_xpath = "html/body/div[1]/div[1]/div/div/div/div[2]/form[1]/div/div[2]/select/option[3]"
search_input_field_xpath = "html/body/div[1]/div[1]/div/div/div/div[2]/form[3]/div/div[1]/input"
find_btn_xpath = "//*[contains(text(),'Найти')]"
vacancy_areas =['Информационные технологии, интернет, телеком', 'Бухгалтерия, управленческий учет, финансы предприятия',
                    'Маркетинг, реклама, PR', 'Банки, инвестиции, лизинг', 'Искусство, развлечения, масс-медиа']


# Method searches for company
def searchForCompany(driver, search_input):
    driver.find_element_by_xpath(search_select_xpath).click()
    driver.find_element_by_xpath(search_company_select_xpath).click()
    driver.find_element_by_xpath(search_input_field_xpath).send_keys(search_input)
    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath(find_btn_xpath), 700, 50).click().perform()


# Method checks if searched company is existing
def checkExictenceOfCompany(driver, company_name):
    company_name_xpath = "//*[contains(text(),'" + company_name + "')]"
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, company_name_xpath)))
        return True
    except TimeoutException:
        return False


# Method goes to company page if it exists
def goToCompanyPage(driver, company_name):
    searchForCompany(driver, company_name)
    if checkExictenceOfCompany(driver, company_name):
        driver.find_element_by_xpath("//*[contains(text(),'" + company_name + "')]").click()


# Method returns number of vacancies
def numberOfVacancies(driver):
    vacancies = re.findall(r'\d+', driver.find_element_by_class_name("b-employerpage-vacancies-region").text)
    try:
        return vacancies[0]
    except IndexError:
        return vacancies


# Method searches for given vacancy on the company page
def findVacancyInThisRegion(driver, vacancy_name):
    for area in vacancy_areas:
        area_xpath = driver.find_element_by_xpath("//*[contains(text(),'" + area + "')]")
        try:
            driver.execute_script("arguments[0].scrollIntoView();", area_xpath)
            ActionChains(driver).move_to_element(area_xpath).click().perform()
        except NoSuchElementException:
            print ("It isn't company page")
            return False
    try:
        driver.find_element_by_xpath("//*[contains(text(),'" + vacancy_name + "')]")
        return True
    except NoSuchElementException:
        return False
