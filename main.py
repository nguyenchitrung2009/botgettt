from keep_alive import keep_alive
keep_alive()


import telebot
import datetime
import time
import os
import subprocess
import psutil
import sqlite3
import hashlib
import requests
import datetime
import sys

bot_token = '7167198827:AAGfl5zAA7k1pawqXkolNHqrmnDi82Ta1RQ'
bot = telebot.TeleBot(bot_token)

allowed_group_id = ""
allowed_users = []
processes = []
ADMIN_ID = '5213067986'

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()


def TimeStamp():
  now = str(datetime.date.today())
  return now


def load_users_from_database():
  cursor.execute('SELECT user_id, expiration_time FROM users')
  rows = cursor.fetchall()
  for row in rows:
    user_id = row[0]
    expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
    if expiration_time > datetime.datetime.now():
      allowed_users.append(user_id)


def save_user_to_database(connection, user_id, expiration_time):
  cursor = connection.cursor()
  cursor.execute(
      '''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
  connection.commit()


print("Bot đã được khởi động thành công")


def add_user(message):
  admin_id = message.from_user.id
  if admin_id != ADMIN_ID:
    bot.reply_to(message, 'BẠN KHÔNG CÓ QUYỀN SỬ DỤNG LỆNH NÀY😾.')
    return

  if len(message.text.split()) == 1:
    bot.reply_to(message, ' VUI LÒNG NHẬP ID NGƯỜI DÙNG ')
    return

  user_id = int(message.text.split()[1])
  allowed_users.append(user_id)
  expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
  connection = sqlite3.connect('user_data.db')
  save_user_to_database(connection, user_id, expiration_time)
  connection.close()

  bot.reply_to(
      message,
      f'🚀NGƯỜI DÙNG CÓ ID {user_id} ĐÃ ĐƯỢC THÊM VÀO DANH SÁCH ĐƯỢC PHÉP SỬ DỤNG LỆNH .🚀'
  )


load_users_from_database()

@bot.message_handler(commands=['fb'])
def lqm_sms(message):
  if len(message.text.split()) == 1:
    bot.reply_to(message, 'Vui lòng nhập link hoặc id fb ')
    return

  phone_number = message.text.split()[1]

  file_path = os.path.join(os.getcwd(), "info.py")
  process = subprocess.Popen(["python", file_path, phone_number, "120"])
  processes.append(process)
  bot.reply_to(
      message,
      f'Vui lòng chờ...'
  )


@bot.message_handler(commands=['start'])
def how_to(message):
  how_to_text = '''
- /fb <link hoặc id facebook>: Check thông tin facebook (chỉ người dùng được phép).
- /status: Xem thông tin về thời gian hoạt động, % CPU, % Memory, % Disk đang sử dụng của bot.
- /stop: Dừng lại tất cả các tác vụ đang chạy. ( Chỉ Quản Trị Viên Mới Được Dùng Lệnh Này).
-/restart: Khởi động lại bot (Chỉ admin).
- /admin: Hiển thị thông tin admin.
- /help: danh sách lệnh và hướng dẫn sử dụng.
'''
  bot.reply_to(message, how_to_text)




@bot.message_handler(commands=['help'])
def help(message):
  help_text = '''
 Danh sách lệnh:
- /fb <link hoặc id facebook>: Check thông tin facebook (chỉ người dùng được phép).
- /status: Xem thông tin về thời gian hoạt động, % CPU, % Memory, % Disk đang sử dụng của bot.
- /stop: Dừng lại tất cả các tác vụ đang chạy. ( Chỉ Quản Trị Viên Mới Được Dùng Lệnh Này).
-/restart: Khởi động lại bot (Chỉ admin).
- /admin: Hiển thị thông tin admin.
'''
  bot.reply_to(message, help_text)


@bot.message_handler(commands=['admin'])
def how_to(message):
  how_to_text = '''
 Thông Tin Admin:
- Nguyễn Chí Trung
🚀Thông Tin Liên Hệ ☎️:🚀
- Owner Telegram: https://t.me/yeuphchii
- Zalo: https://zalo.me/0962343184
- Facebook: https://facebook.com/caydodai.gaming.982
'''
  bot.reply_to(message, how_to_text)



@bot.message_handler(commands=['status'])
def status(message):
  user_id = message.from_user.id
  if user_id != ADMIN_ID:
    bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này😾.')
    return
  if user_id not in allowed_users:
    bot.reply_to(message, text='Bạn không có quyền sử dụng lệnh này😾.')
    return
  process_count = len(processes)
  bot.reply_to(message, f'Số quy trình đang xử lý {process_count}.')


@bot.message_handler(commands=['restart'])
def restart(message):
  user_id = message.from_user.id
  if user_id != ADMIN_ID:
    bot.reply_to(message, 'Đã khởi động lại bot')
    return

  bot.reply_to(message, 'Bot sẽ được khởi động lại sau 3s')
  time.sleep(2)
  python = sys.executable
  os.execl(python, python, *sys.argv)


@bot.message_handler(commands=['stop'])
def stop(message):
  user_id = message.from_user.id
  if user_id != ADMIN_ID:
    bot.reply_to(message, 'Bạn không có quyền Admin')
    return

  bot.reply_to(message, 'Đã dừng bot')
  time.sleep(2)
  bot.stop_polling()


bot.polling()
