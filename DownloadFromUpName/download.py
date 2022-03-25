import logging
import os
from urllib.request import urlretrieve
import mysql.connector
import csv
import re
from datetime import datetime
import urllib.parse

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)


def connect_db():
    dbSge = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB')
    )

    return dbSge


def get_bills():
    with open('.\DownloadList.csv') as csvfile:
        downloadlist = list(csv.reader(csvfile))
    bills = []
    for row in downloadlist:
        ## SPLIT
        row = row[0].split(';')
    ## ZIPS
        ## DOWNLOADDIR
        path = "./download/"
        os.makedirs(path, exist_ok=True)
        ## URL TREATMENT
        url = urllib.parse.unquote(row[0])
        filename = url.rsplit('/',1)[-1]
        download_link(path, filename, row[0])
        print(url)
    ## XLSX
        ## DOWNLOADDIR
        path = "./download/"
        os.makedirs(path, exist_ok=True)
        ## URL TREATMENT
        url = urllib.parse.unquote(row[1])
        filename = url.rsplit('/',1)[-1]
        download_link(path, filename, row[1])
        print(url)

    return bills


def download_link(directory, filename, link):
    download_path = directory + filename
    urlretrieve(link, filename=download_path)

    return download_path


if __name__ == '__main__':
    for bill in get_bills():
        print(bill)
