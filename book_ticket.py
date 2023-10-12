from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
import uuid
from datetime import datetime

class ActionBookTickets(Action):
    def name(self):
        return "action_book_tickets"

    def run(self, dispatcher, tracker, domain):
        # 获取用户提供的音乐会名称和门票数量
        concert_name = tracker.get_slot("concert_name")
        ticket_quantity = tracker.get_slot("ticket_quantity")

        # 生成唯一的订单号
        order_id = str(uuid.uuid4())

        # 获取当前时间作为订单时间
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 连接到SQLite3数据库
        conn = sqlite3.connect("rasa.db")
        cursor = conn.cursor()

        try:
            # 插入订单信息到orders表
            cursor.execute("INSERT INTO orders (order_id, concert_id, ticket_quantity, order_time) VALUES (?, ?, ?, ?)",
                           (order_id, concert_id, ticket_quantity, order_time))
            conn.commit()

            # 更新concerts表中的余票数量
            cursor.execute("UPDATE concerts SET tickets_available = tickets_available - ? WHERE name = ?",
                           (ticket_quantity, concert_name))
            conn.commit()

            # 发送订单确认消息给用户
            message = f"Your order for {ticket_quantity} tickets for {concert_name} has been confirmed. Order ID: {order_id}"
            dispatcher.utter_message(message)
        except Exception as e:
            # 如果出现错误，向用户报告错误
            dispatcher.utter_message("Sorry, there was an error processing your order. Please try again later.")
            conn.rollback()
        finally:
            # 关闭数据库连接
            conn.close()

        return []