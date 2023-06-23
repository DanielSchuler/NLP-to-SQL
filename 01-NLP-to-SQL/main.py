# Dataset based on #https://www.kaggle.com/datasets/kyanyoga/sample-sales-data
from dotenv import load_dotenv
import os
import logging
import pprint
import pandas as pd
import openai

import db_utils
import openai_utils
# Load environment variables from .env
load_dotenv()
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
openai.api_key = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    file_name='ds_salaries.csv'
    database_name=file_name.split('.')[0]
    file_path='data/'
    file_fullpath=file_path+file_name
    logging.info("Loading data...")
    #df = pd.read_csv("data/sales_data_sample.csv")
    try:
        df = pd.read_csv(file_fullpath, encoding='utf-8')
    except UnicodeDecodeError:
        # Try reading with alternative encodings
        try:
            df = pd.read_csv(file_fullpath, encoding='latin-1')
        except UnicodeDecodeError:
            df = pd.read_csv(file_fullpath, encoding='utf-16')
    logging.info(f"Data Format: {df.shape}")
    # Replace whitespaces with underscores in column names
    df.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
    # Print the modified column names
    print(df.columns)
    logging.info("Converting to database...")
    database = db_utils.dataframe_to_database(df, database_name)
    
    fixed_sql_prompt = openai_utils.create_table_definition_prompt(df, database_name)
    logging.info(f"Fixed SQL Prompt: {fixed_sql_prompt}")

    logging.info("Waiting for user input...")
    user_input = openai_utils.user_query_input()
    final_prompt = openai_utils.combine_prompts(fixed_sql_prompt, user_input)
    logging.info(f"Final Prompt: {final_prompt}")

    logging.info("Sending to OpenAI...")
    response = openai_utils.send_to_openai(final_prompt)
    proposed_query = response["choices"][0]["text"]
    proposed_query_postprocessed = db_utils.handle_response(response)
    logging.info(f"Response obtained. Proposed sql query: {proposed_query_postprocessed}")
    result = db_utils.execute_query(database, proposed_query_postprocessed)
    logging.info(f"Result: {result}")
    pprint.pprint(result)