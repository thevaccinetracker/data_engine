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

driver = webdriver.Chrome(executable_path='../driver/chromedriver.exe', chrome_options=chrome_options)

# driver = webdriver.Remote(
#    command_executor='http://127.0.0.1:4444/wd/hub',
#    desired_capabilities=DesiredCapabilities.CHROME)

driver.get('https://www.raps.org/news-and-articles/news-articles/2020/3/covid-19-vaccine-tracker')

table = driver.find_element_by_id("vax_wrapper")
table.find_element_by_name("vax_length").send_keys("100")

rows = table.find_element_by_class_name("dataTable").find_elements_by_tag_name("tr")

tableData = []
isColumn = True
for row in rows:
        rowData = []
        colTag = "td"
        if isColumn:
                isColumn = False
                colTag = "th"
        colFirst = True
        for col in row.find_elements_by_tag_name(colTag):
                if colFirst:
                        colFirst = False
                        continue
                rowData.append(col.text.encode('utf-8').decode('utf-8'))
        tableData.append(rowData)

import  csv
with open(r'../data/raps.org.tabledata.csv', 'w') as file:
    writer = csv.writer(file, delimiter='|', lineterminator='\n')
    writer.writerows(tableData)