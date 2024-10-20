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

# %%
### Import path
with open('config.json') as config_file:
    dataset_path = Path(json.load(config_file)['dataset_path'])

### Use only text data from 4 sources
dataset = pd.read_csv(dataset_path / Path("dataset.csv"))
dataset = dataset[dataset['File'].isin(['filtered_sub_maid.mp4_final',
                                        'filtered_sub_original.mp4_final',
                                        'momotalk_maid',
                                        'momotalk_original'])]

### Create a prompt and save it as a jsonl file
def save_to_jsonl(data, output_file_path):
    jsonl_data = []
    for _, row in data.iterrows():
        jsonl_data.append({
            "messages": [
                {"role": "system", "content": "너는 '블루 아카이브'라는 게임에 등장하는 캐릭터 '아리스'야. 내가 묻는 질문에 대해 '아리스' 답게 대답해 줘."},
                {"role": "user", "content": row['Input']},
                {"role": "assistant", "content": row['Output']}
            ]
        })
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for item in jsonl_data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

output_file_path = dataset_path / Path("train_dataset.jsonl")
save_to_jsonl(dataset, output_file_path)