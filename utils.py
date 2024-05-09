import math,constants,config
from typing import List
import time

from selenium.webdriver.firefox.options import Options

def browserOptions():
    options = Options()
    firefoxProfileRootDir = config.firefoxProfileRootDir
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-gpu')
    if(config.headless):
        options.add_argument("--headless")

    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")
    options.add_argument("-profile")
    options.add_argument(firefoxProfileRootDir)

    return options

def prRed(prt):
    print(f"\033[91m{prt}\033[00m")

def prGreen(prt):
    print(f"\033[92m{prt}\033[00m")

def prYellow(prt):
    print(f"\033[93m{prt}\033[00m")

def getUrlDataFile():
    urlData = ""
    try:
        file = open('data/urlData.txt', 'r')
        urlData = file.readlines()
    except FileNotFoundError:
        text = "FileNotFound:urlData.txt file is not found. Please run ./data folder exists and check config.py values of yours. Then run the bot again"
        prRed(text)
    return urlData

def jobsToPages(numOfJobs: str) -> int:
  number_of_pages = 1

  if (' ' in numOfJobs):
    spaceIndex = numOfJobs.index(' ')
    totalJobs = (numOfJobs[0:spaceIndex])
    totalJobs_int = int(totalJobs.replace(',', ''))
    number_of_pages = math.ceil(totalJobs_int/constants.jobsPerPage)
    if (number_of_pages > 40 ): number_of_pages = 40

  else:
      number_of_pages = int(numOfJobs)

  return number_of_pages

def urlToKeywords(url: str) -> List[str]:
    keywordUrl = url[url.index("keywords=")+9:]
    keyword = keywordUrl[0:keywordUrl.index("&") ] 
    locationUrl =  url[url.index("location=")+9:]
    location = locationUrl[0:locationUrl.index("&") ] 
    return [keyword,location]

def writeResults(text: str):
    timeStr = time.strftime("%Y%m%d")
    fileName = "Applied Jobs DATA - " +timeStr + ".txt"
    try:
        with open("data/" +fileName, encoding="utf-8" ) as file:
            lines = []
            for line in file:
                if "----" not in line:
                    lines.append(line)
                
        with open("data/" +fileName, 'w' ,encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " +timeStr+ "\n" )
            f.write("---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result "   +"\n" )
            for line in lines: 
                f.write(line)
            f.write(text+ "\n")
            
    except:
        with open("data/" +fileName, 'w', encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " +timeStr+ "\n" )
            f.write("---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result "   +"\n" )

            f.write(text+ "\n")

def printInfoMes(bot:str):
    prYellow("ℹ️ " +bot+ " is starting soon... ")

def donate(self):
    prYellow('If you like the project, please support me so that i can make more such projects, thanks!')
    try:
        self.driver.get('https://commerce.coinbase.com/checkout/576ee011-ba40-47d5-9672-ef7ad29b1e6c')
    except Exception as e:
        prRed("Error in donate: " +str(e))

class LinkedinUrlGenerate:
    def generateUrlLinks(self):
        path = []
        for location in config.location:
            for keyword in config.keywords:
                    url = constants.linkJobUrl + "?f_AL=true&keywords=" +keyword+self.jobType()+self.remote()+self.checkJobLocation(location)+self.jobExp()+self.datePosted()+self.salary()+self.sortBy()
                    path.append(url)
        return path

    def checkJobLocation(self, job):
        jobLoc = "&location=" + job
        if job.casefold() == "asia":
            jobLoc += "&geoId=102393603"
        elif job.casefold() == "europe":
            jobLoc += "&geoId=100506914"
        elif job.casefold() == "northamerica":
            jobLoc += "&geoId=102221843"
        elif job.casefold() == "southamerica":
            jobLoc += "&geoId=104514572"
        elif job.casefold() == "australia":
            jobLoc += "&geoId=101452733"
        elif job.casefold() == "africa":
            jobLoc += "&geoId=103537801"

        return jobLoc

    def jobExp(self):
        jobExpArray = config.experienceLevels
        firstJobExp = jobExpArray[0]
        jobExp = ""

        if firstJobExp == "Internship":
            jobExp = "&f_E=1"
        elif firstJobExp == "Entry level":
            jobExp = "&f_E=2"
        elif firstJobExp == "Associate":
            jobExp = "&f_E=3"
        elif firstJobExp == "Mid-Senior level":
            jobExp = "&f_E=4"
        elif firstJobExp == "Director":
            jobExp = "&f_E=5"
        elif firstJobExp == "Executive":
            jobExp = "&f_E=6"

        for index in range(1, len(jobExpArray)):
            if jobExpArray[index] == "Internship":
                jobExp += "%2C1"
            elif jobExpArray[index] == "Entry level":
                jobExp += "%2C2"
            elif jobExpArray[index] == "Associate":
                jobExp += "%2C3"
            elif jobExpArray[index] == "Mid-Senior level":
                jobExp += "%2C4"
            elif jobExpArray[index] == "Director":
                jobExp += "%2C5"
            elif jobExpArray[index] == "Executive":
                jobExp += "%2C6"

        return jobExp

    def datePosted(self):
        datePosted = ""
        if config.datePosted[0] == "Any Time":
            datePosted = ""
        elif config.datePosted[0] == "Past Month":
            datePosted = "&f_TPR=r2592000&"
        elif config.datePosted[0] == "Past Week":
            datePosted = "&f_TPR=r604800&"
        elif config.datePosted[0] == "Past 24 hours":
            datePosted = "&f_TPR=r86400&"
        return datePosted

    def jobType(self):
       """jobTypeArray = config.jobType"""
       jobTypeArray = config.jobType
       firstjobType = jobTypeArray[0]
       jobType = ""
       if firstjobType == "Full-time":
           jobType = "&f_JT=F"
       elif firstjobType == "Part-time":
           jobType = "&f_JT=P"
       elif firstjobType == "Contract":
           jobType = "&f_JT=C"
       elif firstjobType == "Temporary":
           jobType = "&f_JT=T"
       elif firstjobType == "Volunteer":
           jobType = "&f_JT=V"
       elif firstjobType == "Intership":
           jobType = "&f_JT=I"
       elif firstjobType == "Other":
           jobType = "&f_JT=O"

       for index in range(1, len(jobTypeArray)):
           if jobTypeArray[index] == "Full-time":
               jobType += "%2CF"
           elif jobTypeArray[index] == "Part-time":
               jobType += "%2CP"
           elif jobTypeArray[index] == "Contract":
               jobType += "%2CC"
           elif jobTypeArray[index] == "Temporary":
               jobType += "%2CT"
           elif jobTypeArray[index] == "Volunteer":
               jobType += "%2CV"
           elif jobTypeArray[index] == "Intership":
               jobType += "%2CI"
           elif jobTypeArray[index] == "Other":
               jobType += "%2CO"

       jobType += "&"
       return jobType

    def remote(self):
        """replacing the match statement with if else statement"""
        remoteArray = config.remote
        firstJobRemote = remoteArray[0]
        jobRemote = ""
        if firstJobRemote == "On-site":
            jobRemote = "f_WT=1"
        elif firstJobRemote == "Remote":
            jobRemote = "f_WT=2"
        elif firstJobRemote == "Hybrid":
            jobRemote = "f_WT=3"

        for index in range(1, len(remoteArray)):
            if remoteArray[index] == "On-site":
                jobRemote += "%2C1"
            elif remoteArray[index] == "Remote":
                jobRemote += "%2C2"
            elif remoteArray[index] == "Hybrid":
                jobRemote += "%2C3"

        return jobRemote

    def salary(self):
        salary = ""
        if config.salary[0] == "$40,000+":
            salary = "f_SB2=1&"
        elif config.salary[0] == "$60,000+":
            salary = "f_SB2=2&"
        elif config.salary[0] == "$80,000+":
            salary = "f_SB2=3&"
        elif config.salary[0] == "$100,000+":
            salary = "f_SB2=4&"
        elif config.salary[0] == "$120,000+":
            salary = "f_SB2=5&"
        elif config.salary[0] == "$140,000+":
            salary = "f_SB2=6&"
        elif config.salary[0] == "$160,000+":
            salary = "f_SB2=7&"
        elif config.salary[0] == "$180,000+":
            salary = "f_SB2=8&"
        elif config.salary[0] == "$200,000+":
            salary = "f_SB2=9&"

        return salary

    def sortBy(self):
        sortBy = ""
        if config.sort[0] == "Recent":
            sortBy = "sortBy=DD"
        elif config.sort[0] == "Relevent":
            sortBy = "sortBy=R"
        return sortBy

