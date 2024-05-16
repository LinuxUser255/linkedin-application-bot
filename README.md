# LinkedIn Application Bot 🤖

### Forked from <https://github.com/aminblm/linkedin-application-bot/tree/main>
![linkedineasyapplygif](https://user-images.githubusercontent.com/34207598/128695728-6efcb457-0f75-42e2-987a-f7a0c239a235.gif)

## A Python bot to apply all LinkedIn Easy Apply jobs based on your preferences.

- Two options are avalible to use this bot, either with entering password or without, fully secure no credentials are stored.
- Export all results and offers as txt file
- Fully customizable job preferences
- Can be used for many job search websites such as Linkedin, Glassdoor, AngelCo, Greenhouse, Monster, GLobalLogic and Djinni.

<br>

# TO DO - Fixes and Changes 
In order of most to least important

- [x] Follow [PEP 8 Syle Guide coding conventions:](https://peps.python.org/pep-0008/)
- [x] ~~Change all Variable and Function names to lower case: linkedin.py & utils.py~~
- [x] Document code: Implement TypeHints & [reStructuredText markup and doctrings](https://devguide.python.org/documentation/markup/)
- [x] ~~linkedin.py - document~~
- [ ] utils.py - document
- [ ] Fix the [find_element "xpath" issues](https://selenium-python.readthedocs.io/locating-elements.html).
- [ ] Implement [Anti-Bot detection](https://scrapeops.io/selenium-web-scraping-playbook/python-selenium-undetected-chromedriver/) to avoid account login issues, captchas
- [ ] Eliminate launching a new browser/login session with each iteration.
- [ ] Conduct all searches and applications within one browser session.
- [ ] Look at other [Forks](https://github.com/aminblm/linkedin-application-bot/forks) for ideas
- [ ] ---
- [ ] Maybe retrieve and use session cookies from the browser?
- [ ] Chromium not woking properly with Linux
- [ ] Implement Headless browser experience (run the bot without launching the browser)
- [ ] Add More robustness of the bot for different fields
- [ ] Blacklist offers in Linkedin
- [ ] Output not completed fields in Linkedin
- [ ] Add support to other major job seeking websites:
- [ ] [Indeed](https://www.indeed.com/)
- [ ] [Glassdoor](https://www.glassdoor.com/index.htm)
- [ ] [AngelCo](https://angel.co/l/2xRADV) And possibly Greenhouse, Monster, GLobalLogic, and djinni.


<br>


## Installation 🔌

- clone the repo `git clone https://github.com/LinuxUser255/linkedin-application-bot.git`
- Make sure [Python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/getting-started/) is installed
- Install dependencies with `pip3 install -r requirements.yaml`
- Either create firefox Profile and put its path on line 8 of config.py or enter your linkedin credentials line 11 and 12 of config.py.
- Modify config.py according to your demands.
- Run `python3 linkedin.py`
- Check Applied Jobs DATA .txt file is generate under /data folder
- [Selenium Documentation](https://www.selenium.dev/selenium/docs/api/py/index.html#)


## Features 💡

- Ability to filter jobs, by easy apply, by location, keyword, by experience, position, job type and date posted.
- See config.py, this is where you set job filtering
- Apply based on your salary preferance (works best for job offers from States)
- Automatically apply single page jobs in which you need to send your up-to-date CV and contact.
- Automatically apply more than one page long offers with the requirements saved in LinkedIn like experience, etc.
- Output the results in a data txt file where you can later work on.
- Print the links for the jobs that the bot couldn’t apply, due to extra requirements.
- Put time breaks in between functions to prevent threshold.
- Automatically apply for jobs.
- Automatically run in the background.
- Compatible with Firefox and Chrome.
- Runs based on your preferences.
- Optional follow or not follow company upon successful application.
- Much more!


## Tests 🔦

There is test script that can be run to test the dependencies, and functionality of the bot. 

1. Located in the repo's parent directory is a script named `test.py`. this will check if Python, pip, selenium, dotenv and Firefox are correctly installed on your system.
2. Run `python3 test.py` (or click the green arrow on the line `if __name__ == "__main__":`), this will output if the Selenium and gecko driver is able to retrieve data from a website. If it returns an error make sure you have correctly installed selenium and gecko drive
3. It will also try to log in to your Linkedin account based on the path you defined in the .env file. If its giving an error make sure the path exists and you created firefox profile, logged in manually to your Linkedin account once.
   Here is the result you should get after running test files,
   ![test1](https://user-images.githubusercontent.com/34207598/189535308-c2c546de-caec-4460-823d-dd5ca208c480.png)

## How to Set up (long old way) 🛠

This tutorial briefly explains how to set up LinkedIn Easy Apply jobs bot. With few modifications you can make your own bot or try my other bots for other platforms.

1. Install Firefox or Chrome. I was using Firefox for this so I will continue the usage of it on Firefox browser. Process would be similar on Chrome too.
2. Install Python.
3. Download [Geckodriver](https://github.com/mozilla/geckodriver/releases) put it in Python’s installation folder.
4. Install pip, python get-pip.py
5. Install selenium pip install selenium
6. Clone the code
7. Create a profile on Firefox, about:profiles
8. Launch new profile, go Linkedin.com and log in your account
9. Copy the root folder of your new profile, to do that type about:profiles on your Firefox search bar, copy the root folder C:\---\your-profile-name.
10. Paste the root folder on the `config.py` if the `firefoxProfileRootDir` file
11. Modify/adapt the code and run in `config.py` to preferences.
12. After each run check the jobs that the bot didn’t apply automatically, apply them manually by saving your preferences
13. Next time the bot will apply for more jobs based on your saved preferences on Linkedin.
14. Feel free to contact me for any update/request or question.

## Demo 🖥

![banner](https://github.com/aminblm/linkedin-application-bot/assets/25132838/b0dda2f0-b531-48af-b769-fc1370d88fdb)
![1](https://github.com/aminblm/linkedin-application-bot/assets/25132838/1caeeff1-7f70-423a-ae51-ae97ba00bc99)
![2](https://github.com/aminblm/linkedin-application-bot/assets/25132838/3cb59d82-b167-40ad-8fef-d8e1430bf6c1)

## Future Implementations

- See the TO DO list above

<br>
