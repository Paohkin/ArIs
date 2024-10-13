# %%
### Requirements
import cv2
import json
import os
from pathlib import Path

# %%
### Import video path
with open('config.json') as config_file:
    config = json.load(config_file)
    video_path = Path(config['video_path'])
    capture_path = Path(config['capture_path'])

### Read file names in the video path
file_names = [file.name for file in video_path.iterdir() if file.is_file()]

# %%
### Set parameters
start_time = {'main_2-1.mp4' : 1243, 'main_2-2.mp4' : 0,
              'sub_maid.mp4' : 0, 'sub_original.mp4' : 0}  # No need of the front of main_2-1
fps_limit = 2

### Iter through 4 files
for file_name in file_names:
    print(f"Currently Capturing {file_name}")
    
    file = video_path / Path(file_name)
    vidcap = cv2.VideoCapture(file)
    cur_start = start_time[file_name]
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_interval = round(fps / fps_limit)  # e.g. 30fps/2fps = 15 frame interval
    count = 0  # Count to check interval
    
    to_save = capture_path / Path(file_name)  # Output path
    if not to_save.exists():
        os.makedirs(to_save)
        
    total_frame = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total frames
    success, image = vidcap.read()
    cur_time = vidcap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Convert into sec
    
    ### Read each frame from the file
    while success:
        if count%1000 == 0:
            print(f"Now Working... {count}/{total_frame}")  # Print progress
        
        if cur_start <= cur_time and count%frame_interval == 0:  # Save if condition meets
            cv2.imwrite(to_save / Path(f"frame{count // frame_interval}.png"), image)

        success, image = vidcap.read()
        cur_time = vidcap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Convert into sec
        count += 1
    
    vidcap.release()


