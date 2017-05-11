import re
import requests
import urllib
from sys import argv
from bs4 import BeautifulSoup

def get_prefix_codes(soup):
    pass 

def download_course_data(src):
    # base url
    url = "http://www.washington.edu/students/crscat/" + src
    destination = 'html/' + src
    # fetching HTML
    urllib.urlretrieve(url, destination)
    return destination


def get_soup(target):
    # opening file
    with open(target, "r") as f:
        data = f.read()
    # processing data
    soup = BeautifulSoup(data, "lxml")
    return soup

def get_tags(pattern, soup):
    tags = soup.find_all("a", attrs={"name": pattern})
    return tags

def get_courses_offered_with(contents):
    # checking to see if there are any relevent courses
    infoInd = str(contents).find("Prerequisite: ")
    if infoInd == -1:
        return []
    infoInd += len("Prerequisite: ")
    connectionInfo = 0

def has_prereqs(content):
    return not (str(content).find("Prerequisite: ")==-1)

def has_offered_with(content):
    return not (str(content).find("Offered")==-1)

def get_relevant_end_ind(strContent, relevantStartInd): 
    if strContent.find("Offered: jointly") != -1:
        return strContent.find("Offered: jointly")
    return strContent.find("<br/>", relevantStartInd) 

def getRawPrereqList(content):
    if not hasPrereqs(content):
        return []
    strContent = str(content)
    relevantStartInd = strContent.find("Prerequisite: ")+len("Prerequisite: ")
    relevantEndInd = getRelevantEndInd(strContent, relevantStartInd)
    relevantContent = str(content)[relevantStartInd:relevantEndInd]
    # splitting into each seperate prereq
    return relevantContent.split(";")


def getRegPrereqs(rawPrereqList, coursePatt):
    if not rawPrereqList:
        return tuple()
    regPrereqs = []
    for section in rawPrereqList:
        # checking for optional prereqs
        if "or" not in section:
            # append EACH ITEM from the list of options
            for item in coursePatt.findall(section):
                regPrereqs.append(item.replace(" ", "").lower())
    return tuple(regPrereqs)


def getChoicePrereqs(rawPrereqList, coursePatt):
    if not rawPrereqList:
        return tuple()
    choicePrereqs = []
    for section in rawPrereqList:
        # checking for optional prereqs
        if "or" in section:
            # append the ENTIRE tuple of options to the prereq list
            options = coursePatt.findall(section)
            if options != []:
                choicePrereqs.append(tuple(options))
    return tuple(choicePrereqs)


def getCourseId(content, deptCode):
    # if content.b:
    # defining string with course info
    course_str = content.b.string
    # finding index of end of course string
    course_str_end = course_str.find("(")-1
    # finding length of course_id
    id_end = len(deptCode.lower())+4  # length of space and number
    # defining course id, ex: CSE 143
    course_id = course_str[0:id_end].replace(" ", "").lower()
    return course_id



