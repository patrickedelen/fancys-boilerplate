import os
import signal
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class CeleryReloader(FileSystemEventHandler):
    def __init__(self):
        self.celery_process = None
        self.restart_celery()

    def restart_celery(self):
        if self.celery_process:
            os.killpg(os.getpgid(self.celery_process.pid), signal.SIGTERM)
        self.celery_process = subprocess.Popen(
            ['celery', '-A', 'worker.app', 'worker', '--loglevel=info'],
            preexec_fn=os.setsid
        )

    def on_any_event(self, event):
        self.restart_celery()


if __name__ == "__main__":
    event_handler = CeleryReloader()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
