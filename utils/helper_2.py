import pandas as pd
from csv import DictWriter
import os
import json
import logging
import pickle
import datetime
import time
from ast import literal_eval
from pymongo import MongoClient

client = MongoClient("mongodb+srv://ducanh:1234@ducanh.sa1mn.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client['chatlog_db']
db_name = ""
month_dict = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

def get_data_from_table(db_name, from_date=None, to_date=None):
    # collection = db["conversation_outcome"]
    collection = db[db_name]

    if from_date is None and to_date is None:
        data_df = pd.DataFrame([document for document in collection.find({})])
        return data_df

    start = datetime.datetime.strptime(from_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(to_date, "%Y-%m-%d")
    data_df = pd.DataFrame([document for document in collection.find({
        '$and': [
            {'conversation_begin_date': {'$gte': start, '$lte': end}},
        ]
    })])
    return data_df


def get_success_rate(df):
    no_success = len(df[(df["thank"] == 1) | (df["shipping_order"] == 1)])
    total = len(df)
    success_rate = no_success * 100 / total
    success_rate = "{:.2f}".format(success_rate)
    return str(success_rate) + "%"


def get_number_of_conversation(df):
    no_conversation = len(df["conv_id"].drop_duplicates().to_list())
    return no_conversation


def get_number_of_user(df):
    no_user = len(df["sender_id"].drop_duplicates().to_list())
    return no_user


def get_number_of_conversation_every_month(df):
    month_list = list(
        range(1, max(pd.DatetimeIndex(df["conversation_begin_date"]).month.drop_duplicates().to_list()) + 1))
    no_conversation_list = []
    for month in month_list:
        sub_df = df[pd.DatetimeIndex(df["conversation_begin_date"]).month == month]
        if len(sub_df) == 0:
            no_conversation_list.append(0)
            continue
        no_conversation = get_number_of_conversation(sub_df)
        no_conversation_list.append(no_conversation)
    month_list = [month_dict[x] for x in month_list]
    return month_list, no_conversation_list
