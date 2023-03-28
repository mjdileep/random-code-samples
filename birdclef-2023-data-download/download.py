import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

rating_classes = ["A", "B"]
counts = None
with open("bird_file_counts.pt", "rb") as fp:
    counts = pickle.load(fp)


def process_results(results):
    classes = results.find_elements(By.CLASS_NAME, "selected")
    for class_ in classes:
        if class_.text in rating_classes:
            try:
                es = class_.find_element(By.XPATH,'..').find_element(By.XPATH,'..').find_element(By.XPATH,'..').find_elements(By.TAG_NAME, "a")
                es[0].click()

            except Exception as ex:
                print(ex)
        else:
            time.sleep(20)
            return False
    time.sleep(20)
    return True


def process_class(class_name):
    chrome_options = Options()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
                 '(KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://xeno-canto.org/species/{}".format(class_name))
    time.sleep(1)
    current_page = 0
    while True:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "results")))
        results = driver.find_element(By.CLASS_NAME, "results")
        if process_results(results):
            try:
                current_page += 1
                next_page = driver.find_element(By.CLASS_NAME, "results-pages").find_elements(By.TAG_NAME, "li")[current_page]
                next_page.click()
                continue
            except Exception as ex:
                pass
        break


for each in counts:
    print("Downloading ", each["scientific_name"])
    scientific_name = each["scientific_name"].replace(" ", "-")
    try:
        process_class(scientific_name)
    except Exception as ex:
        print("Error occured:", ex)


