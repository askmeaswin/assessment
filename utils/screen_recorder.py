import cv2
import numpy as np
import mss
import time
import threading

class ScreenRecorder:
    def __init__(self, output_file="recording.avi", fps=15):
        self.output_file = output_file
        self.fps = fps
        self.running = False
        self.thread = None

    def start_recording(self):
        self.running = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def _record(self):
        with mss.mss() as sct:
            screen_size = sct.monitors[1]["width"], sct.monitors[1]["height"]
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(self.output_file, fourcc, self.fps, screen_size)

            while self.running:
                frame = np.array(sct.grab(sct.monitors[1]))[:, :, :3]
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame)
                time.sleep(1 / self.fps)

            out.release()

    def stop_recording(self):
        self.running = False
        self.thread.join()
