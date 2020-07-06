import sys

sys.path.append(r'C:\Users\v-shvi\Desktop\Personal\VT\data_engine')
sys.path.append(r'C:\Users\v-shvi\Desktop\Personal\VT\data_engine\web_scrap_data')
sys.path.append(r'C:\Users\v-shvi\Desktop\Personal\VT\data_engine\get_cosine')
sys.path.append(r'C:\Users\v-shvi\Desktop\Personal\VT\data_engine\preprocess_data')


ROOT_PATH = "../"
DATA_PATH = "data"

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": r"C:\Users\v-shvi\Desktop\Personal\VT\data_engine\data",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

# chrome_options = chrome_options
# GOOGLE_DRIVER = webdriver.Chrome(executable_path='driver/chromedriver.exe')
GOOGLE_DRIVER = webdriver.Chrome(executable_path='driver/chromedriver.exe', chrome_options=chrome_options)

# SETTINGS DATA
GSHEET_CRED_FILE = "credentials.json"
GSHEET_SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
GSHEET_FILE = "Data Engine Database"
GSHEET_WORKSHEET = 6

WHO_INPUT_DATA = "data/who.int.transformed_data.csv"
RAPS_INPUT_DATA = "data/raps.org.tabledata.csv"
AIRTABLE_INPUT_DATA = "data/COVID-19 Tracker-Vaccines.csv"

VT_CORPS = 'vt_corp/phase.txt'
STOPWORDS = 'english'

