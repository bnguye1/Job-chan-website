from .indeed_job import start_scraping
from pathlib import Path
import csv
import os


def get_list_of_jobs(position, location):
    start_scraping(position, location)
    jobs = []
    with open('clean_results.csv', mode='r', encoding='utf-8') as file:
        csvfile = csv.reader(file)

        for job in csvfile:
            jobs.append(job)

    return jobs


def delete_csv():
    if Path('clean_results.csv').is_file:
        os.remove('clean_results.csv')

    if Path('results.csv').is_file:
        os.remove('results.csv')

