from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3

class ActionCheckOrderStatus(Action):
    def name(self):
        return "action_check_order_status"

    def run(self, dispatcher, tracker, domain):
        # 获取用户提供的订单号
        order_id = tracker.get_slot("order_id")

        # 连接到SQLite3数据库
        conn = sqlite3.connect("rasa.db")
        cursor = conn.cursor()

        try:
            # 查询订单状态
            cursor.execute("SELECT status FROM orders WHERE order_id = ?", (order_id,))
            order_status = cursor.fetchone()

            if order_status:
                dispatcher.utter_message(f"The status of order {order_id} is: {order_status[0]}")
            else:
                # 如果订单不存在，向用户报告错误
                dispatcher.utter_message(f"Order {order_id} does not exist.")
        except Exception as e:
            # 如果出现错误，向用户报告错误
            dispatcher.utter_message("Sorry, there was an error checking the order status. Please try again later.")
        finally:
            # 关闭数据库连接
            conn.close()

        return []