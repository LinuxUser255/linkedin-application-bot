#!/usr/bin/env python3

import sys
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import pr_green, pr_red, pr_yellow

pr_yellow("ℹ️  This script will check if the bot can automatically log in Linkedin for you.")


def check_python():
    try:
        if sys.version:
            pr_green("✅ Python is succesfully installed!")
        else:
            pr_red("❌ Python is not installed please install Python first: https://www.python.org/downloads/")
    except Exception as e:
        pr_red(e)


def check_pip():
    try:
        import pip
        pr_green("✅ Pip is succesfully installed!")
    except ImportError:
        pr_red("❌ Pip not present. Install pip: https://pip.pypa.io/en/stable/installation/")


def check_selenium():
    try:
        import selenium
        pr_green("✅ Selenium is succesfully installed!")
    except ImportError:
        pr_red("❌ Selenium not present. Install Selenium: https://pypi.org/project/selenium/")


def check_firefox():
    try:
        import subprocess
        output = subprocess.check_output(['firefox', '--version'])
        if output:
            pr_green("✅ Firefox is succesfully installed!")
        else:
            pr_red("❌ Firefox not present. Install firefox: https://www.mozilla.org/en-US/firefox/")

    except ImportError as e:
        pr_red(e)


def check_selenium_linkedin():
    options = Options()
    # firefoxProfileRootDir = os.getenv('firefoxProfileRootDir')

    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("-profile")
    # options.add_argument(firefoxProfileRootDir)
    # options.headless = True

    browser = webdriver.Firefox(options=options)

    try:
        browser.get('https://www.ongundemirag.com')
        if browser.title.index("Ongun") > -1:
            pr_green("✅ Selenium and geckodriver is working succesfully!")
        else:
            pr_red("❌ Please check if Selenium and geckodriver is installed")
    except Exception as e:
        pr_red(e)

    try:
        browser.get('https://www.linkedin.com/feed/')
        time.sleep(3)
        if "Feed" in browser.title:
            pr_green('✅ Successfully you are logged in to Linkedin, you can now run main bot script!')
        else:
            pr_red('❌ You are not automatically logged in, please set up your Firefox Account correctly.')
    except Exception as e:
        pr_red(e)
    finally:
        browser.quit()


def main():
    check_python()
    check_pip()
    check_selenium()
    check_firefox()
    check_selenium_linkedin()


if __name__ == "__main__":
    main()
