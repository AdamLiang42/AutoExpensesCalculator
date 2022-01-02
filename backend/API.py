from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from extract_data import *

class Data(Resource):
    def __init__(self):
        # specify info
        data_location = "../data/data.json"
        category_location = "../data/trans_cat.csv"
        expense_type_location = "../data/cat_label.csv"
        start_date = datetime.datetime(2021, 11, 1)
        end_date = datetime.datetime(2021, 12, 1)
        
        # load data
        self.data = process_data(data_location, category_location, expense_type_location)
    
        # select data within given time frame
        self.data_selected = select_data(self.data, start_date, end_date)

    def get(self):
        # convert date time to actual string
        data = self.data
        data = []
        for i in self.data:
            i["date"] = i["date"].strftime("%Y/%m/%d")
            data.append(i)
        return {'data': data}, 200  # return data and 200 OK code
    

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    # add '/data' as entry point for data
    api.add_resource(Data, '/data')

    # run Flask app
    app.run()