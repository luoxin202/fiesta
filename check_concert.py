from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3

class ActionQueryConcert(Action):
    def name(self):
        return "action_query_concert"

    def run(self, dispatcher, tracker, domain):
        # 获取用户提供的音乐会名称
        concert_name = tracker.latest_message.get("text")

        # 连接到SQLite3数据库
        conn = sqlite3.connect("rasa.db")
        cursor = conn.cursor()

        # 执行查询操作
        cursor.execute("SELECT * FROM concerts WHERE name = ?", (concert_name,))
        concert_data = cursor.fetchone()

        if concert_data:
            # 如果找到匹配的音乐会信息，将其发送给用户
            concert_id, name, location, date, tickets_available = concert_data
            message = f"Concert Name: {name}\nLocation: {location}\nDate: {date}\nTickets Available: {tickets_available}"
            dispatcher.utter_message(message)
        else:
            # 如果未找到匹配的音乐会信息，向用户报告错误
            dispatcher.utter_message("Sorry, I couldn't find information about that concert.")

        # 关闭数据库连接
        conn.close()

        return []