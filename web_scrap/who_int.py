from settings import GOOGLE_DRIVER, DATA_PATH
import time


def WebScrap():
    print("WHO webscrap: Started...")

    driver = GOOGLE_DRIVER

    driver.get('https://www.who.int/publications/m/item/draft-landscape-of-covid-19-candidate-vaccines')

    body = driver.find_element_by_tag_name("body")
    body.find_element_by_class_name('button-blue-background').click()

    time.sleep(60 * 1)

    print("WHO webscrap: Completed...")
