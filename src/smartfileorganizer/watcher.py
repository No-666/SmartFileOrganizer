import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from .organizer import Organizer

console = Console()

class Handler(FileSystemEventHandler):
    def __init__(self, target: str):
        self.organizer = Organizer()
        self.target = target

    def on_created(self, event):
        if not event.is_directory:
            console.print(f"[yellow]检测到新文件[/yellow] {event.src_path}")
            self.organizer.organize(str(Path(event.src_path).parent), self.target, dry_run=False)

def start_watcher(source: str, target: str | None = None):
    if target is None:
        target = source + "_organized"
    event_handler = Handler(target)
    observer = Observer()
    observer.schedule(event_handler, source, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()