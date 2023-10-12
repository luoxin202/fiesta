from flask import Flask, render_template, request
from rasa.nlu import Interpreter

app = Flask(__name__)
interpreter = Interpreter.load("<E:\Code\python\demo\rasaProject\models\20231012-112503-marked-pair.tar.gz>")

@app.route("/")
def index():
    return render_template("web/templates/chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["text"]
    bot_response = get_bot_response(user_input)
    return bot_response

def get_bot_response(user_input):
    response = interpreter.parse(user_input)  # 发送用户输入给 Rasa 解释器
    bot_response = response["text"]  # 获取机器人回复
    return bot_response

if __name__ == "__main__":
    app.run(debug=True)
