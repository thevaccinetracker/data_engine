import tabula

file = "../data/novel-coronavirus-landscape-covid-19-24062020.pdf"
tabula.convert_into(file, "../data/who_covid_data.csv", output_format="csv", pages='all')

import csv

file_CSV = open('../data/who_covid_data.csv')
data_CSV = csv.reader(file_CSV)
list_CSV = list(data_CSV)


def transformData(data):
    if len(data) <= 0:
        return []
    tempData = data[0]
    data.remove(tempData)
    for r in data:
        index = 0
        for c in range(len(tempData)):
            col = tempData[c] + " " + r[c].lstrip('\r\n').rstrip('\r\n').strip()
            tempData[c] = col.strip()

    cleanCol = []
    for col in tempData:
        cleanCol.append(col.replace("\n", " "))
    return cleanCol


indexStartFrom = 3
row = []
transformedData = []
for data in range(indexStartFrom, len(list_CSV)):
    if list_CSV[data][3] != '':
        if len(row) > 0:
            transformedData.append(transformData(row))
        row = []
    row.append(list_CSV[data])

with open(r'../data/who.int.transformed_data.csv', 'w') as file:
    writer = csv.writer(file, delimiter='|', lineterminator='\n')
    writer.writerows(transformedData)
