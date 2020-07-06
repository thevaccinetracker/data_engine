import time

from settings import GOOGLE_DRIVER


def WebScrap():
    driver = GOOGLE_DRIVER

    driver.get('https://airtable.com/shrSAi6t5WFwqo3GM/tblEzPQS5fnc0FHYR/viweyymxOAtNvo7yH?blocks=bipZFzhJ7wHPv7x9z')

    table = driver.find_element_by_id("table")
    table.find_element_by_class_name('viewConfigContainer').find_element_by_class_name('link-quiet').click()
    time.sleep(5)
    table.find_element_by_class_name('viewSwitcherContainer').find_elements_by_tag_name('li')[2].click()
    time.sleep(5)
    viewMenuPopover = table.find_elements_by_class_name("viewMenuPopover")[0]
    viewMenuPopover.click()
    time.sleep(3)
    viewMenuPopover.find_element_by_class_name("menu").find_element_by_tag_name("li").click()

# References
# https://medium.com/@moungpeter/how-to-automate-downloading-files-using-python-selenium-and-headless-chrome-9014f0cdd196
