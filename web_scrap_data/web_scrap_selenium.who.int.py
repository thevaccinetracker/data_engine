from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from pyvirtualdisplay import Display

import time
import  numpy

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
# chrome_options=chrome_options
driver = webdriver.Chrome(executable_path='../driver/chromedriver.exe', chrome_options=chrome_options)

# driver = webdriver.Remote(
#    command_executor='http://127.0.0.1:4444/wd/hub',
#    desired_capabilities=DesiredCapabilities.CHROME)

driver.get('https://www.who.int/publications/m/item/draft-landscape-of-covid-19-candidate-vaccines')

body = driver.find_element_by_tag_name("body")
body.find_element_by_class_name('button-blue-background').click()

tableData = []
isColumn = True

import  csv
with open(r'../data/raps.org.tabledata.csv', 'w') as file:
    writer = csv.writer(file, delimiter='|', lineterminator='\n')
    writer.writerows(tableData)