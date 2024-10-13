# %%
### Requirements
import json
import os
import pandas as pd
from pathlib import Path

# %%
### Import path
with open('config.json') as config_file:
    config = json.load(config_file)
    script_path = Path(config['script_path'])

to_save = script_path / Path(f"filtered")  # Save into subfolder, 'filtered'
if not to_save.exists():
    os.makedirs(to_save)
    
files = [file.name for file in script_path.iterdir() if file.is_file()]

# %%
### Iter for 4 csv files
for file in files:
    print(f"Currently Working at {file}")
    
    cur_file = script_path / Path(file)
    df = pd.read_csv(cur_file)
    filtered_rows = []
    prev = {'Name' : None, 'Script' : None}  # Save the script just before
    queue = []  # Save continuous scripts of Aris
    
    ### Iter for each row
    for _, row in df.iterrows():
        if ('아리스' not in row['Name']):  # In case not a script from Aris
            if (prev['Script'] and queue):  # There is both a previous character's script and Aris' script
                new_row = {'Question' : prev['Script'], 'Answer' : queue}
                filtered_rows.append(new_row)  # Hence, we will append the pair
            queue = []  # Anyway, queue needs to be reset
            prev['Name'], prev['Script'] = row['Name'], row['Script']
        else:  # In case a script from Aris
            queue.append(row['Script'])  # Append a script to the queue
    
    filtered_df = pd.DataFrame(filtered_rows, columns=['Question', 'Answer'])
    filtered_df.to_csv(to_save / Path(f"filtered_{file}"), index=False)  # Save csv file


