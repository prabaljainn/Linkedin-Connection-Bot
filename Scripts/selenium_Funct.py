import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from Scripts import constants
import csv

file_to_write = open('OutputFolder/dataset.csv',mode= 'a',newline='')
csv_writer= csv.writer(file_to_write)



def selenium_function():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options, executable_path="ChromeDriver/chromedriver.exe")
    driver.implicitly_wait(5)
    # opening website
    driver.get("https://www.linkedin.com/login")
    # filling username and pass with const and pressing login

    driver.find_element_by_css_selector("input[id= 'username']").send_keys(constants.username)
    driver.find_element_by_css_selector("input[id= 'password']").send_keys(constants.password)
    driver.find_element_by_css_selector("button[type= 'submit']").click()

    for keyword in list(constants.commaseparated.split(";")):
        for page in range(1, int(constants.upto_page) + 1):
            link = "https://www.linkedin.com/search/results/people/?keywords=" + keyword + "&origin=CLUSTER_EXPANSION&page=" + str(
                page)
            time.sleep(2)
            driver.get(link)
            list_of_cards = driver.find_elements_by_css_selector("li[class= 'reusable-search__result-container ']")
            print(f"a total of {len(list_of_cards)} Connections found on page {page} for {keyword} ")
            for i in range(1, len(list_of_cards) + 1):
                time.sleep(2)
                try:
                    name_container_with_link = driver.find_element_by_css_selector(
                        f"li[class= 'reusable-search__result-container ']:nth-child({i}) span a span span")
                    button_on_card = driver.find_element_by_css_selector(
                        f"li[class= 'reusable-search__result-container ']:nth-child({i}) button").is_enabled()
                    button_on_card2 = driver.find_element_by_css_selector(
                        f"li[class= 'reusable-search__result-container ']:nth-child({i}) button span")
                    if button_on_card == True and button_on_card2.text == 'Connect':
                        name_container_with_link.click()
                        time.sleep(2)
                        connect_button = driver.find_element_by_css_selector("button[data-control-name='connect']")
                        time.sleep(2)
                        connect_button.click()
                        time.sleep(2)
                        connect_last = driver.find_element_by_css_selector("button[aria-label='Send now']")
                        time.sleep(1)
                        connect_last.click()
                        name_grab = driver.find_element_by_tag_name("h1").text
                        description1 = driver.find_element_by_css_selector(
                            "div[class= 'text-body-medium break-words']").text
                        description2 = driver.find_element_by_css_selector(
                            "span[class = 'text-body-small inline t-black--light break-words']").text
                        link_to_profile = str(driver.current_url)
                        time.sleep(2)
                        print(
                            f"{constants.Bcolors.WARNING}{name_grab} who is {description1} at {description2} for profile {link_to_profile}{constants.Bcolors.ENDC}")
                        info_insert =[name_grab,description1,description2,link_to_profile]
                        csv_writer.writerow(info_insert)
                        time.sleep(2)
                    driver.get(link)
                    time.sleep(2)
                except NoSuchElementException:
                    pass
                except Exception as e:
                    print(e)
                    pass
    print(f"{constants.Bcolors.UNDERLINE} All New Connection's data appended to dataset.csv {constants.Bcolors.ENDC}")
    driver.quit()
    csv_writer.writerow(["---------","----------","----------","-------------"])




