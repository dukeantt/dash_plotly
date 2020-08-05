from rasa_chatlog_processor import RasaChalogProcessor

b = RasaChalogProcessor()
a = b.get_chatlog_by_month(input_month="07", raw_chatlog="data/rasa_chatlog/raw_data/all_conv_detail.csv")