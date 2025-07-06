import subprocess
import time
import os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

date = datetime.now().strftime("%d-%m-%Y")
path_point = os.path.join("point")
script = os.path.join("scanrex.py")
log_file = os.path.join("log", f"registro_{date}.log")
clear = 'clear'

if os.name != 'posix':
    clear = 'cls'

def run_script(script):
    try:
        subprocess.run(['python', 'scanrex.py'])
    except Exception as e:
        print(f"Houve erro ao executar o script: {e}")

class RexLeu(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        if not event.is_directory and event.src_path.endswith(".txt"):
            time.sleep(0.5)
            if os.path.exists(event.src_path) and os.path.getsize(event.src_path) > 0:
                run_script(script)
            else:
                print("Não foi possivel ler o arquivo.")

class LogHandler(FileSystemEventHandler):
    def __init__(self, log_file):
        self.log_file = log_file

    def log_event(self, path):
        filename = os.path.basename(path)
        with open(self.log_file, "a", encoding="latin1") as log:
            now = datetime.now().strftime("%d-%m-%Y | %H:%M:%S")
            log.write(f"[{now}] LIDO: {filename}\n")
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.log_event(event.src_path)

Rex_event = RexLeu()
Log_event = LogHandler(log_file)
observer1 = Observer()
observer2 = Observer()
observer1.schedule(Rex_event, path_point, recursive=True)
observer2.schedule(Log_event, path_point, recursive=True)
observer1.start()
observer2.start()

os.system(clear)
print("Lazzy dog is run-time...")

try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()



