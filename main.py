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
course_ids = []
course_id_raw_list = []

soup = get_soup("crscat.html")

goal_tag = soup.find_all("ul")[1]
for tag in goal_tag.find_all("a", href=re.compile(".*.html")):
    # checking for parens
    pattern = r"\([A-Z| ]*\)"

    # making sure we aren't looking at a non-dept line
    if "(" not in tag.string:
        continue
    first_dash = tag.string.find("--")
    if first_dash == -1:
        end = tag.string.find("(") - 1 
    else:
        end = min(tag.string.find("("), first_dash) - 1
    dept_name = tag.string[:end]

    search_obj = re.search(pattern, tag.string)
    # making sure we found a prefix
    if not search_obj:
        continue
    dept_prefix = unicode(search_obj.group()).encode('utf-8').translate(None, "()")
    print dept_prefix
    print tag['href']
    # download the course webpage
    download_course_data(tag['href'])
    dept_soup = get_soup("html/" + tag['href'])
    class_tags = get_tags(dept_soup)
    for ct in class_tags:
        course_id = get_course_id(ct, dept_prefix)
        course_class = course_id.replace(" ", "").lower()
        # filtering out grad level courses
        numCID = int(float(course_id[len(dept_prefix):]))
        if numCID < 500:
            raw_list = get_raw_prereq_list(ct)
            #reg_prereqs = get_reg_prereqs(raw_list, course_patt)
            #choice_prereqs = get_choice_prereqs(raw_list, course_patt)
            course_id_raw_list.append((course_id, raw_list))
            course_ids.append(course_id)

combined = "(" + "|".join(course_ids) + ")"
course_patt = re.compile(combined)
for i in course_id_raw_list:
    print str(i[0]) + ": "
    course_json = {
        u'course_id': unicode(i[0]),
        u'req_prereqs': get_reg_prereqs(i[1], course_patt),
        u'choice_prereqs': get_choice_prereqs(i[1], course_patt)
    }
    json_output[i[0]] = course_json
    #print "\tRequired: " + str(get_reg_prereqs(i[1], course_patt))
    #print "\tChoice: " + str(get_choice_prereqs(i[1], course_patt))

with open("course-data.json", "w") as outfile:
    json.dump(json_output, fp=outfile)

pprint(json_output)






