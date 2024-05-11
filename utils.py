"""
Utilities

:author: LinuxUser255
:date: 2024-05-10
:version: 1.0

About
============
This file contains all the utility functions used in the main script.
Some of the code had been refactored, and in keeping within the PEP 8 naming-conventions,
all of the function names and variable names have been changed to lower case.

And, all of the methods contained within the class: "LinkedinUrlGenerate:"
have been converted to @staticmethod


References
==========
https://peps.python.org/pep-0008/#naming-conventions
Original Author: amimblm(https://github.com/aminblm)
Original Repository: https://github.com/aminblm/linkedin-application-bot
"""

import math, constants, config
from typing import List
import time

from selenium.webdriver.firefox.options import Options


def browser_options():
    options = Options()
    firefox_profile_root_dir = config.firefoxProfileRootDir
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-gpu')
    if (config.headless):
        options.add_argument("--headless")

    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")
    options.add_argument("-profile")
    options.add_argument(firefox_profile_root_dir)

    return options


def pr_red(prt: object) -> object:
    """

    :rtype: object
    """
    print(f"\033[91m{prt}\033[00m")


def pr_green(prt):
    print(f"\033[92m{prt}\033[00m")


def pr_yellow(prt):
    print(f"\033[93m{prt}\033[00m")


def get_url_data_file():
    urlData = ""
    try:
        file = open('data/urlData.txt', 'r')
        urlData = file.readlines()
    except FileNotFoundError:
        text = ("FileNotFound:urlData.txt file is not found. Please run ./data folder exists and check config.py "
                "values of yours. Then run the bot again")
        pr_red(text)
    return urlData


def jobs_to_pages(numOfJobs: str) -> int:
    number_of_pages = 1

    if ' ' in numOfJobs:
        space_index = numOfJobs.index(' ')
        total_jobs = (numOfJobs[0:space_index])
        total_jobs_int = int(total_jobs.replace(',', ''))
        number_of_pages = math.ceil(total_jobs_int / constants.jobsPerPage)
        if number_of_pages > 40: number_of_pages = 40

    else:
        number_of_pages = int(numOfJobs)

    return number_of_pages


def url_to_keywords(url: str) -> List[str]:
    keyword_url = url[url.index("keywords=") + 9:]
    keyword = keyword_url[0:keyword_url.index("&")]
    location_url = url[url.index("location=") + 9:]
    location = location_url[0:location_url.index("&")]
    return [keyword, location]


def write_results(text: str):
    time_str = time.strftime("%Y%m%d")
    file_name = "Applied Jobs DATA - " + time_str + ".txt"
    try:
        with open("data/" + file_name, encoding="utf-8") as file:
            lines = []
            for line in file:
                if "----" not in line:
                    lines.append(line)

        with open("data/" + file_name, 'w', encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " + time_str + "\n")
            f.write(
                "---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result " + "\n")
            for line in lines:
                f.write(line)
            f.write(text + "\n")

    except:
        with open("data/" + file_name, 'w', encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " + time_str + "\n")
            f.write(
                "---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result " + "\n")

            f.write(text + "\n")


def print_info_mes(bot: str):
    pr_yellow("ℹ️ " + bot + " is starting soon... ")


def donate(self):
    pr_yellow('If you like the project, please support me so that i can make more such projects, thanks!')
    try:
        self.driver.get('https://commerce.coinbase.com/checkout/576ee011-ba40-47d5-9672-ef7ad29b1e6c')
    except Exception as e:
        pr_red("Error in donate: " + str(e))


class LinkedinUrlGenerate:
    def generate_url_links(self):
        path = []
        for location in config.location:
            for keyword in config.keywords:
                url = constants.linkJobUrl + "?f_AL=true&keywords=" + keyword + self.job_type() + self.remote() + self.check_job_location(
                    location) + self.job_exp() + self.date_posted() + self.salary() + self.sort_by()
                path.append(url)
        return path

    @staticmethod
    def check_job_location(job):
        job_loc = "&location=" + job
        match job.casefold():
            case "asia":
                job_loc += "&geoId=102393603"
            case "europe":
                job_loc += "&geoId=100506914"
            case "northamerica":
                job_loc += "&geoId=102221843&"
            case "southamerica":
                job_loc += "&geoId=104514572"
            case "australia":
                job_loc += "&geoId=101452733"
            case "africa":
                job_loc += "&geoId=103537801"

        return job_loc

    @staticmethod
    def job_exp():
        jobt_exp_array = config.experienceLevels
        first_job_exp = jobt_exp_array[0]
        job_exp = ""
        match first_job_exp:
            case "Internship":
                job_exp = "&f_E=1"
            case "Entry level":
                job_exp = "&f_E=2"
            case "Associate":
                job_exp = "&f_E=3"
            case "Mid-Senior level":
                job_exp = "&f_E=4"
            case "Director":
                job_exp = "&f_E=5"
            case "Executive":
                job_exp = "&f_E=6"
        for index in range(1, len(jobt_exp_array)):
            match jobt_exp_array[index]:
                case "Internship":
                    job_exp += "%2C1"
                case "Entry level":
                    job_exp += "%2C2"
                case "Associate":
                    job_exp += "%2C3"
                case "Mid-Senior level":
                    job_exp += "%2C4"
                case "Director":
                    job_exp += "%2C5"
                case "Executive":
                    job_exp += "%2C6"

        return job_exp

    @staticmethod
    def date_posted():
        date_posted = ""
        match config.datePosted[0]:
            case "Any Time":
                date_posted = ""
            case "Past Month":
                date_posted = "&f_TPR=r2592000&"
            case "Past Week":
                date_posted = "&f_TPR=r604800&"
            case "Past 24 hours":
                date_posted = "&f_TPR=r86400&"
        return date_posted

    @staticmethod
    def job_type():
        job_type_array = config.jobType
        first_type = job_type_array[0]
        job_type = ''
        match first_type:
            case "Full-time":
                job_type = "&f_JT=F"
            case "Part-time":
                job_type = "&f_JT=P"
            case "Contract":
                job_type = "&f_JT=C"
            case "Temporary":
                job_type = "&f_JT=T"
            case "Volunteer":
                job_type = "&f_JT=V"
            case "Intership":
                job_type = "&f_JT=I"
            case "Other":
                job_type = "&f_JT=O"
        for index in range(1, len(job_type_array)):
            match job_type_array[index]:
                case "Full-time":
                    job_type += "%2CF"
                case "Part-time":
                    job_type += "%2CP"
                case "Contract":
                    job_type += "%2CC"
                case "Temporary":
                    job_type += "%2CT"
                case "Volunteer":
                    job_type += "%2CV"
                case "Intership":
                    job_type += "%2CI"
                case "Other":
                    job_type += "%2CO"
        job_type += "&"
        return job_type

    @staticmethod
    def remote():
        remote_array = config.remote
        first_job_remote = remote_array[0]
        job_remote = ""
        match first_job_remote:
            case "On-site":
                job_remote = "f_WT=1"
            case "Remote":
                job_remote = "f_WT=2"
            case "Hybrid":
                job_remote = "f_WT=3"
        for index in range(1, len(remote_array)):
            match remote_array[index]:
                case "On-site":
                    job_remote += "%2C1"
                case "Remote":
                    job_remote += "%2C2"
                case "Hybrid":
                    job_remote += "%2C3"

        return job_remote

    @staticmethod
    def salary():
        salary = ""
        match config.salary[0]:
            case "$40,000+":
                salary = "f_SB2=1&"
            case "$60,000+":
                salary = "f_SB2=2&"
            case "$80,000+":
                salary = "f_SB2=3&"
            case "$100,000+":
                salary = "f_SB2=4&"
            case "$120,000+":
                salary = "f_SB2=5&"
            case "$140,000+":
                salary = "f_SB2=6&"
            case "$160,000+":
                salary = "f_SB2=7&"
            case "$180,000+":
                salary = "f_SB2=8&"
            case "$200,000+":
                salary = "f_SB2=9&"
        return salary

    @staticmethod
    def sort_by():
        sort_by = ""
        match config.sort[0]:
            case "Recent":
                sort_by = "sort_by=DD"
            case "Relevent":
                sort_by = "sort_by=R"
        return sort_by
