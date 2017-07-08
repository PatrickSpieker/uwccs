import re
import requests
import urllib
from sys import argv
from bs4 import BeautifulSoup


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


def get_tags(soup):
    tags = soup.find_all("a")
    return [t for t in tags if t.has_attr('name')]


def get_courses_offered_with(contents):
    # checking to see if there are any relevent courses
    info_ind = str(contents).find("Prerequisite: ")
    if info_ind == -1:
        return []
    info_ind += len("Prerequisite: ")
    connectionInfo = 0


def has_prereqs(content):
    return not (str(content).find("Prerequisite: ")==-1)


def has_offered_with(content):
    return not (str(content).find("Offered")==-1)


def get_relevant_end_ind(str_content, relevant_start_ind):
    if str_content.find("Offered: jointly") != -1:
        return str_content.find("Offered: jointly")
    return str_content.find("<br/>", relevant_start_ind)


def get_raw_prereq_list(content):
    if not has_prereqs(content):
        return []
    str_content = str(content)
    relevant_start_ind = str_content.find("Prerequisite: ")+len("Prerequisite: ")
    relevant_end_ind = get_relevant_end_ind(str_content, relevant_start_ind)
    relevant_content = str(content)[relevant_start_ind:relevant_end_ind]
    # splitting into each seperate prereq
    return relevant_content.split(";")


def get_reg_prereqs(raw_prereq_list, course_patt):
    if not raw_prereq_list:
        return tuple()
    reg_prereqs = []
    for section in raw_prereq_list:
        # checking for optional prereqs
        if "or" not in section:
            # append EACH ITEM from the list of options
            for item in course_patt.findall(section):
                reg_prereqs.append(item)
    return tuple(reg_prereqs)


def get_choice_prereqs(raw_prereq_list, course_patt):
    if not raw_prereq_list:
        return tuple()
    choice_prereqs = []
    for section in raw_prereq_list:
        # checking for optional prereqs
        if "or" in section:
            # append the ENTIRE tuple of options to the prereq list
            options = course_patt.findall(section)
            if options is not []:
                choice_prereqs.append(tuple(options))
    return tuple(choice_prereqs)


def get_course_id(content, dept_code):
    # if content.b:
    # defining string with course info
    course_str = content.b.string
    # finding index of end of course string
    course_str_end = course_str.find("(")-1
    # finding length of course_id
    id_end = len(dept_code.lower())+4  # length of space and number
    # defining course id, ex: CSE 143
    course_id = course_str[0:id_end]
    return course_id



