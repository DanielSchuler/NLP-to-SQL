


step 1 have python

step 2 have an ID like pycham or visual studio code.

step 3 run the requirements.txt
pip install -r requirements.txt

step 4) have an open ai api key account

https://platform.openai.com/

create a .env file add OPENAI_API_KEY



explanation:

the main file specifies the name of the file that should be in the data folder in csv format

the system reads the csv from the data folder at the time of running the script.

validates the different encodings (utf-8, latin-1 and utf-16) to avoid character errors.

column titles are transformed if they have words separated by spaces. these are changed by the same words joined by _

at the prompt presents the names of the columns.

The user must know in part which are the types of data that exist within the csv.

When the user makes a report request, the schema of the table is sent to gpt3, but not the information.
With this scheme and the question gpt3 generates the query that is then executed and the result is presented
to the person who requested it.


example data:

1) Current pro meta DOTA csv
2) data science jobs csv
3) data scientist salaries 2023 csv
4) laptop prices csv
5) sales data sample csv
