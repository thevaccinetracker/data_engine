from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from pyvirtualdisplay import Display

import time

# display = Display(visible=0, size=(800, 600))
# display.start()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
        "download.default_directory": r"C:\Users\v-shvi\PycharmProjects\cosin-similarity\data",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

# chrome_options = chrome_options
driver = webdriver.Chrome(executable_path='../driver/chromedriver.exe', chrome_options=chrome_options)

# driver = webdriver.Remote(
#    command_executor='http://127.0.0.1:4444/wd/hub',
#    desired_capabilities=DesiredCapabilities.CHROME)

driver.get('https://airtable.com/shrSAi6t5WFwqo3GM/tblEzPQS5fnc0FHYR/viweyymxOAtNvo7yH?blocks=bipZFzhJ7wHPv7x9z')

# driver.manage().timeouts().implicitlywait(30)

# time.sleep(10)
# elem = driver.find_element_by_id("headerAndDataRowContainer")
#
# print elem.find_element_by_id("headerLeftPane").text
# dataLeftPane = elem.find_element_by_id("dataLeftPane")
# for dataRow in dataLeftPane.find_elements_by_class_name("dataRow"):
#     print dataRow.text

# def enable_download_headless(browser, download_dir):
#     browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
#     params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
#     browser.execute("send_command", params)
#
# download_dir = r"C:\Users\v-shvi\PycharmProjects\cosin-similarity\data"
# enable_download_headless(driver, download_dir)


table = driver.find_element_by_id("table")
table.find_element_by_class_name('viewConfigContainer').find_element_by_class_name('link-quiet').click()
time.sleep(5)
table.find_element_by_class_name('viewSwitcherContainer').find_elements_by_tag_name('li')[2].click()
time.sleep(5)
viewMenuPopover = table.find_elements_by_class_name("viewMenuPopover")[0]
viewMenuPopover.click()
time.sleep(3)
viewMenuPopover.find_element_by_class_name("menu").find_element_by_tag_name("li").click()
# time.sleep(20)
# import os
# import shutil
# Initial_path = r"C:\Users\v-shvi\Downloads"
# filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)], key=os.path.getctime)
# shutil.move(filename, os.path.join(r"data", "airtable.com.csv"))





# References
# https://medium.com/@moungpeter/how-to-automate-downloading-files-using-python-selenium-and-headless-chrome-9014f0cdd196