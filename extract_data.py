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

def check_category(description, category_data):
    desc = list(category_data["desc"])
    cate = list(category_data["cate"])
    for i in range (len(cate)):
        if process_str(desc[i]) in process_str(description):
            return cate[i]
    return False

def add_category(data, category_data):
    temp_data = []
    for item in data:
        category = check_category(item["description"], category_data)
        if category:
            item["category"] = category
        else:
            item["category"] = None
        temp_data.append(item)
    return temp_data

def check_expense_type(category, expense_type_data):
    cate = list(expense_type_data["category"])
    label = list(expense_type_data["label"])
    for i in range (len(cate)):
        if cate[i] == category:
            return label[i]
    return False

def add_expense_type(data, expense_type_data):
    temp_data = []
    for item in data:
        if item["category"]:
            expense_type = check_expense_type(item["category"], expense_type_data)
            if expense_type:
                item["expense_type"] = expense_type
            else:
                item["expense_type"] = None
        else:
            item["expense_type"] = None
        temp_data.append(item)
    return temp_data

#############################################Temp Use#######################################
def exist_category(description, categories):
    for item in categories:
        if process_str(item) in process_str(description):
            return True
    return False

def missed_desc(data_selected, all_categories):
    missed = []
    for i in range (len(data_selected)):
         #print(data_selected[i])
         temp = data_selected[i]["description"]
         if not exist_category(temp, all_categories):
             missed.append(data_selected[i])
    print(len(missed))
    for i in missed:
        print(i)

def exist_expense_type(category, all_categories):
    for item in all_categories:
        if category == item:
            return True
    return False

def missed_category(all_available_categories, all_categories):
    missed = []
    for category in all_available_categories:
        if not exist_expense_type(category, all_categories):
            missed.append(category)
    print(len(missed))
    for i in missed:
        print(i)




if __name__ == "__main__":

    # specify info
    data_location = "./data.json"
    category_location = "./trans_cat.csv"
    expense_type_location = "./cat_label.csv"
    start_date = datetime.datetime(2021, 12, 1)
    end_date = datetime.datetime(2022, 12, 1)

    # load data
    raw_data = load_data(data_location)
    category_data = pd.read_csv(category_location)
    expense_type_data = pd.read_csv(expense_type_location)
    
    # process data
    processed_data = process_data(raw_data)
    
    # select data within given time frame
    data_selected = select_data(processed_data, start_date, end_date)
    
    # add category to items
    data_selected = add_category(data_selected, category_data)

    # add 4 expenses type to data
    data_selected = add_expense_type(data_selected, expense_type_data)

    # for i in data_selected:
    #     print(i)

###############################Temp Use###############################
    
    # find desc that missing catrgory
    # all_category = list(category_data["desc"])
    # missed_desc(data_selected, all_category)

    # find category that missing expense type
    # all category listed
    # all_available_categories = list(category_data["cate"])
    # # all categroy that have assigned a expense type
    # all_categories = list(expense_type_data["category"])
    # missed_category(all_available_categories, all_categories)