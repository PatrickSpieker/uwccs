# UW Course Catalog Scraper (UWCCS) #

Scrapes all UW courses into JSON file

### Contribution guidelines ###

* This project is under construction for the UW DataLab, supervised by Jevin West.

### Contact ###
* pspieker@cs.washington.edu

### Usage/Installation ###
* This requires Python 3.x. After cloning the repo, `pip -r requirements.txt` will get 
everything installed.
* `python main.py` will run download the relevant files into the `html/` directory
and then populate `course-data.json`. 
* The JSON format is `{course_id: {"course_id": course_id, 
"req_prereqs": [], "choice_prereqs": []}, ...}`

