statement = """"Institute of Medical Biology, Chinese Academy of Medical Sciences",Vaccine,Inactivated virus,Phase II,Phase II began June 2020,Inactivated,NCT04412538,Unknown,,,N/A,https://docs.google.com/document/d/1Y4nCJJ4njzD1wiHbufCY6gqfRmj49Qn_qNgOJD62Wik/edit,6/23/2020"""


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
    print(rowArray)
    return rowArray

parseRowToCell(statement)