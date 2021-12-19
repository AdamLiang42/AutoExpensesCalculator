from selenium import webdriver
from bs4 import BeautifulSoup
import re
import datetime
import json
import pandas as pd
import string

def load_data(data_location):
    # load data file
    data = json.load(open("./data.json"))
    data = json.load(open(data_location))
    data = data["transactions"]

    # construct data
    temp_data = []
    for i in data:
        temp_data += i
    data = temp_data
    return data

def process_data(data):
    # convert date
    processed_data = []
    for i in range (len(data)):
        item = {}
        date = data[i]["FormattedDate"]
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        #data[i]["Date"] = date
        item["date"] = date
        item["description"] = data[i]["Description"]
        item["amount"] = data[i]["AmountNumeric"]
        processed_data.append(item)
    return processed_data

def select_data(data, start_date, end_date):
    selected_data = []
    for i in data:
        if start_date <= i["date"] < end_date:
            selected_data.append(i)
    return selected_data

def process_str(a_str):
    # convert to all lower case
    temp_str = a_str.lower()
    # remove all punctuation
    for character in string.punctuation:
        temp_str = temp_str.replace(character, '')
    # remove spaces
    temp_str = temp_str.replace(" ", '')
    return temp_str

def exist_category(description, categories):
    for item in categories:
        if process_str(item) in process_str(description):
            return True
    return False
#############################################Temp Use#######################################
def missed_desc(data_selected, all_category):
    missed = []
    for i in range (len(data_selected)):
         #print(data_selected[i])
         temp = data_selected[i]["description"]
         if not exist_category(temp, all_category):
             missed.append(data_selected[i])
    
    print(len(missed))
    for i in missed:
        print(i)




if __name__ == "__main__":
    # specify info
    data_location = "./data.json"
    category_location = "./trans_cat.csv"
    start_date = datetime.datetime(2021, 12, 1)
    end_date = datetime.datetime(2022, 12, 1)

    # load data
    data = load_data(data_location)
    category_data = pd.read_csv(category_location)
    
    # process data
    data = process_data(data)
    
    # select data within given time frame
    data_selected = select_data(data, start_date, end_date)


    # find missed catrgory
    all_category = list(category_data["desc"])
    missed_desc(data_selected, all_category)