import signal
import sys
import time
from datetime import datetime
from pathlib import Path

from picamera2 import Picamera2
from picamera2.outputs import FileOutput
from picamera2.encoders import H264Encoder

SAVE_DIRECTORY = "/home/urd/Videos"
Path(SAVE_DIRECTORY).mkdir(parents=True, exist_ok=True)

picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (1920, 1080)})
picam2.configure(config)

def stop_recording(signum, frame):
  print("\nShutdown signal received. Saving video...")
  picam2.stop_recording()
  sys.exit(0)

signal.signal(signal.SIGTERM, stop_recording)
signal.signal(signal.SIGINT, stop_recording)

def start_auto_record():
  timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  filename = f"{SAVE_DIRECTORY}/rec_{timestamp}.h264"

  print(f"Starting recording: {filename}")
  picam2.start_recording(H264Encoder(), FileOutput(filename))

  while True:
    time.sleep(1)

if __name__ == "__main__":
  try:
    start_auto_record()
  except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)