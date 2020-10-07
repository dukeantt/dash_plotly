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
month_dict = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct",
              11: "Nov", 12: "Dec"}
outcome_list = ["thank", "shipping_order", "handover_to_inbox", "silence", "other"]
uc_list = ["uc_s1", "uc_s2", "uc_s3", "uc_s4", "uc_s5", "uc_s8", "uc_s9", "other"]


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

def get_chatlog_from_db(db_name, from_date, to_date):
    client = MongoClient("mongodb+srv://ducanh:1234@ducanh.sa1mn.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client['chatlog_db']
    collection = db[db_name]
    start = datetime.datetime.strptime(from_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(to_date, "%Y-%m-%d")

    start_month = from_date[:7]
    end_month = to_date[:7]
    special_month = ["2020-02", "2020-03", "2020-04", "2020-05", "2020-06"]  # 2 thang nay co thoi gian bat bot khac cac thang con lai
    time_start_morning = datetime.datetime.strptime("09:00:00", "%H:%M:%S")
    time_end_morning = datetime.datetime.strptime("12:05:00", "%H:%M:%S")

    time_start_afternoon = datetime.datetime.strptime("14:00:00", "%H:%M:%S")
    time_end_afternoon = datetime.datetime.strptime("17:05:00", "%H:%M:%S")

    # chatlog_df = pd.DataFrame([document for document in collection.find({'conversation_begin_date': {'$gte': start, '$lte': end, }})])
    if start_month in special_month and end_month in special_month:
        chatlog_df = pd.DataFrame([document for document in collection.find({
            '$and': [
                {'conversation_begin_date': {'$gte': start, '$lte': end}},
                {'conversation_begin_time': {'$gte': datetime.datetime.strptime("09:00:00", "%H:%M:%S"),
                                             '$lte': datetime.datetime.strptime("17:30:00", "%H:%M:%S")}},
                {'week_day': {'$gte': 0, '$lte': 4}},
            ]
        })])
    elif start_month in special_month:
        chatlog_df = pd.DataFrame([document for document in collection.find(
            {
                '$or': [
                    {
                        '$and': [
                            {'conversation_begin_date': {'$gte': start,
                                                         '$lte': datetime.datetime.strptime("2020-07-31", "%Y-%m-%d")}},
                            {'conversation_begin_time': {'$gte': datetime.datetime.strptime("09:00:00", "%H:%M:%S"),
                                                         '$lte': datetime.datetime.strptime("17:30:00", "%H:%M:%S")}},
                            {'week_day': {'$gte': 0, '$lte': 4}},
                        ]
                    },
                    {
                        '$and': [
                            {'conversation_begin_date': {'$gte': datetime.datetime.strptime("2020-08-01", "%Y-%m-%d"),
                                                         '$lte': end}},
                            {'$or': [
                                {'conversation_begin_time': {'$gte': time_start_morning, '$lte': time_end_morning}},
                                {'conversation_begin_time': {'$gte': time_start_afternoon, '$lte': time_end_afternoon}},
                            ]},
                            {'week_day': {'$gte': 0, '$lte': 4}},
                        ]
                    }
                ]
            }
        )])
    else:
        chatlog_df = pd.DataFrame([document for document in collection.find({
            '$and': [
                {'conversation_begin_date': {'$gte': start, '$lte': end}},
                {'$or': [
                    {'conversation_begin_time': {'$gte': time_start_morning, '$lte': time_end_morning}},
                    {'conversation_begin_time': {'$gte': time_start_afternoon, '$lte': time_end_afternoon}},
                ]},
                {'week_day': {'$gte': 0, '$lte': 4}},
            ]
        })])

    if len(chatlog_df) > 0:
        chatlog_df = chatlog_df.drop(columns=["_id", "conversation_time", "conversation_begin_date", "week_day"])
    return chatlog_df

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
    no_user_list = []
    success_rate_list = []

    for month in month_list:
        sub_df = df[pd.DatetimeIndex(df["conversation_begin_date"]).month == month]
        sub_df_success = sub_df[(sub_df["thank"] == 1) | (sub_df["shipping_order"] == 1)]
        if len(sub_df) == 0:
            no_conversation_list.append(0)
            success_rate_list.append(0)
            continue
        no_user = get_number_of_user(sub_df)
        no_conversation = get_number_of_conversation(sub_df)
        success_rate = get_number_of_conversation(sub_df_success) * 100 / no_conversation
        success_rate = float("{:.1f}".format(success_rate))

        if success_rate == 0.0:
            success_rate = int(success_rate)

        no_conversation_list.append(no_conversation)
        no_user_list.append(no_user)
        success_rate_list.append(success_rate)
    month_list = [month_dict[x] for x in month_list]
    return month_list, no_conversation_list, no_user_list, success_rate_list


def get_number_of_each_outcome(df):
    outcome_dict = {}
    for outcome in outcome_list:
        outcome_dict[outcome] = sum(df[outcome].to_list())
    return outcome_dict


def get_number_of_each_usecase(df):
    usecase_dict = {}
    column_list = df.columns.to_list()

    for uc in uc_list:
        columns_to_use = [x for x in column_list if uc in x]
        usecase_dict[uc] = sum(df[columns_to_use].sum(axis=0).to_list())
    return usecase_dict


def get_number_of_outcome_of_each_usecase(df_outcome, df_usecase):
    outcome_of_usecase_dict = {x: {y: 0 for y in outcome_list} for x in uc_list}
    df_usecase_column_list = df_usecase.columns.to_list()
    for uc in uc_list:
        columns_to_use = [x for x in df_usecase_column_list if uc in x]
        sub_df_usecase = df_usecase[columns_to_use]
        sub_df_usecase = sub_df_usecase[(sub_df_usecase.T != 0).any()]
        index_list = sub_df_usecase.index.to_list()
        for index in index_list:
            conv_id = df_usecase.loc[index]["conv_id"]
            outcome_of_uc_df = df_outcome[df_outcome["conv_id"] == conv_id][outcome_list]
            outcome_of_uc_df = outcome_of_uc_df.loc[:, (outcome_of_uc_df != 0).any(axis=0)]
            outcome_of_uc_list = outcome_of_uc_df.columns.to_list()
            for oc in outcome_of_uc_list:
                outcome_of_usecase_dict[uc][oc] += 1

    return outcome_of_usecase_dict


def get_conversation_each_outcome(df: pd.DataFrame):
    column_list = ["conversation_id", "use_case", "sender_id", "user_message", "bot_message", "created_time", "intent",
                   "entities"]
    qualified_thank = []
    qualified_shipping = []

    for id in df[df["outcome"] == "thank"]["conversation_id"].to_list():
        if len(df[df["conversation_id"] == id]["turn"].drop_duplicates()) > 1:
            qualified_thank.append(id)


    thank_df = df[df["conversation_id"].isin(qualified_thank)][column_list]
    # shipping_order_df = df[df["conversation_id"].isin(qualified_shipping)][column_list]
    shipping_order_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "shipping_order"]["conversation_id"]))][column_list]
    handover_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "handover_to_inbox"]["conversation_id"]))][column_list]
    silence_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "silence"]["conversation_id"]))][column_list]
    other_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "other"]["conversation_id"]))][column_list]
    # agree_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "agree"]["conversation_id"]))][column_list]

    return thank_df, shipping_order_df, handover_df, silence_df, other_df


def get_conversation_each_usecase(df: pd.DataFrame):
    column_list = ["conversation_id", "use_case", "outcome", "sender_id", "user_message", "bot_message", "created_time",
                   "intent",
                   "entities"]
    uc1_df = df[df["conversation_id"].isin(list(df[df["use_case"] == "uc_s1"]["conversation_id"]))][column_list]
    uc2_df = df[df["conversation_id"].isin(list(df[df["use_case"] == "uc_s2"]["conversation_id"]))][column_list]
    uc3_df = df[df["conversation_id"].isin(list(df[df["use_case"].isin(["uc_s31", "uc_s32"])]["conversation_id"]))][column_list]
    uc4_df = df[df["conversation_id"].isin(list(df[df["use_case"].isin(["uc_s41", "uc_s42", "uc_s43"])]["conversation_id"]))][column_list]
    uc5_df = df[df["conversation_id"].isin(list(df[df["use_case"].isin(["uc_s51", "uc_s52", "uc_s53"])]["conversation_id"]))][column_list]
    uc8_df = df[df["conversation_id"].isin(list(df[df["use_case"] == "uc_s8"]["conversation_id"]))][column_list]
    uc9_df = df[df["conversation_id"].isin(list(df[df["use_case"] == "uc_s9"]["conversation_id"]))][column_list]

    noticable_usecase_conversation_id = uc1_df["conversation_id"].drop_duplicates().to_list() \
                                        + uc2_df["conversation_id"].drop_duplicates().to_list() \
                                        + uc3_df["conversation_id"].drop_duplicates().to_list() \
                                        + uc4_df["conversation_id"].drop_duplicates().to_list() \
                                        + uc5_df["conversation_id"].drop_duplicates().to_list()\
                                        + uc8_df["conversation_id"].drop_duplicates().to_list() \
                                        + uc9_df["conversation_id"].drop_duplicates().to_list()

    other_usecase_df = df[~df["conversation_id"].isin(noticable_usecase_conversation_id)][column_list]

    return uc1_df, uc2_df, uc3_df, uc4_df, uc5_df, uc8_df, uc9_df, other_usecase_df