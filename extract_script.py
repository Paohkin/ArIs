# %%
### Requirements
import cv2
import easyocr
import json
import os
import re
import shutil
import csv
import numpy as np
from pathlib import Path

# %%
### Extract only numbers from a file name
def extract_number(file):
    match = re.search(r'\d+', file.stem)
    return int(match.group()) if match else 0

# %%
### Import path
with open('config.json') as config_file:
    config = json.load(config_file)
    capture_path = Path(config['capture_path'])
    script_path = Path(config['script_path'])
    
### Read folder names in the capture path
folders = [folder.name for folder in capture_path.iterdir() if folder.is_dir()]

# %%
### Collect only images containing completed scripts using a reference image
ref = cv2.imread(capture_path / Path("ref.png"))
x, y, w, h = 1650, 850, 100, 100  # Position of blue triangle(implies the script is complete)

### Iter through 4 folders
for folder in folders:
    print(f"Currently Working at {folder}")
    
    cur_folder = capture_path / Path(folder)
    to_save_match = cur_folder / Path("matched")  # Completed scripts
    if not to_save_match.exists(): os.makedirs(to_save_match)
    to_save_unmatch = cur_folder / Path("unmatched")  # Uncompleted scripts
    if not to_save_unmatch.exists(): os.makedirs(to_save_unmatch)

    captures = [image for image in cur_folder.iterdir() if image.is_file()]
    cnt = 0  # Count to check progress
    
    ### Iter through captured images
    for image in captures:
        roi = cv2.imread(image)[y:y+h, x:x+w]
        result = cv2.matchTemplate(roi, ref, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(result >= threshold)
        
        if len(loc[0]):  # If matches
            shutil.copy(image, to_save_match)
        else:  # If unmatches
            shutil.copy(image, to_save_unmatch)
        
        cnt += 1        
        if (cnt%1000 == 0):
            print(f"Now Working... {cnt}/{len(captures)}")  # Print progress

# %%
reader = easyocr.Reader(['ko', 'en'])  # Load EasyOCR model
character_box = (230, 680, 500, 70)  # Position of character box
script_box = (230, 760, 1500, 200)  # Position of script box

### Iter through 4 folders
for folder in folders:
    print(f"Currently Working at {folder}")
    
    work_dir = capture_path / Path(folder) / Path("matched")
    captures = sorted([image for image in work_dir.iterdir() if image.is_file()],
                      key=extract_number)  # frame3 must come before frame10
    scripts = []  # New rows
    cnt = 0
    
    for image in captures:
        (chr_x, chr_y, chr_w, chr_h), (scr_x, scr_y, scr_w, scr_h) = character_box, script_box 
        roi_chr = cv2.bitwise_not(cv2.cvtColor(cv2.imread(image)[chr_y:chr_y+chr_h, chr_x:chr_x+chr_w], cv2.COLOR_BGR2GRAY))  # Grayscale, then invert
        roi_scr = cv2.bitwise_not(cv2.cvtColor(cv2.imread(image)[scr_y:scr_y+scr_h, scr_x:scr_x+scr_w], cv2.COLOR_BGR2GRAY))  # Grayscale, then invert
        result_chr = reader.readtext(roi_chr, detail=0)  # Get only texts
        result_scr = reader.readtext(roi_scr, detail=0)  # Get only texts
        
        cnt += 1       
        if not (result_chr and result_scr):  # In case if no character and script
            if (cnt%100 == 0):
                print(f"Now Working... {cnt}/{len(captures)}")
            continue
        
        row = {}
        if (result_chr[0] == ''):  # In case if no character
            row['Name'] = row['Club'] = None
        else:
            if (' ' in result_chr[0]):  # In case if club exists
                row['Name'], row['Club'] = result_chr[0].split()[:-1], result_chr[0].split()[-1]
            else:  # In case if no club
                row['Name'], row['Club'] = [result_chr[0]], None

        row['Script'] = result_scr[0]
        scripts.append(row)
        
        if (cnt%100 == 0):
            print(f"Now Working... {cnt}/{len(captures)}")  # Print progress
        
    to_save = script_path
    if not to_save.exists():
        os.makedirs(to_save)
    
    with open(to_save / Path(f"{folder}.csv"), mode='w', encoding='utf-8-sig', newline='') as file:
        fields = ['Name', 'Club', 'Script']
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(scripts)
    
    print(f"{folder}.csv has been saved")


