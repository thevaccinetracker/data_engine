from settings import GOOGLE_DRIVER, DATA_PATH
import time

def WebScrap():
    print("Raps webscrap: Started...")

    driver = GOOGLE_DRIVER

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

    import csv
    with open(DATA_PATH + r'/raps.org.tabledata.csv', 'w') as file:
        writer = csv.writer(file, delimiter='|', lineterminator='\n')
        writer.writerows(tableData)

    time.sleep(60 * 1)

    print("Raps webscrap: Completed...")
