import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import schedule
import time

# options is used to save user-data from the previous session, so we don't need to scan the QR code everytime
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=./BrowserAutomation/")
driver = webdriver


def send(message):
    inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
    input_box = driver.find_element_by_xpath(inp_xpath)
    time.sleep(2)
    input_box.send_keys(message + Keys.ENTER)
    time.sleep(2)


def session(contact, message, scheduleTimeValue, popup):
    global driver
    try:
        driver = webdriver.Chrome(executable_path='./chromedriver.exe',
                          options=options)
    except selenium.common.exceptions.WebDriverException:
        popup.config(text="Make sure correct version of chromedriver is downloaded and chromedriver.exe it is present in the current directory")


    driver.find_element_by_xpath("//body").click()

    driver.get("http://web.whatsapp.com")
    time.sleep(10)

    # find search box
    input_xpath_search = '//*[@id="side"]/div[1]/div/label/div/div[2]'
    input_box_search = WebDriverWait(driver, 50).until(
        lambda driver: driver.find_element_by_xpath(input_xpath_search))
    input_box_search.click()
    time.sleep(2)

    # type contact
    input_box_search.send_keys(contact)
    time.sleep(2)

    # tabs to the first item in the list
    input_box_search.send_keys(Keys.TAB)
    input_box_search.send_keys(Keys.ENTER)

    # schedule
    schedule.every().day.at(scheduleTimeValue).do(send, message)
    while True:
        schedule.run_pending()
        time.sleep(1)


# cancels the reminder and closes the browser
def close():
    global driver
    driver.quit()