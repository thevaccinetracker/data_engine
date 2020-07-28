import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

from settings import GSHEET_CRED_FILE, GSHEET_SCOPE, GSHEET_FILE, GSHEET_WORKSHEET
from settings import WHO_INPUT_DATA, RAPS_INPUT_DATA, AIRTABLE_INPUT_DATA
from settings import VT_CORPS

import get_cosine.get_cosine

# use creds to create a client to interact with the Google Drive API
creds = ServiceAccountCredentials.from_json_keyfile_name(GSHEET_CRED_FILE, GSHEET_SCOPE)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open(GSHEET_FILE).get_worksheet(GSHEET_WORKSHEET)

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()


def GetDataFromFile(file, separator):
    with open(file) as who_file:
        file_data = who_file.readlines()
        for index in range(len(file_data)):
            file_data[index] = file_data[index].split(separator)

    return file_data


def GetRow(data, matchString, col):
    perfactMatch = None
    perfactMatchPer = 0
    for row in data:
        # try:
            # print(row[col] , matchString)
            cosineSim = get_cosine.get_cosine.GetCosineSim([row[col], matchString])
            if cosineSim > 0.70:
                if perfactMatchPer < cosineSim:
                    perfactMatch = row
                    perfactMatchPer = cosineSim
            # if row[col] == matchString:
            #     return row
        # except:
        #     print("Error:", row)

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

print("WHO data loading start...")
whoData = GetDataFromFile(WHO_INPUT_DATA, "|")
print("WHO data loading complete...")

print("RAPS data loading start...")
rapsData = GetDataFromFile(RAPS_INPUT_DATA, "|")
print("RAPS data loading complete...")

print("AirTable data loading start...")
airTableData = GetDataFromFile(AIRTABLE_INPUT_DATA, "|")
print("AirTable data loading complete...")

time.sleep(10)

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

print("Updating GSheet for WHO...")
UpdateGoogleSheet(whoSettings, whoData, sheet)
print("Updating GSheet for WHO Completed...")

time.sleep(10)

print("Updating GSheet for RAPS...")
UpdateGoogleSheet(rapsSettings, rapsData, sheet)
print("Updating GSheet for RAPS Completed...")

time.sleep(10)

print("Updating GSheet for AirTable...")
UpdateGoogleSheet(airTableSettings, airTableData, sheet)
print("Updating GSheet for AirTable Completed...")

time.sleep(10)

def GetPhaseCorp():
    with open(VT_CORPS, 'r') as file:
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
def MainGSheetUpdate():
    print("Updating GSheet for Final Stage...")
    UpdateGoogleSheetFinalStage(sheet)
    print("Updating GSheet for Final Stage Completed...")
