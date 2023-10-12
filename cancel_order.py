from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3

class ActionCancelOrder(Action):
    def name(self):
        return "action_cancel_order"

    def run(self, dispatcher, tracker, domain):
        # 获取用户提供的订单号
        order_id = tracker.get_slot("order_id")

        # 连接到SQLite3数据库
        conn = sqlite3.connect("rasa.db")
        cursor = conn.cursor()

        try:
            # 检查订单是否存在并且未取消
            cursor.execute("SELECT * FROM orders WHERE order_id = ? AND status = 'active'", (order_id,))
            order_data = cursor.fetchone()

            if order_data:
                # 更新订单状态为已取消
                cursor.execute("UPDATE orders SET status = 'cancelled' WHERE order_id = ?", (order_id,))
                conn.commit()
                dispatcher.utter_message(f"Order {order_id} has been cancelled.")
            else:
                # 如果订单不存在或已取消，向用户报告错误
                dispatcher.utter_message(f"Order {order_id} does not exist or has already been cancelled.")
        except Exception as e:
            # 如果出现错误，向用户报告错误
            dispatcher.utter_message("Sorry, there was an error cancelling your order. Please try again later.")
            conn.rollback()
        finally:
            # 关闭数据库连接
            conn.close()

        return []