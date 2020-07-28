from settings import DATA_PATH
import csv


def parseRowToCell(row):
    isSingleWord = False;
    word = ""
    rowArray = []
    for letter in row:
        if letter == "\"" and not isSingleWord:
            isSingleWord = True
        elif letter == "\"" and isSingleWord:
            isSingleWord = False
        elif letter == "," and not isSingleWord:
            rowArray.append(word)
            word = ""
        else:
            word += letter
    return rowArray


def PreProcessAirtableData():
    print("Airtable csv pre-processing: Started...")
    # with open(r"../data/COVID-19 Tracker-Vaccines.csv") as file:
    with open(DATA_PATH + r"/COVID-19 Tracker-Vaccines.csv") as file:
        data = file.readlines()
        dataMatrix = []
        for row in data:
            if ("\n" in row):
                row = row.replace('\n', '')
            if ("\"" in row):
                dataMatrix.append(parseRowToCell(row))
            else:
                dataMatrix.append(row.split(","))

    with open(DATA_PATH + r'/airtable.transformed_data.csv', 'w') as file:
        writer = csv.writer(file, delimiter='|', lineterminator='\n')
        writer.writerows(dataMatrix)

    print("Airtable csv pre-processing: Completed...")


# PreProcessAirtableData()
