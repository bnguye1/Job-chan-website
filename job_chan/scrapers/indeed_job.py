"""
Usage: python indeed_job.py job_title state
"""

from datetime import datetime
from bs4 import BeautifulSoup as bs
from pathlib import Path
from more_itertools import unique_everseen
import csv
import requests
import re


def get_url(position, location, page):
    template = 'https://www.indeed.com/jobs?q={}&l={}&start={}&fromage=14'
    return template.format(position, location, page)


def extract_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')
        cards = soup.find_all('div', 'job_seen_beacon')

        jobs = []

        # Go through each job on the page
        for card in cards:
            job = card.h2.a.span.text
            job_url = 'https://www.indeed.com' + card.h2.a.get('href')

            company = card.find("span", attrs='companyName').text
            location = card.find("div", attrs={'class': 'company_location'}).div.text

            # Get the job salary if it exists
            try:
                salary = card.find("div", attrs={"class": "salary-snippet-container"}).text.strip()

            except AttributeError:
                salary = 'N/A'

            # Remove any misc text before the number of days
            post_date = card.find("span", attrs={"class": "date"}).text
            index = re.search(r"\d", post_date)
            if index is not None:
                post_date = post_date[int(index.start()):]

            today = datetime.today().strftime('%m-%d-%Y')

            if "pagead" not in job_url:
                if "PostedToday" in post_date or "PostedJust posted" in post_date:
                    post_date = "Today"

                data = (job, company, location, salary, post_date, today, job_url)
                jobs.append(data)

        return jobs


def start_scraping(position, location):
    # Grab jobs from the first 5 pages in the search
    for i in range(0, 70, 10):
        # search = sys.argv[1]
        # search = search.replace('_', ' ')
        # url = get_url('software engineer', 'maryland', i)
        url = get_url(position, location, i)

        job_list = extract_data(url)

        # The file doesn't exist
        if not Path('results.csv').is_file():
            with open('results.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(job_list)

        # The file exists
        else:
            with open('results.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(job_list)

    cleanse_csv()


# Removes the duplicates from the job list
def cleanse_csv():
    with open('results.csv', 'r', encoding='utf-8') as f, open('clean_results.csv', 'w', encoding='utf-8') as out:
        out.writelines(unique_everseen(f))

