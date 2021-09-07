from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from Scripts import constants
import csv

def configurations():
    global driver
    global options
    
    options = Options()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=options, executable_path="ChromeDriver/chromedriver.exe")

class Csv_io:
    def __init__(self, filename, mode, newline):
        self.filename = filename
        self.mode = mode
        self.newline = newline
        
        self.openfile()
        self.writer_setup()
        
    def openfile(self):
        self.file_to_write = open(self.filename, mode = self.mode, newline = self.newline)
    
    def writer_setup(self):
        self.csv_writer = csv.writer(self.file_to_write)
        
    def insert_row(self, info):
        self.csv_writer.writerow(info)

class Webpage:
    def visit(self, url):
        driver.get(url)
    
    def click_with_css_selector(self, css_selector):
        driver.find_element_by_css_selector(css_selector).click()
    
    def grab_element_with_css_selector(self, css_selector):
        return driver.find_element_by_css_selector(css_selector)
    
    def grab_elements_with_css_selector(self, css_selector):
        return driver.find_elements_by_css_selector(css_selector)
    
    def type_value_with_css_selector(self, css_selector, keys):
        driver.find_element_by_css_selector(css_selector).send_keys(keys)
        
    def grab_text_with_css_selector(self, css_selector):
        return driver.find_element_by_css_selector(css_selector).text
        
    def get_url(self):
        return driver.current_url

class Browser:
    def end_session(self):
        driver.quit()
    
    def go_back(self):
        driver.back()
        
    def wait(self, duration):
        driver.implicitly_wait(duration)
        
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
def log(text):
    print(text)
    
def main():
    configurations()
    
    user = User(constants.username, constants.password)
    
    csv_io = Csv_io('OutputFolder/dataset.csv', 'a', '')
    
    webpage = Webpage()
    
    browser = Browser()
    
    browser.wait(5)
    
    webpage.visit("https://www.linkedin.com/login")
    
    webpage.type_value_with_css_selector("input[id='username']", user.username) 
    webpage.type_value_with_css_selector("input[id='password']", user.password)
    webpage.click_with_css_selector("button[type='submit']")
    
    for keyword in list(constants.commaseparated.split(';')):
        for page in range(1, int(constants.upto_page) + 1):
            browser.wait(2)
            
            link = "https://www.linkedin.com/search/results/people/?keywords=" + keyword + "&origin=CLUSTER_EXPANSION&page=" + str(page)
            webpage.visit(link)
            
            list_of_cards = list(webpage.grab_elements_with_css_selector("li[class='reusable-search__result-container ']"))
            
            log(f"a total of {len(list_of_cards)} Connections found on page {page} for {keyword}")
            
            for i in range(1, len(list_of_cards) + 1):
                browser.wait(2)
                
                try:                    
                    button_on_card = webpage.grab_element_with_css_selector(f"li[class= 'reusable-search__result-container ']:nth-child({i}) button").is_enabled()
            
                    button_text = webpage.grab_text_with_css_selector(f"li[class= 'reusable-search__result-container ']:nth-child({i}) button span")
                    
                    if button_on_card == True and button_text == 'Connect':
                        webpage.click_with_css_selector(f"li[class= 'reusable-search__result-container ']:nth-child({i}) span a span span")
                        
                        browser.wait(2)
                        
                        webpage.click_with_css_selector("button[data-control-name='connect']")
                        
                        browser.wait(2)
                        
                        webpage.click_with_css_selector("button[aria-label='Send now']")
                        
                        name_grab = webpage.grab_text_with_css_selector("h1")
                        
                        description1 = webpage.grab_text_with_css_selector("div[class= 'text-body-medium break-words']")
                        
                        description2 = webpage.grab_text_with_css_selector("span[class = 'text-body-small inline t-black--light break-words']")
                        
                        link_to_profile = webpage.get_url()
                        
                        browser.wait(2)
                        
                        log(f"{constants.Bcolors.WARNING}{name_grab} who is {description1} at {description2} for profile {link_to_profile}{constants.Bcolors.ENDC}")
                        
                        info = [name_grab, description1, description2, link_to_profile]
                        
                        csv_io.insert_row(info)
                        
                        browser.wait(2)
                        
                    webpage.visit(link)
                    
                    browser.wait(2)
                
                except NoSuchElementException:
                    pass
                except Exception as e:
                    log(e)
                    
        log(f"{constants.Bcolors.UNDERLINE} All New Connection's data appended to dataset.csv {constants.Bcolors.ENDC}")
        
        browser.end_session()
        
        csv_io.insert_row(["---------","----------","----------","-------------"])


