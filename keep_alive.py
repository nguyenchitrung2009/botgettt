from flask import Flask, render_template
from threading import Thread

app = Flask('')


@app.route('/')
def index():
  return "Bot get thông tin fb đã chạy bởi Trung"


def run():
  app.run(host='0.0.0.0', port=80)


def keep_alive():
  server = Thread(target=run)
  server.start()
