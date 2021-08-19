import time
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import openpyxl_operation
import constants
from graphical_script import guibuild


def selenium_function(sheet, book, filename):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")
    driver.implicitly_wait(5)
    # opening website
    driver.get("https://www.linkedin.com/login")
    # filling username and pass with const and pressing login

    driver.find_element_by_css_selector("input[id= 'username']").send_keys(constants.username)
    driver.find_element_by_css_selector("input[id= 'password']").send_keys(constants.password)
    driver.find_element_by_css_selector("button[type= 'submit']").click()

    for keyword in constants.list_of_searching_text:
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

                        max_rows = sheet.max_row
                        sheet.cell(row=max_rows + 1, column=1).value = name_grab
                        sheet.cell(row=max_rows + 1, column=2).value = description1
                        sheet.cell(row=max_rows + 1, column=3).value = description2
                        sheet.cell(row=max_rows + 1, column=4).value = link_to_profile
                        time.sleep(2)
                    driver.get(link)
                    time.sleep(2)
                except NoSuchElementException:
                    i=i=1
                except Exception as e:
                    print(e)
                    i=i+1
    now = str(datetime.now().strftime("%H")) + "H" + str(datetime.now().strftime("%M")) + "M" + str(
        datetime.now().strftime("%S") + "S")

    book.save(f"Res of {filename} at {now}.xlsx")
    print(f"{constants.Bcolors.UNDERLINE} See excel file on the same dir {filename} {constants.Bcolors.ENDC}")
    driver.quit()


if __name__ == '__main__':
    guibuild()



