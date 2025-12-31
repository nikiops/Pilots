import subprocess
import time
import os

os.chdir(r'd:\TgWork\TgWork\telegram-bot')

print("Starting NGROK...")
subprocess.Popen(['ngrok', 'http', '3000'])
time.sleep(3)

print("Updating NGROK URL...")
subprocess.run(['python', 'ngrok_helper.py'])

print("\nStarting WebApp server...")
subprocess.Popen(['python', r'webapp\server.py'])

print("Starting Telegram Bot...")
subprocess.Popen(['python', 'main.py'])

print("\nAll services started!")
print("Press Ctrl+C to stop")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutdown")
