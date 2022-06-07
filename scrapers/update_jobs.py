from scrapers.indeed_job import start_scraping
import csv
# import sys, os
# import time
#

def get_list_of_jobs(position, location):
    start_scraping(position, location)
    jobs = []
    with open('clean_results.csv', mode='r') as file:
        csvfile = csv.reader(file)

        for job in csvfile:
            jobs.append(job)

    return jobs

