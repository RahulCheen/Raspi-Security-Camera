import time
import os
from subprocess import call
from datetime import datetime
import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from libcamera import controls
import cv2

# Helper function to flip video because I installed my camera upside-down :P
def flip_video(video_path):
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'avc1') # Use AVC codec so videos will embed in discord DMs for easy viewing
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_out = cv2.VideoWriter(video_path[:-4]+'_flipped.mp4', fourcc, fps, (width, height)) # Creates VideoWriter object to save output video using same dimensions/framerate as input video 
    
    while video.isOpened(): # Loops through every frame of the video
        ret, frame = video.read()
        if ret:
            flipped_frame = cv2.flip(frame, 0) # Flips frame vertically
            video_out.write(flipped_frame)
        else:
            break
                
    video.release()
    video_out.release()
    os.remove(video_path) # Deletes input video to avoid clogging up local storage

time_format = "%Y-%m-%d_%H-%M-%S"
frame_rate = 30
lsize = (320, 180)
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"},
                                                lores={"size": lsize, "format": "YUV420"}) # Set video recording properties
picam2.configure(video_config)
picam2.set_controls({"FrameRate": frame_rate})
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
encoder = H264Encoder(bitrate=4000000, repeat=True)
encoder.output = CircularOutput()
picam2.encoder = encoder
picam2.start()
picam2.start_encoder()

w, h = lsize
prev = None
encoding = False
ltime = 0

while True:
    cur = picam2.capture_buffer("lores")
    cur = cur[:w * h].reshape(h, w)
    if prev is not None:
        mse = np.square(np.subtract(cur, prev)).mean() # Motion detection via simple frame differencing
        if mse > 6: # When motion is detected
            if not encoding:
                print("Motion detected")
                filename = datetime.now().strftime(time_format)
                encoder.output.fileoutput = f"./video_cache/{filename}.h264"
                encoder.output.start()
                encoding = True
                print("Starting recording")
            ltime = time.time()
        else:
            if encoding and time.time() - ltime > 5.0: # Stops recording after 5 seconds of no motion
                print("Saving video")
                encoder.output.stop()
                encoding = False
                time.sleep(1)
                print("Transcoding video") # Uses MP4Box to transcode h264 video to mp4
                input_file = f"./video_cache/{filename}.h264"
                output_file = f"./video_cache/{filename}.mp4"
                command = f"MP4Box -add {input_file} {output_file}"
                call(command, shell=True)
                os.remove(input_file) # Deletes h264 file to avoid clogging local storage
                print("Done recording")
                flip_video(output_file) # Flips video because my camera is upside-down
                print("Video Flipped")
                time.sleep(60) # Wait 60 seconds to avoid duplicate alerting for same instance of motion
    prev = cur

picam2.stop_encoder()
picam2.stop()
