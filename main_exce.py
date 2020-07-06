from web_scrap import airtable_com, raps_org, who_int
import time

airtable_com.WebScrap()
raps_org.WebScrap()
who_int.WebScrap()

time.sleep(60 * 5)

from preprocess_data import pdf_read_table

pdf_read_table.TransformPDFData()

time.sleep(60 * 2)

import googleDb

googleDb.MainGSheetUpdate()
