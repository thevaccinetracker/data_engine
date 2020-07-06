from settings import GOOGLE_DRIVER


def WebScrap():
    driver = GOOGLE_DRIVER

    driver.get('https://www.who.int/publications/m/item/draft-landscape-of-covid-19-candidate-vaccines')

    body = driver.find_element_by_tag_name("body")
    body.find_element_by_class_name('button-blue-background').click()

    tableData = []
    isColumn = True

    import csv
    with open(r'../data/raps.org.tabledata.csv', 'w') as file:
        writer = csv.writer(file, delimiter='|', lineterminator='\n')
        writer.writerows(tableData)
