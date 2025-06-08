# importing the required modules
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from . import constants
import csv
import time
import os
import logging
import sys
from datetime import datetime

# Configure logging
def setup_logging():
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Console handler with simple format
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    
    # Add handler to root logger
    root_logger.addHandler(console_handler)
    
    # Create logger for this module
    logger = logging.getLogger(__name__)
    return logger

# Initialize logger
logger = setup_logging()

# Redirect print to logger
class PrintLogger:
    def __init__(self, logger):
        self.logger = logger
        self.stdout = sys.stdout
        sys.stdout = self

    def write(self, message):
        if message.strip():  # Only log non-empty messages
            self.logger.info(message.strip())
        self.stdout.write(message)

    def flush(self):
        self.stdout.flush()

# Redirect print statements to logger
print_logger = PrintLogger(logger)

# Update the log function to use the logger
def log(text):
    logger.info(text)

# setup


def configurations():
    global driver
    global options

    options = Options()
    # Basic options
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Disable GPU and WebGL to avoid warnings
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-webgl")
    options.add_argument("--disable-webgl2")
    
    # Additional stability options
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Add user agent to avoid detection
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Add additional options for stability
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    
    # Add options to handle cookies and sessions
    options.add_argument("--enable-cookies")
    options.add_argument("--enable-local-storage")
    options.add_argument("--enable-session-storage")
    
    # Create a new Chrome service with error handling
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.common.exceptions import WebDriverException
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            # Set page load timeout
            driver.set_page_load_timeout(60)  # Increased timeout
            # Set script timeout
            driver.set_script_timeout(60)  # Increased timeout
            break
        except WebDriverException as e:
            retry_count += 1
            if retry_count == max_retries:
                raise Exception(f"Failed to initialize Chrome driver after {max_retries} attempts: {str(e)}")
            time.sleep(2)  # Wait before retrying


# this class deals with the CSV file operations like opening the file, setting up the writer, inserting new row, etc.
class Csv_io:
    def __init__(self, filename, mode, newline):
        self.filename = filename
        self.mode = mode
        self.newline = newline

        self.openfile()
        self.writer_setup()

    # opens file
    def openfile(self):
        self.file_to_write = open(
            self.filename, mode=self.mode, newline=self.newline)

    # initialises the writer object
    def writer_setup(self):
        self.csv_writer = csv.writer(self.file_to_write)

    # inserts a new row into the CSV file
    def insert_row(self, info):
        self.csv_writer.writerow(info)

    def __str__(self):
        return 'this class deals with the CSV file operations'

# this class deals with the DOM operations like grabbing the elements using selectors, clicking on elements, sending text to elements, etc.


class Webpage:
    # opens the given url
    def visit(self, url):
        driver.get(url)

    def click_with_xpath_selector(self, xpath_selector):
        driver.find_element(By.XPATH, xpath_selector).click()
    # clicks the element selected using CSS Selector

    def click_with_css_selector(self, css_selector):
        driver.find_element(By.CSS_SELECTOR, css_selector).click()

    # gets the element selected using CSS Selector
    def grab_element_with_css_selector(self, css_selector):
        return driver.find_element(By.CSS_SELECTOR, css_selector)

    # gets the elements* selected using CSS Selector
    def grab_elements_with_css_selector(self, css_selector):
        return driver.find_elements(By.CSS_SELECTOR, css_selector)

    # sends the entered text to the element selected using CSS Selector
    def type_value_with_css_selector(self, css_selector, keys):
        driver.find_element(By.CSS_SELECTOR, css_selector).send_keys(keys)

    # gets the text from the element selected using CSS Selector
    def grab_text_with_css_selector(self, css_selector):
        return driver.find_element(By.CSS_SELECTOR, css_selector).text

    # returns the url of the current page
    def get_url(self):
        return driver.current_url

# this class deals with the browser operations like ending the session, going back to previous page, wait, etc.


class Browser:
    # end the current session
    def end_session(self):
        driver.quit()

    # go back to previous page
    def go_back(self):
        driver.back()

    # wait/sleep for given time
    def wait(self, duration):
        driver.implicitly_wait(duration)

# this is the user class


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# main function


def main():
    try:
        configurations()

        user = User(constants.username, constants.password)

        # Create OutputFolder if it doesn't exist
        if not os.path.exists('OutputFolder'):
            os.makedirs('OutputFolder')

        csv_io = Csv_io('OutputFolder/dataset.csv', 'a', '')

        webpage = Webpage()
        browser = Browser()

        browser.wait(10)  # Increased initial wait

        try:
            # First visit LinkedIn homepage to set initial cookies
            webpage.visit("https://www.linkedin.com")
            time.sleep(1)
            
            # Then go to login page
            webpage.visit("https://www.linkedin.com/login")
            time.sleep(3)  # Increased wait after page load
        except Exception as e:
            log(f"Error accessing LinkedIn login page: {str(e)}")
            raise

        try:
            # Wait for username field and enter credentials
            username_field = webpage.grab_element_with_css_selector("input[id='username']")
            username_field.clear()
            username_field.send_keys(user.username)
            time.sleep(2)

            # Wait for password field and enter credentials
            password_field = webpage.grab_element_with_css_selector("input[id='password']")
            password_field.clear()
            password_field.send_keys(user.password)
            time.sleep(2)

            # Find and click submit button
            submit_button = webpage.grab_element_with_css_selector("button[type='submit']")
            submit_button.click()
            time.sleep(3)  # Wait after login attempt

            # Enhanced security verification handling
            try:
                # Check for various security verification scenarios
                security_indicators = [
                    "div.challenge-dialog",
                    "div.security-verification",
                    "div.verification-code-form",
                    "div.challenge-container",
                    "div.security-verification__container",
                    "div[data-test-id='challenge-dialog']",
                    "div[data-test-id='security-verification']"
                ]

                verification_detected = False
                for indicator in security_indicators:
                    try:
                        if driver.find_element(By.CSS_SELECTOR, indicator).is_displayed():
                            verification_detected = True
                            logger.warning("Security verification detected. Waiting for manual completion...")
                            break
                    except:
                        continue

                if verification_detected:
                    # Wait for verification to complete
                    max_wait_time = 180  # 3 minutes maximum wait
                    start_time = time.time()
                    
                    while time.time() - start_time < max_wait_time:
                        try:
                            # Check if we're back to the main feed
                            feed = driver.find_element(By.CSS_SELECTOR, "div.feed-shared-update-v2")
                            if feed.is_displayed():
                                logger.info("Security verification completed successfully")
                                break
                        except:
                            # Check if verification is still present
                            try:
                                for indicator in security_indicators:
                                    if driver.find_element(By.CSS_SELECTOR, indicator).is_displayed():
                                        time.sleep(3)  # Wait before checking again
                                        break
                            except:
                                # If no verification elements found, might be completed
                                try:
                                    feed = driver.find_element(By.CSS_SELECTOR, "div.feed-shared-update-v2")
                                    if feed.is_displayed():
                                        logger.info("Security verification completed successfully")
                                        break
                                except:
                                    pass
                        
                    
                    if time.time() - start_time >= max_wait_time:
                        raise Exception("Security verification timeout - please complete verification manually")

                # Final verification of successful login
                try:
                    feed = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-shared-update-v2"))
                    )
                    if not feed.is_displayed():
                        raise Exception("Login verification failed - feed not found or not visible")
                    logger.info("Login successful - feed is visible")
                except Exception as e:
                    logger.error(f"Login verification failed: {str(e)}")
                    raise

            except Exception as e:
                logger.error(f"Error during login verification: {str(e)}")
                raise

        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            raise

        for keyword in list(constants.commaseparated.split(';')):
            for page in range(1, int(constants.upto_page) + 1):
                try:
                
                    time.sleep(2)  # Increased wait between searches

                    # Get list of locations
                    locations = []
                    if hasattr(constants, 'location') and constants.location:
                        locations = [loc.strip() for loc in constants.location.split(';')]
                        locations = [loc for loc in locations if loc]  # Remove empty locations
                    
                    # If no locations specified, use empty list to process page once without location filter
                    if not locations:
                        locations = [None]

                    # Process page for each location
                    for location in locations:
                        location_applied = False
                        attempts = 0
                        max_attempts = 3
                        while not location_applied and attempts < max_attempts:
                            attempts += 1
                            try:
                                # First visit the search URL
                                link = f"https://www.linkedin.com/search/results/people/?keywords={keyword}&origin=GLOBAL_SEARCH_HEADER&page={page}"
                                webpage.visit(link)
                                time.sleep(4)  # Wait for page to load
                                
                                log(f"Attempt {attempts} to apply location filter '{location}'")
                                # Click the Locations filter button
                                location_button = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.ID, "searchFilter_geoUrn"))
                                )
                                driver.execute_script("arguments[0].scrollIntoView(true);", location_button)
                                time.sleep(1)
                                location_button.click()
                                time.sleep(2)

                                # Wait for the location dropdown to appear and enter location
                                location_input = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='Add a location']"))
                                )
                                driver.execute_script("arguments[0].scrollIntoView(true);", location_input)
                                time.sleep(1)
                                location_input.clear()
                                location_input.send_keys(location)
                                time.sleep(3) # Wait for suggestions to appear

                                #keyboard navigation
                                location_input.send_keys(Keys.DOWN)
                                time.sleep(1)
                                location_input.send_keys(Keys.ENTER)
                                time.sleep(2)
                                    

                                # Click the Show results button
                                try:
                                    time.sleep(2) # Increased pause before waiting for the button
                                    
                                    # Try multiple selectors in order of preference
                                    show_results_selectors = [
                                        # 1. CSS selector: 5th <li> of type with button as 2nd child, with specific aria-label
                                        "li.search-reusables__primary-filter:nth-of-type(5) button.artdeco-button--primary:nth-child(2)[aria-label='Apply current filter to show results']",

                                        # 2. XPath: 4th <li> with specific class, then find 2nd <button> child with desired text
                                        "(//li[contains(@class, 'search-reusables__primary-filter')])[4]//button[position()=2 and contains(@class, 'artdeco-button--primary') and .//span[contains(text(), 'Show results')]]",

                                        # 3. XPath: similar to #2, but with normalized text match
                                        "(//li[contains(@class, 'search-reusables__primary-filter')])[4]//button[position()=2 and contains(@class, 'artdeco-button--primary') and .//span[normalize-space(.)='Show results']]"
                                    ]


                                    
                                    show_results_button = None
                                    for selector in show_results_selectors:
                                        try:
                                            if selector.startswith("//"):
                                                # Use explicit wait for XPath
                                                show_results_button = WebDriverWait(driver, 2).until(
                                                    EC.presence_of_element_located((By.XPATH, selector))
                                                )
                                            else:
                                                # Use explicit wait for CSS
                                                show_results_button = WebDriverWait(driver, 2).until(
                                                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                                )
                                            
                                            # Additional check for element visibility and clickability
                                            if show_results_button and show_results_button.is_displayed() and show_results_button.is_enabled():
                                                # Try to scroll element into view
                                                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", show_results_button)
                                                time.sleep(1)
                                                break
                                        except Exception as e:
                                            log(f"Selector {selector} failed: {str(e)}")
                                            continue
                                    
                                    if not show_results_button:
                                        raise Exception("Could not find Show results button with any selector")
                                    
                                    # Wait for button to be interactable and click
                                    try:
                              
                                        # Scroll button into view
                                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", show_results_button)
                                        time.sleep(1)
                                        
                                        # Try JavaScript click first
                                        try:
                                            driver.execute_script("arguments[0].click();", show_results_button)
                                        except:
                                            # Fallback to regular click
                                            show_results_button.click()
                                        
                                        # Wait for dropdown to disappear
                                        WebDriverWait(driver, 5).until(
                                            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div#hoverable-outlet-locations-filter-value>div.reusable-search-filters-trigger-dropdown__content"))
                                        )
                                        time.sleep(2)  # Wait for results to load
                                    except Exception as e:
                                        raise Exception(f"Failed to click Show results button: {str(e)}")
                                    
                                except Exception as e:
                                    raise Exception(f"Failed to find or click 'Show results' button: {str(e)}")

                                location_applied = True

                            except Exception as e:
                                log(f"Error during location filter application for '{location}': {str(e)}. Retrying...")
                                # Re-visit the search page to ensure a clean state for retry
                                link = f"https://www.linkedin.com/search/results/people/?keywords={keyword}&origin=GLOBAL_SEARCH_HEADER&page={page}"
                                webpage.visit(link)
                                time.sleep(4)
                                continue

                        if not location_applied:
                            log(f"{constants.Bcolors.FAIL}Failed to apply location filter for '{location}' after {max_attempts} attempts. Skipping this location.{constants.Bcolors.ENDC}")
                            continue

                    # Verify we're still logged in
                    try:
                        login_button = webpage.grab_element_with_css_selector("button[data-control-name='nav.login']")
                        if login_button:
                            log("Session expired, attempting to login again...")
                            raise Exception("Session expired")
                    except NoSuchElementException:
                        pass  # No login button found, we're still logged in

                    # Try multiple selectors for search results
                    list_of_cards = []
                    selectors = [
                        "li.SEqptLqWkqtDzWhauSoylugoMquJTSEaJfVZ",
                        "div.reusable-search__result-container",
                        "div.search-result__info",
                        "div.entity-result__item"
                    ]

                    for selector in selectors:
                        try:
                            elements = webpage.grab_elements_with_css_selector(selector)
                            if elements:
                                list_of_cards = list(elements)
                                log(f"Found results using selector: {selector}")
                                break
                        except Exception:
                            continue

                    location_str = f" for location '{location}'" if location else ""
                    log(f"a total of {len(list_of_cards)} Connections found on page {page} for {keyword}{location_str}")

                    # Process all contacts on the page
                    try:
                        for i in range(1, len(list_of_cards) + 1):
                            try:
                                time.sleep(3)  # Increased wait between cards

                                # Try multiple selectors for buttons
                                button = None
                                button_type = None
                                button_selectors = [
                                    f"li.SEqptLqWkqtDzWhauSoylugoMquJTSEaJfVZ:nth-child({i}) button.artdeco-button",
                                    f"div.reusable-search__result-container:nth-child({i}) button.artdeco-button",
                                    f"div.search-result__info:nth-child({i}) button.artdeco-button",
                                    f"div.entity-result__item:nth-child({i}) button.artdeco-button"
                                ]

                                for selector in button_selectors:
                                    try:
                                        temp_button = webpage.grab_element_with_css_selector(selector)
                                        if temp_button and temp_button.is_enabled():
                                            button_text = temp_button.text.strip()
                                            if 'Follow' in button_text:
                                                button = temp_button
                                                button_type = 'follow'
                                                break
                                            elif 'Connect' in button_text:
                                                button = temp_button
                                                button_type = 'connect'
                                                break
                                    except Exception:
                                        continue

                                if button:
                                    time.sleep(2)
                                    
                                    try:
                                        if button_type == 'connect':
                                            # For Connect buttons, click directly
                                            button.click()
                                            time.sleep(2)
                                            
                                            # Handle the connection modal
                                            try:
                                                # Try to find and click "Send without a note" button
                                                send_without_note_selectors = [
                                                    "button.artdeco-button--primary[aria-label='Send without a note']",
                                                    "button[aria-label='Send without a note']",
                                                    "button.artdeco-button--2.artdeco-button--primary"
                                                ]
                                                
                                                for selector in send_without_note_selectors:
                                                    try:
                                                        send_button = webpage.grab_element_with_css_selector(selector)
                                                        if send_button and send_button.is_enabled():
                                                            send_button.click()
                                                            time.sleep(2)
                                                            break
                                                    except Exception:
                                                        continue
                                            except Exception as e:
                                                log(f"Error handling connection modal: {str(e)}")
                                                continue
                                            
                                            # Get profile info from the card
                                            try:
                                                name_grab = webpage.grab_text_with_css_selector(
                                                    f"li.SEqptLqWkqtDzWhauSoylugoMquJTSEaJfVZ:nth-child({i}) span.entity-result__title-text a span span")
                                            except:
                                                try:
                                                    name_grab = webpage.grab_text_with_css_selector(
                                                        f"div.reusable-search__result-container:nth-child({i}) span.entity-result__title-text a span span")
                                                except:
                                                    name_grab = "N/A"

                                            try:
                                                description1 = webpage.grab_text_with_css_selector(
                                                    f"li.SEqptLqWkqtDzWhauSoylugoMquJTSEaJfVZ:nth-child({i}) div.aFjBrNZtAQJlsDdweGlZDZXrbSCaQplKaU")
                                            except:
                                                try:
                                                    description1 = webpage.grab_text_with_css_selector(
                                                        f"div.reusable-search__result-container:nth-child({i}) div.aFjBrNZtAQJlsDdweGlZDZXrbSCaQplKaU")
                                                except:
                                                    description1 = "N/A"

                                            try:
                                                description2 = webpage.grab_text_with_css_selector(
                                                    f"li.SEqptLqWkqtDzWhauSoylugoMquJTSEaJfVZ:nth-child({i}) div.AfYWBcJALseTYlgAgWShDEAOnbbteeRp")
                                            except:
                                                try:
                                                    description2 = webpage.grab_text_with_css_selector(
                                                        f"div.reusable-search__result-container:nth-child({i}) div.AfYWBcJALseTYlgAgWShDEAOnbbteeRp")
                                                except:
                                                    description2 = "N/A"

                                            try:
                                                link_element = webpage.grab_element_with_css_selector(
                                                    f"li.SEqptLqWkqtDzWhauSoylugoMquJTSEaJfVZ:nth-child({i}) a.zSvKgyodXUoGbhUhxSWpxUXaFuhWtTKexrM")
                                                if link_element:
                                                    link_to_profile = link_element.get_attribute('href')
                                                else:
                                                    link_to_profile = "N/A"
                                            except:
                                                try:
                                                    link_element = webpage.grab_element_with_css_selector(
                                                        f"div.reusable-search__result-container:nth-child({i}) a.zSvKgyodXUoGbhUhxSWpxUXaFuhWtTKexrM")
                                                    if link_element:
                                                        link_to_profile = link_element.get_attribute('href')
                                                    else:
                                                        link_to_profile = "N/A"
                                                except:
                                                    link_to_profile = "N/A"

                                            log(f"{constants.Bcolors.WARNING}{name_grab} who is {description1} at {description2} for profile {link_to_profile}{constants.Bcolors.ENDC}")

                                            info = [name_grab, description1,
                                                    description2, link_to_profile]

                                            csv_io.insert_row(info)
                                            time.sleep(2)

                                        elif button_type == 'follow':
                                            # For Follow buttons, we need to click the overflow menu first
                                            try:
                                                # Try to find and click the overflow menu button
                                                overflow_selectors = [
                                                    f"li.SEqptLqWkqtDzWhauSoylugoMquJTSEaJfVZ:nth-child({i}) button.artdeco-dropdown__trigger",
                                                    f"div.reusable-search__result-container:nth-child({i}) button.artdeco-dropdown__trigger",
                                                    f"div.search-result__info:nth-child({i}) button.artdeco-dropdown__trigger",
                                                    f"div.entity-result__item:nth-child({i}) button.artdeco-dropdown__trigger"
                                                ]

                                                overflow_button = None
                                                for selector in overflow_selectors:
                                                    try:
                                                        temp_button = webpage.grab_element_with_css_selector(selector)
                                                        if temp_button and temp_button.is_enabled():
                                                            overflow_button = temp_button
                                                            break
                                                    except Exception:
                                                        continue

                                                if overflow_button:
                                                    overflow_button.click()
                                                    time.sleep(2)

                                                    # Try to find and click the Connect option in the dropdown
                                                    connect_option_selectors = [
                                                        "div.artdeco-dropdown__item[aria-label*='Invite']",
                                                        "div.artdeco-dropdown__item[aria-label*='Connect']",
                                                        "div.artdeco-dropdown__item:has(svg[data-test-icon='connect-medium'])"
                                                    ]

                                                    connect_option = None
                                                    for selector in connect_option_selectors:
                                                        try:
                                                            temp_option = webpage.grab_element_with_css_selector(selector)
                                                            if temp_option and temp_option.is_enabled():
                                                                connect_option = temp_option
                                                                break
                                                        except Exception:
                                                            continue

                                                    if connect_option:
                                                        connect_option.click()
                                                        time.sleep(2)

                                                        # Handle the connection modal
                                                        try:
                                                            # Try to find and click "Send without a note" button
                                                            send_without_note_selectors = [
                                                                "button.artdeco-button--primary[aria-label='Send without a note']",
                                                                "button[aria-label='Send without a note']",
                                                                "button.artdeco-button--2.artdeco-button--primary"
                                                            ]
                                                            
                                                            for selector in send_without_note_selectors:
                                                                try:
                                                                    send_button = webpage.grab_element_with_css_selector(selector)
                                                                    if send_button and send_button.is_enabled():
                                                                        send_button.click()
                                                                        time.sleep(2)
                                                                        break
                                                                except Exception:
                                                                    continue
                                                        except Exception as e:
                                                            log(f"Error handling connection modal: {str(e)}")
                                                            continue

                                                        # Get profile info from the card
                                                        try:
                                                            name_grab = webpage.grab_text_with_css_selector(
                                                                f"li.SEqptLqWkqtDzWhauSoylugoMquJTSEaJfVZ:nth-child({i}) span.entity-result__title-text a span span")
                                                        except:
                                                            try:
                                                                name_grab = webpage.grab_text_with_css_selector(
                                                                    f"div.reusable-search__result-container:nth-child({i}) span.entity-result__title-text a span span")
                                                            except:
                                                                name_grab = "N/A"

                                                        try:
                                                            description1 = webpage.grab_text_with_css_selector(
                                                                f"li.SEqptLqWkqtDzWhauSoylugoMquJTSEaJfVZ:nth-child({i}) div.aFjBrNZtAQJlsDdweGlZDZXrbSCaQplKaU")
                                                            if description1 == "N/A":
                                                                description1 = webpage.grab_text_with_css_selector(
                                                                    f"div.reusable-search__result-container:nth-child({i}) div.aFjBrNZtAQJlsDdweGlZDZXrbSCaQplKaU")
                                                        except:
                                                            description1 = "N/A"

                                                        try:
                                                            description2 = webpage.grab_text_with_css_selector(
                                                                f"li.SEqptLqWkqtDzWhauSoylugoMquJTSEaJfVZ:nth-child({i}) div.AfYWBcJALseTYlgAgWShDEAOnbbteeRp")
                                                            if description2 == "N/A":
                                                                description2 = webpage.grab_text_with_css_selector(
                                                                    f"div.reusable-search__result-container:nth-child({i}) div.AfYWBcJALseTYlgAgWShDEAOnbbteeRp")
                                                        except:
                                                            description2 = "N/A"

                                                        try:
                                                            link_element = webpage.grab_element_with_css_selector(
                                                                f"li.SEqptLqWkqtDzWhauSoylugoMquJTSEaJfVZ:nth-child({i}) a.zSvKgyodXUoGbhUhxSWpxUXaFuhWtTKexrM")
                                                            if link_element:
                                                                link_to_profile = link_element.get_attribute('href')
                                                            else:
                                                                link_to_profile = "N/A"
                                                        except:
                                                            try:
                                                                link_element = webpage.grab_element_with_css_selector(
                                                                    f"div.reusable-search__result-container:nth-child({i}) a.zSvKgyodXUoGbhUhxSWpxUXaFuhWtTKexrM")
                                                                if link_element:
                                                                    link_to_profile = link_element.get_attribute('href')
                                                                else:
                                                                    link_to_profile = "N/A"
                                                            except:
                                                                link_to_profile = "N/A"

                                                        log(f"{constants.Bcolors.WARNING}{name_grab} who is {description1} at {description2} for profile {link_to_profile}{constants.Bcolors.ENDC}")

                                                        info = [name_grab, description1,
                                                                description2, link_to_profile]

                                                        csv_io.insert_row(info)
                                                        time.sleep(2)

                                            except Exception as e:
                                                log(f"Error processing follow button: {str(e)}")
                                                continue

                                    except Exception as e:
                                        log(f"Error processing button action: {str(e)}")
                                        continue

                            except Exception as e:
                                log(f"Error processing card {i}: {str(e)}")
                                continue

                    except Exception as e:
                        log(f"Error processing page {page} for keyword {keyword}: {str(e)}")
                        continue

                except Exception as e:
                    log(f"Error processing page {page} for keyword {keyword}: {str(e)}")
                    continue

        log(f"{constants.Bcolors.UNDERLINE} All New Connection's data appended to dataset.csv {constants.Bcolors.ENDC}")

    except Exception as e:
        log(f"Critical error: {str(e)}")
        raise
    finally:
        try:
            browser.end_session()
        except:
            pass
        try:
            csv_io.insert_row(["---------", "----------",
                          "----------", "-------------"])
        except:
            pass
