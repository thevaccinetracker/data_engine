from web_scrap import airtable_com, raps_org, who_int
import time

airtable_com.WebScrap()
raps_org.WebScrap()
who_int.WebScrap()

print("Sleep for 1 min")
time.sleep(60 * 1)

from preprocess_data import pdf_read_table

pdf_read_table.TransformPDFData()

print("Sleep for 1 min")
time.sleep(60 * 1)

import googleDb

googleDb.MainGSheetUpdate()
