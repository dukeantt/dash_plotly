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

logging.root.setLevel(logging.NOTSET)
logging.basicConfig(
    level=logging.NOTSET,
    format='%(asctime)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
# db_name = "rasa_chatlog_all_9_9"
db_name = "test_crawl_weekly_14_9"


def get_all_conv():
    with open('../data/rasa_chatlog/raw_data/all_conv.pkl', 'rb') as f:
        data = pickle.load(f)
    return data


def get_all_conv_detail():
    """
    Get conversation detail from file
    """
    all_conv_detail_df = pd.read_csv("chatlog_data/all_conv_detail.csv",
                                     names=["sender_id", "slots", "latest_message", "latest_event_time",
                                            "followup_action", "paused", "events", "latest_input_channel",
                                            "active_form", "latest_action_name"
                                            ])
    return all_conv_detail_df


def append_dict_as_row(file_name, dict_of_elem, field_names):
    with open(file_name, 'a+', newline='') as write_obj:
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        dict_writer.writerow(dict_of_elem)


def export_conversation_detail():
    """
    Export all conversation detail to file so that we dont have to crawl everytime
    """
    file_name = "../data/rasa_chatlog/raw_data/all_conv_detail.csv"
    all_conv = get_all_conv()
    all_sender_id = [x["sender_id"] for x in all_conv]
    for sender_id in all_sender_id:
        conversation_detail_api = "curl -H \"Authorization: Bearer $TOKEN\" -s https://babeshop.ftech.ai/api/conversations/{}"
        token = "TOKEN=$(curl -s https://babeshop.ftech.ai/api/auth -d '{\"username\": \"me\", \"password\": \"w4J6OObi996nDGcQ4mlYNK4F\"}' | jq -r .access_token)"
        if os.popen(token + " && " + conversation_detail_api.format(sender_id)).read() is not None:
            try:
                conversation_detail = json.loads(
                    os.popen(token + " && " + conversation_detail_api.format(sender_id)).read())
                field_names = list(conversation_detail.keys())
                append_dict_as_row(file_name, conversation_detail, field_names)
                logger.info("Add row to file")
            except Exception as ex:
                logger.error(ex)


def export_conversations():
    """
    Export all conversation to file so that we dont have to crawl everytime
    """
    conversation_api = "curl -H \"Authorization: Bearer $TOKEN\" -s https://babeshop.ftech.ai/api/conversations?start=2020-07-01T00:00:00.000Z"
    token = "TOKEN=$(curl -s https://babeshop.ftech.ai/api/auth -d '{\"username\": \"me\", \"password\": \"w4J6OObi996nDGcQ4mlYNK4F\"}' | jq -r .access_token)"
    all_conversations = json.loads(os.popen(token + " && " + conversation_api).read())
    with open('../data/rasa_chatlog/raw_data/all_conv.pkl', 'wb') as f:
        pickle.dump(all_conversations, f)


def get_timestamp(timestamp: int, format: str):
    """

    :param timestamp:
    :param format: %Y-%m-%d %H:%M:%S
    :return:
    """
    readable_timestamp = datetime.datetime.utcfromtimestamp(timestamp).strftime(format)
    return readable_timestamp


def crawl_rasa_chatlog():
    export_conversations()
    export_conversation_detail()


def get_chatlog_from_db(from_date, to_date):
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


def get_chatlog_from_db2(from_date, to_date):
    client = MongoClient("mongodb+srv://ducanh:1234@ducanh.sa1mn.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client['chatlog_db']
    # collection = db[db_name]
    collection = db["test_crawl_weekly_14_9"]
    start = datetime.datetime.strptime(from_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(to_date, "%Y-%m-%d")

    time_start_morning = datetime.datetime.strptime("09:00:00", "%H:%M:%S")
    time_end_morning = datetime.datetime.strptime("12:05:00", "%H:%M:%S")

    time_start_afternoon = datetime.datetime.strptime("14:00:00", "%H:%M:%S")
    time_end_afternoon = datetime.datetime.strptime("17:05:00", "%H:%M:%S")

    chatlog_df = pd.DataFrame([document for document in collection.find({})])
    # chatlog_df = pd.DataFrame([document for document in collection.find({'conversation_begin_date': {'$gte': start, '$lte': end, }})])
    # chatlog_df = pd.DataFrame([document for document in collection.find({
    #     '$and': [
    #         {'conversation_begin_date': {'$gte': start, '$lte': end}},
    #         {'$or': [
    #             {'conversation_begin_time': {'$gte': time_start_morning, '$lte': time_end_morning}},
    #             {'conversation_begin_time': {'$gte': time_start_afternoon, '$lte': time_end_afternoon}},
    #         ]},
    #         {'week_day': {'$gte': 0, '$lte': 4}},
    #     ]
    # })])

    if len(chatlog_df) > 0:
        chatlog_df = chatlog_df.drop(columns=["_id", "conversation_time", "conversation_begin_date", "week_day"])
    return chatlog_df
