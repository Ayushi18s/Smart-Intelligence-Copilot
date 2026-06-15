import time
from threading import Thread

scheduled_tasks = []

def schedule_report(func, interval_seconds=60):

    def run():
        while True:
            func()
            time.sleep(interval_seconds)

    thread = Thread(target=run)
    thread.daemon = True
    thread.start()

def add_task(task_name):
    scheduled_tasks.append(task_name)