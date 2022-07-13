import time
import json
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# C:\Users\brook\Downloads\
DOWNLOAD_DIRECTORY = os.path.join(os.path.expanduser('~'), 'Downloads')
EXTENSION_FILE = './extensions.json'


def init_extensions():
    with open(EXTENSION_FILE, 'r') as extensions:
        ext_list = json.load(extensions)
    return ext_list


def match_extension(file_extension):
    print(file_extension)
    categories = extension_list['categories']
    for category, ext_list in categories.items():
        if file_extension in ext_list:
            return category
    return 'Miscellaneous'


class Watcher:

    def __init__(self, directory='.', handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.observer.schedule(self.handler, self.directory, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()
        print("\nWatcher Terminated\n")


class DownloadDirHandler(FileSystemEventHandler):

    def on_created(self, event):
        print('New file by on_created')
        print(match_extension(os.path.splitext(event.src_path)[-1][1:]))

    def on_any_event(self, event):
        print('New event')


if __name__ == "__main__":
    extension_list = init_extensions()
    monitor = Watcher(DOWNLOAD_DIRECTORY, DownloadDirHandler())
    monitor.run()
