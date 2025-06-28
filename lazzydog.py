import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

path_point = os.path.join("point")
script = os.path.join("scanrex.py")

def run_script(script):
    try:
        with open(script, "r") as f:
            run = f.read()
        exec(run)
    except FileNotFoundError:
        print(f"Não foi encontrado nada no caminho {script}")
    except Exception as e:
        print(f"Erro ao executar o script {e}")

class MyEventHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        run_script(script)

event_handler = MyEventHandler()
observer = Observer()
observer.schedule(event_handler, path_point, recursive=True)
observer.start()

os.system("clear")
print("Lazzy dog is run-time...")

try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()



