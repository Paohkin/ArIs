# %%
import json
from openai import OpenAI

# %%
with open('config.json') as config_file:
    config = json.load(config_file)
    openai_api_key = config['OPENAI_KEY']
    training_file_name = config['training_file_name']
    
client = OpenAI(api_key=openai_api_key)

client.fine_tuning.jobs.create(
  training_file=training_file_name,
  model="gpt-4o-mini-2024-07-18",
  seed=149
)