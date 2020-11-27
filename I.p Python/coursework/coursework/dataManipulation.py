import requests
import pandas as pd
import user_agents
from tkinter import messagebox
from requests.exceptions import HTTPError
import constants as const


# Read data from the givURL
def getResponse(url):
    try:
        openUrl = requests.get(url)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
        messagebox.showerror('DocumentAnalysis', err)

    else:
        if openUrl.status_code == 200:
            jsonData = pd.read_json(openUrl.text, lines=True)
            if checkIfColumnsExists(jsonData, [const.Columns.visitor_country.name,const.Columns.env_doc_id.name,const.Columns.visitor_uuid.name]):
                jsonData['continents_code'] = jsonData[const.Columns.visitor_country.name].map(const.cntry_to_cont)
                jsonData['continents'] = jsonData['continents_code'].map(const.continents)
            else:
                messagebox.showwarning('Mandatory fields are missing in the json provided')
        else:
            messagebox.showwarning("Error receiving data", openUrl.getcode())
    return jsonData


# Check whether the given dataframe contains the necessary column
def checkIfColumnsExists(dfDoc, listOfColumns):
    if set(listOfColumns).issubset(dfDoc.columns):
        return True
    else:
        return False


# Method used to load data from the json and returns dataframe
def loadFromJson(fileName=None):
    if fileName:
        if len(fileName.split('.')) > 1:
            filePath = r'dataset\\' + fileName
        else:
            messagebox.showerror('Info',"Kindly provide the correct file name")
    else:
        filePath = r'dataset\sample_100k_lines.json'

    try:
        jsonData = pd.read_json(filePath, lines=True)
    except Exception as err:
        print(f'Other error occurred: {err}')
        messagebox.showerror('DocumentAnalysis', err)
    else:
        if checkIfColumnsExists(jsonData, ['visitor_country', 'env_doc_id', 'visitor_uuid']):
            jsonData['continents_code'] = jsonData['visitor_country'].map(const.cntry_to_cont)
            jsonData['continents'] = jsonData['continents_code'].map(const.continents)
    return jsonData


# Takes the user-agent as input parse it and returns the family name of the browser
def parse_ua_series(ua):
    try:
        p = user_agents.parse(ua)
    except Exception as err:
        print(f'Error while paring the user agent: {err}')
        messagebox.showerror('DocumentAnalysis', err)
    return pd.Series([p.browser.family])


# Method used to parse the user-agent
def parseUserAgent(dfDoc, _inColumn):
    if not dfDoc.empty:
        dfDoc = dfDoc.visitor_useragent.apply(parse_ua_series).rename(columns={0: 'browser'})
    return dfDoc['browser'].value_counts().to_dict()


# Form the size of the given file
def formSize(visitors):
    if visitors.getCountofRows() // 1000000 != 0:
        size = str(visitors.getCountofRows() // 1000000) + 'm lines'
    elif visitors.getCountofRows() // 1000 != 0:
        size = str(visitors.getCountofRows() // 1000) + 'k lines'
    else:
        size = str(visitors.getCountofRows()) + ' lines'

    return size
