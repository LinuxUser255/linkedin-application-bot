#!/usr/bin/env python3

"""
===============
Automated Linkedin Job application bot
===============

:author: LinuxUser255
:date: 2024-05-10
:version: 1.0

Introduction
============
A python bot to apply all Linkedin Easy Apply jobs based on your preferences.
This one version logs you in and applying to each job individually.

About this fork - edited using Python version 3.12
================
Some of the code has been refactored, and in keeping within the PEP 8 naming-conventions,
all of the function names and variable names have been changed to lower case.
These changes are reflected in utils.py, as linkein.py
Tip: Avoid security checkpoints/captchas by storing your login creds in the browser
by using Firefox and storing your profile data in /env/.env

End Goal: what this is suppossed to do:
========================================
1. Launch just one selenium browser instance & auto logged into my account

2. have linkedin.py search and apply for all jobs based on your config.py specs

3. Have it iterate/repeate this process untill all jobs have been applied to

4. and all non fast apply jobs have had their urls logged in /data/urlData.txt


TO DO
============
- [x] ~~Sort out the Firefox Profile config~~
- [x] **Resolve inability to login using the Firefox Profile option**
- [x] ~~**Auto login with the test.py script:**~~ Resoved by creating a `env` dir and a `.env` file containing `firefox_profile_root_dir = r""`
- [x] Refactor and clean up the Linkedin Class block of code in linkedin.py
- [ ] **NEED To AUTO LOGIN using firefox profile in the .env file `linkedin.py` script**
- [ ] **Fix the [find_element "xpath" issues](https://selenium-python.readthedocs.io/locating-elements.html).**
- [ ] Eliminate launching a new browser/login session with each iteration: **Using Firefox profile resolves this**
- [ ] Conduct all searches and applications within one browser session.
- [ ] Forget Chrome, Just use firefox, it's easier to automate.
- [ ] ---
- [ ] Implement Headless browser experience (run the bot without launching the browser)
- [ ] Add More robustness of the bot for different fields
- [ ] Blacklist offers in Linkedin
- [ ] Output not completed fields in Linkedin
- [ ] Add support to other major job seeking websites:
- [ ] [Indeed](https://www.indeed.com/)
- [ ] [Glassdoor](https://www.glassdoor.com/index.htm)
- [ ] [AngelCo](https://angel.co/l/2xRADV) And possibly Greenhouse, Monster, GLobalLogic, and djinni.

References
==========
Original Author: amimblm(https://github.com/aminblm)
Original Repository: https://github.com/aminblm/linkedin-application-bot
"""

import math
import os
import platform
import random
import time
from typing import Union

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import config
import constants
import utils
from utils import pr_red, pr_yellow, pr_green

class Linkedin:

    def __init__(self) -> None:
        """
        Initialize LinkedIn class.
        Login to LinkedIn using the firefox_profile_root_dir located in the .env file.
        """
        self.driver = self.get_webdriver()
        self.login()

    def get_webdriver(self) -> webdriver.Remote:
        """
        Get the appropriate webdriver based on the specified browser.

        Returns:
        webdriver.Remote: The webdriver instance.
        """
        browser = config.browser[0].lower()
        browser_mapping = {
            "firefox": webdriver.Firefox,
            "chrome": webdriver.Chrome
        }

        if browser in browser_mapping:
            return browser_mapping[browser]()
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        def login(self) -> None:
        """
        Login to LinkedIn using the firefox_profile_root_dir located in the .env file.
        """
        # if config.firefox_profile_root_dir!= "":
        try:
            # Intended operation. But not working.
            # Use the current logged in firefox instance
            # and conduct all searches and applications within that browser session.
            self.driver = webdriver.Firefox(options=utils.browser_options())
            # Login to LinkedIn using the firefox_profile_root_dir located in the .env file.
            self.driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
            # Begin job search according to the specified criteria in the config file.
            self.driver.get("https://www.linkedin.com/jobs/?=")
            time.sleep(5)
            pr_yellow("Attempting to log into linkedin...")
        except Exception as e:
            pr_red(e)

    @staticmethod
    def generate_urls() -> None:
        """
        Generate LinkedIn job URLs based on the specified criteria in the config file.

        This function creates a directory named 'data' if it doesn't exist, then it opens a file named 'urlData.txt' in write mode.
        It generates LinkedIn job URLs by calling the 'generate_url_links' method of the 'utils.LinkedinUrlGenerate' class.
        These URLs are then written into the 'urlData.txt' file, one URL per line.
        If any error occurs during the process, it prints an error message using the 'pr_red' function.

        Parameters:
        None

        Returns:
        None

        Raises:
        Exception: If any error occurs while creating the directory, opening the file, or writing to the file.
        """
        if not os.path.exists('data'):
            os.makedirs('data')
        try:
            with open('data/urlData.txt', 'w', encoding="utf-8") as file:
                linkedin_job_links = utils.LinkedinUrlGenerate().generate_url_links()
                for url in linkedin_job_links:
                    file.write(url + "\n")
            pr_green("Urls are created successfully, now the bot will visit those urls.")
        except:
            pr_red(
                "Couldnt generate url, make sure you have /data folder and modified config.py file for your "
                "preferances.")

    def link_job_apply(self) -> None:
        """
        This method is responsible for applying to jobs based on the generated URLs.
        It navigates through the job search pages, retrieves job details, and applies to the jobs.

        Parameters:
        self (LinkedIn): The instance of the Linkedin class.

        Returns:
        None

        Raises:
        Exception: If any error occurs during the execution of the method.
        """
        self.generate_urls()
        count_applied = 0
        count_jobs = 0

        url_data = utils.get_url_data_file()

        for url in url_data:
            self.driver.get(url)
            try:
                total_jobs = self.driver.find_element(By.XPATH, '//small').text
            except:
                print("No Matching Jobs Found")
                continue
            total_pages = utils.jobs_to_pages(total_jobs)

            url_words = utils.url_to_keywords(url)
            line_to_write = "\n Category: " + url_words[0] + ", Location: " + url_words[1] + ", Applying " + str(
                total_jobs) + " jobs."
            self.display_write_results(line_to_write)

            for page in range(total_pages):
                current_page_jobs = constants.jobsPerPage * page
                url = url + "&start=" + str(current_page_jobs)
                self.driver.get(url)
                time.sleep(random.uniform(1, constants.botSpeed))

                offers_per_page = self.driver.find_elements(By.XPATH, '//li[@data-occludable-job-id]')

                offer_ids = []
                for offer in offers_per_page:
                    offer_id = offer.get_attribute("data-occludable-job-id")
                    offer_ids.append(int(offer_id.split(":")[-1]))

                for jobID in offer_ids:
                    offer_page = 'https://www.linkedin.com/jobs/view/' + str(jobID)
                    self.driver.get(offer_page)
                    time.sleep(random.uniform(1, constants.botSpeed))

                    count_jobs += 1

                    job_properties = self.get_job_properties(count_jobs)

                    button = self.easy_apply_button()

                    if button is not False:
                        button.click()
                        time.sleep(random.uniform(1, constants.botSpeed))
                        count_applied += 1
                        try:
                            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
                            time.sleep(random.uniform(1, constants.botSpeed))

                            line_to_write = job_properties + " | " + "* 🥳 Just Applied to this job: " + str(offer_page)
                            self.display_write_results(line_to_write)

                        except:
                            try:
                                self.driver.find_element(By.CSS_SELECTOR,
                                                         "button[aria-label='Continue to next step']").click()
                                time.sleep(random.uniform(1, constants.botSpeed))
                                com_percentage = self.driver.find_element(By.XPATH,
                                                                          'html/body/div[3]/div/div/div[2]/div/div/span').text
                                percen_number = int(com_percentage[0:com_percentage.index("%")])
                                result = self.apply_process(percen_number, offer_page)
                                line_to_write = job_properties + " | " + result
                                self.display_write_results(line_to_write)

                            except Exception as e:
                                try:
                                    self.driver.find_element(By.CSS_SELECTOR,
                                                             "option[value='urn:li:country:" + config.country_code + "']").click()
                                    time.sleep(random.uniform(1, constants.botSpeed))
                                    self.driver.find_element(By.CSS_SELECTOR, 'input').send_keys(config.phone_number)
                                    time.sleep(random.uniform(1, constants.botSpeed))
                                    self.driver.find_element(By.CSS_SELECTOR,
                                                             "button[aria-label='Continue to next step']").click()
                                    time.sleep(random.uniform(1, constants.botSpeed))
                                    com_percentage = self.driver.find_element(By.XPATH,
                                                                              'html/body/div[3]/div/div/div[2]/div/div/span').text
                                    percen_number = int(com_percentage[0:com_percentage.index("%")])
                                    result = self.apply_process(percen_number, offer_page)
                                    line_to_write = job_properties + " | " + result
                                    self.display_write_results(line_to_write)
                                except Exception as e:
                                    line_to_write = job_properties + " | " + "* 🥵 Cannot apply to this Job! " + str(
                                        offer_page)
                                    self.display_write_results(line_to_write)
                    else:
                        line_to_write = job_properties + " | " + "* 🥳 Already applied! Job: " + str(offer_page)
                        self.display_write_results(line_to_write)

            pr_yellow("Category: " + url_words[0] + "," + url_words[1] + " applied: " + str(count_applied) +
                      " jobs out of " + str(count_jobs) + ".")

        # utils.donate(self)

    def get_job_properties(self, count: int) -> str:
        """
        This function retrieves and formats the properties of a job from the LinkedIn job page.

        Parameters:
        count (int): The count of the job being processed.

        Returns:
        str: A formatted string containing the job properties.

        The function retrieves the job title, company, location, workplace type, posted date, and number of applications
        from the LinkedIn job page and formats them into a single string.
        """
        text_to_write = ""
        job_title = ""
        job_company = ""
        job_location = ""
        job_work_place = ""
        job_posted_date = ""
        job_applications = ""

        try:
            job_title = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'job-title')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            pr_yellow("Warning in getting job_title: " + str(e)[0:50])
            job_title = ""
        try:
            job_company = self.driver.find_element(By.XPATH,
                                                   "//a[contains(@class, 'ember-view t-black t-normal')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            pr_yellow("Warning in getting job_company: " + str(e)[0:50])
            job_company = ""
        try:
            job_location = self.driver.find_element(By.XPATH, "//span[contains(@class, 'bullet')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            pr_yellow("Warning in getting job_location: " + str(e)[0:50])
            job_location = ""
        try:
            job_work_place = self.driver.find_element(By.XPATH,
                                                      "//span[contains(@class, 'workplace-type')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            pr_yellow("Warning in getting jobWorkPlace: " + str(e)[0:50])
            job_work_place = ""
        try:
            job_posted_date = self.driver.find_element(By.XPATH,
                                                       "//span[contains(@class, 'posted-date')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            pr_yellow("Warning in getting job_posted_date: " + str(e)[0:50])
            job_posted_date = ""
        try:
            job_applications = self.driver.find_element(By.XPATH,
                                                        "//span[contains(@class, 'applicant-count')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            pr_yellow("Warning in getting job_applications: " + str(e)[0:50])
            job_applications = ""

        text_to_write = str(
            count) + " | " + job_title + " | " + job_company + " | " + job_location + " | " + job_work_place + " | " + job_posted_date + " | " + job_applications
        return text_to_write

    def easy_apply_button(self) -> Union[WebElement, bool]:
        """
        This method is used to find the 'Easy Apply' button on LinkedIn job pages.

        Parameters:
        self (Linkedin): The instance of the Linkedin class.

        Returns:
        selenium.webdriver.remote.webelement.WebElement or bool:
            Returns the 'Easy Apply' button if found, otherwise returns False.

        Raises:
        Exception: If any error occurs during the execution of the method.
        """
        try:
            # Find the 'Easy Apply' button using the XPath selector.
            button = self.driver.find_element(By.XPATH,
                                              '//button[contains(@class, "jobs-apply-button")]')
            easy_apply_button = button
        except:
            # If the 'Easy Apply' button is not found, return False.
            easy_apply_button = False

        return easy_apply_button

    def apply_process(self, percentage: int, offer_page: str) -> str:
        """
        This method calculates the number of pages to navigate through the LinkedIn application process based on the given
        percentage and then performs the application process.

        Parameters:
        self (Linkedin): The instance of the Linkedin class.
        percentage (int): The percentage of the application process completed.
        offer_page (str): The URL of the LinkedIn job offer page.

        Returns:
        str: A string indicating the result of the application process.

        Raises:
        Exception: If any error occurs during the execution of the method.
        """
        apply_pages = math.floor(100 / percentage)
        result = ""
        try:
            for pages in range(apply_pages - 2):
                self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()
                time.sleep(random.uniform(1, constants.botSpeed))

            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Review your application']").click()
            time.sleep(random.uniform(1, constants.botSpeed))

            if config.followCompanies is False:
                self.driver.find_element(By.CSS_SELECTOR, "label[for='follow-company-checkbox']").click()
                time.sleep(random.uniform(1, constants.botSpeed))

            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
            time.sleep(random.uniform(1, constants.botSpeed))

            result = "* 🥳 Just Applied to this job: " + str(offer_page)
        except:
            result = "* 🥵 " + str(apply_pages) + " Pages, couldn't apply to this job! Extra info needed. Link: " + str(
                offer_page)
        return result

    @staticmethod
    def display_write_results(line_to_write: str) -> None:
        """
        This function prints and writes the given line to the results file.

        Parameters:
        line_to_write (str): The line to be printed and written.

        Returns:
        None

        Raises:
        Exception: If there is an error while writing to the file.
        """
        try:
            print(line_to_write)
            utils.write_results(line_to_write)
        except Exception as e:
            pr_red("Error in DisplayWriteResults: " + str(e))


start = time.time()
while True:
    try:
        Linkedin().link_job_apply()
    except Exception as e:
        pr_red("Error in main: " + str(e))
        # close firefox driver
        end = time.time()
        pr_yellow("---Took: " + str(round((time.time() - start) / 60)) + " minute(s).")
        Linkedin().driver.quit()
