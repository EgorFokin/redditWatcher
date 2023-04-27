import time
from pmaw import PushshiftAPI
import csv
import os, sys
import json
from datetime import datetime, timedelta
import eel

# define a storage folder to store the downloaded data
STORAGE_FOLDER = "raw"

# initialize eel
eel.init("web")


# function to fetch data from the Pushshift API
@eel.expose
def fetch_data(subreddit, since, until):
    # convert since and until strings to Unix timestamps
    since_timestamp = int(datetime.strptime(since, '%Y-%m-%d').timestamp())
    until_timestamp = int(datetime.strptime(until, '%Y-%m-%d').timestamp())

    # create a folder to store the subreddit data
    folder = os.path.join(STORAGE_FOLDER, subreddit)
    if not os.path.exists(folder):
        os.makedirs(folder)
    # create a file to store the subreddit data
    file_path = os.path.join(folder, f"submissions_{int(datetime.now().timestamp())}.csv")

    # open the csv file for writing
    csvfile = open(file_path, 'w+', encoding='utf-8')
    fieldnames = ['timestamp', 'title']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    api = PushshiftAPI(num_workers=20)
    submissions = api.search_submissions(subreddit=subreddit, since=since_timestamp, until=until_timestamp,
                                         mem_safe=True)
    submission_count = len(submissions)
    for i, submission in enumerate(submissions):
        writer.writerow({'timestamp': submission['created_utc'], 'title': submission['title']})

    csvfile.close()
    result = {'file_path': file_path, 'submission_count': submission_count}
    return result


# start the user interface
eel.start("index.html", size=(800, 600))
