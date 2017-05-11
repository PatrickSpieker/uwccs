# importing:
# regex, requests, urllib, argv, and beautiful soup
import re
import requests
import urllib
import sys
from bs4 import BeautifulSoup
import json
from helpers import *
from pprint import pprint


json_output = {}


soup = get_soup("crscat.html")

goal_tag = soup.find_all("ul")[1]
for tag in goal_tag.find_all("a", href=re.compile(".*.html")):
    # checking for parens
    pattern = r"\([A-Z| ]*\)"

    # making sure we aren't looking at a non-dept line
    if "(" not in tag.string: continue
    first_dash = tag.string.find("--")
    if first_dash == -1:
        end = tag.string.find("(") - 1 
    else:
        end = min(tag.string.find("("), first_dash) - 1
    dept_name = tag.string[:end]

    search_obj =  re.search(pattern, tag.string)
    # making sure we found a prefix
    if not search_obj: continue
    dept_prefix = str(search_obj.group()).translate(None, "()")
    print dept_prefix
    # download the course webpage
    download_course_data(tag['href'])
    """ 
    dept_soup = get_soup("html/" + dept_prefix
    # only concerned with first child
    content = tag.findAll()[0]
    courseId = getCourseId(content, deptCode)
    courseClass = courseId.replace(" ", "").lower()

    # filtering out grad level courses
    numCID = int(float(courseId[len(deptCode):]))
    if numCID < 500:
        rawList = getRawPrereqList(content)
        regPrereqs = getRegPrereqs(rawList, coursePatt)
        choicePrereqs = getChoicePrereqs(rawList, coursePatt)
         
        # creating JSON object to represent current node
        courseInfo = {u"course_id": courseId, u"regPrereqs": regPrereqs,
                u"choicePrereqs": choicePrereqs, u"numCID": numCID}
        deptJSON[courseClass] = courseInfo
        
       
with open("course-data.json", "w") as outfile:
    json.dump(json_output, fp=outfile)

pprint(json_output)
"""






