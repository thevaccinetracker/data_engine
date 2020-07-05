import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

stopwords = stopwords.words('english')

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Data Engine Database").get_worksheet(6)

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()


# sheetData = sheet.get_all_values()


def GetDataFromFile(file, separator):
    with open(file) as who_file:
        file_data = who_file.readlines()
        for index in range(len(file_data)):
            file_data[index] = file_data[index].split(separator)

    return file_data


def clean_string(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text


def cosine_sim_vectors(vec1, vec2):
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]


def GetCosineSim(sentanceList):
    try:
        cleaned = list(map(clean_string, sentanceList))
        vectorizer = CountVectorizer().fit_transform(cleaned)
        vectors = vectorizer.toarray()
        # csim = cosine_similarity(vectors)

        return cosine_sim_vectors(vectors[0], vectors[1])
    except:
        return 0


def GetRow(data, matchString, col):
    perfactMatch = None
    perfactMatchPer = 0
    for row in data:
        try:
            # print(row[col] , matchString)
            cosineSim = GetCosineSim([row[col], matchString])
            if cosineSim > 0.70:
                if perfactMatchPer < cosineSim:
                    perfactMatch = row
                    perfactMatchPer = cosineSim
            # if row[col] == matchString:
            #     return row
        except:
            print("Error:", row)

    # print(perfactMatch, perfactMatchPer, cosineSim)
    return perfactMatch, perfactMatchPer


def UpdateGoogleSheet(settings, data, gSheet):
    sheetCol = settings["sheetCol"]
    dataCol = settings["dataCol"]
    currentSheetRow = settings["currentSheetRow"]
    updateSheetCol = settings["updateSheetCol"]
    dataColForUpdate = settings["dataColForUpdate"]
    currentIndex = 0
    for sheetRow in gSheet.get_all_values():
        try:
            foundRow, foundRowMatchPer = GetRow(data, sheetRow[sheetCol], dataCol)
            # print(foundRowMatchPer, sheetRow[sheetCol], foundRow)
            if foundRow:
                gSheet.update_cell(currentSheetRow, updateSheetCol, foundRow[dataColForUpdate])
                gSheet.update_cell(currentSheetRow, updateSheetCol + 1, foundRowMatchPer)
                time.sleep(3)

        except:
            print(currentSheetRow, updateSheetCol, dataColForUpdate, foundRow)
        currentSheetRow += 1
        currentIndex += 1


whoData = GetDataFromFile("data/who.int.transformed_data.csv", "|")
rapsData = GetDataFromFile("data/raps.org.tabledata.csv", "|")
airTableData = GetDataFromFile("data/COVID-19 Tracker-Vaccines.csv", ",")

whoSettings = {
    'sheetCol': 2,
    'dataCol': 2,
    'currentSheetRow': 1,
    'updateSheetCol': 8,
    'dataColForUpdate': 4
}
rapsSettings = {
    'sheetCol': 3,
    'dataCol': 1,
    'currentSheetRow': 1,
    'updateSheetCol': 10,
    'dataColForUpdate': 2
}
airTableSettings = {
    'sheetCol': 1,
    'dataCol': 0,
    'currentSheetRow': 1,
    'updateSheetCol': 6,
    'dataColForUpdate': 3
}

# UpdateGoogleSheet(whoSettings, whoData, sheet)
# UpdateGoogleSheet(rapsSettings, rapsData, sheet)
UpdateGoogleSheet(airTableSettings, airTableData, sheet)


def GetPhaseCorp():
    with open('vt_corp/phase.txt', 'r') as file:
        data = file.readlines()
        phase = {}
        for row in data:
            col = row.split(':')
            phase[col[0]] = col[1].split(',')
    return phase


def GetStagePhase(stage):
    stage = stage.lower().replace(' ', '')
    findStageIn = []
    for key in phase:
        for p in phase[key]:
            if p.lower().replace(' ', '') in stage:
                findStageIn.append(key)
    findStageIn = sorted(list(set(findStageIn)), reverse=True)
    if len(findStageIn) > 0:
        return findStageIn[0]
    return '0'


def GetFinalPhase(all_stage):
    initLen = len(all_stage)
    final_stage = dict()

    final_stage_result = "Not Sure"
    for d in all_stage:
        if d not in final_stage:
            final_stage[d] = 1
        else:
            final_stage[d] += 1
    if len(final_stage) == initLen:
        final_stage_result = "Not Sure"

    final_stage = sorted(final_stage.items(), key=lambda x: x[1], reverse=True)
    if len(final_stage):
        final_stage_result = final_stage[0][0]

    if final_stage_result == '0':
        final_stage_result = "Not Sure"

    return final_stage_result


def UpdateGoogleSheetFinalStage(gSheet):
    currentSheetRow = 2
    updateSheetCol = 15
    index = 0
    for sheetRow in gSheet.get_all_values():
        if index == 0:
            index = 1
            continue
        WHOStage = GetStagePhase(sheetRow[7])
        RAPSStage = GetStagePhase(sheetRow[9])
        AIRTableStage = GetStagePhase(sheetRow[5])
        finalStage = GetFinalPhase([WHOStage, RAPSStage, AIRTableStage])
        gSheet.update_cell(currentSheetRow, updateSheetCol, finalStage)
        currentSheetRow += 1
        time.sleep(3)


phase = dict(GetPhaseCorp())
UpdateGoogleSheetFinalStage(sheet)

# {
#     "1": ["phase1", "phase 1",
#           "phasei", "phase i",
#           "phase1/2", "phase 1/2", "phase 1 /2", "phase 1 / 2",
#           "phase1/1", "phase 1/1", "phase 1 /1", "phase 1 / 1",
#           ],
#     "3": ["phase3", "phase 3",
#           "phaseiii", "phase iii",
#           "phase1/3", "phase 1/3", "phase 1 /3", "phase 1 / 3",
#           ],
#     "2": ["phase2", "phase 2",
#           "phaseii", "phase ii",
#           "phase1/2", "phase 1/2", "phase 1 /2", "phase 1 / 2",
#           ],
# }
