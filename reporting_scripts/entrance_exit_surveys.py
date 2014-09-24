'''
This module extract all the information filled by students for the entrance 
and exit survey

First step is to get ids of each page in the surveys. One may have to do this 
manually by:

1) Go to http://studio.edx.org and select the required course. For e.g., for
the course ATOC185x, go to https://studio.edx.org/course/McGillX/ATOC185x/2T2014

2) In the course outline, go to Entrance Survey and select the first page of the
entrance survey, e.g. General Info

3) On the new page that opens, click on 'View Live Version', this opens a page 
in a new tab

4) Click on 'STAFF DEBUG INFO'. Note that there are two links to 'STAFF 
DEBUG INFO', one at the top and one at the bottom. Select the one on the
bottom of the page

5) A small window should pop up. In the window, the value stored under location
is the id the of page General Info for the Entrance Survey e.g.
location = i4x://McGillX/ATOC185x/problem/e60f566b9a9342ac9b8dd3f92296af41

6) Once you get the id for one page of a survey, repeat above process to get 
ids of all the pages of both the Entrance and Exit Surveys

7) The ids will be used in the scripts below to extract all the information 
filled by students in the Entrance and Exit Surveys from the collection 
courseware_studentmodule of a given course.

Usage (after getting the ids of all the pages in the Entrance and Exit surveys): 

python entrance_exit_surveys.py 

'''

from collections import defaultdict

from base_edx import EdXConnection
from generate_csv_report import CSV

connection = EdXConnection('courseware_studentmodule', 'auth_user')
collection = connection.get_access_to_collection()

# Modify key-value pairs in survey_pages to the name of the survey pages and to 
# the problem ids that maps to the survey pages E.g. if a course have a 
survey_pages = {'entrance_survey' : {'general_info' : 'i4x://McGillX/ATOC185x/problem/e60f566b9a9342ac9b8dd3f92296af41', 
'demographics_background' : 'i4x://McGillX/ATOC185x/problem/e60f566b9a9342ac9b8dd3f92296af41' , 
'aspirations_motivation' : None}, 'exit_survey' : {'part_1' : None, 'part_2': None}}

survey_ids = [_id for page in survey_pages.values() for _id in page.values()]

cursor_courseware_studentmodule = collection['courseware_studentmodule'].find()
cursor_student = collection['auth_user']

result = defaultdict(list)
survey_questions = set()
for document in cursor_courseware_studentmodule:
	if document['module_id'] in survey_ids:
		username = cursor_student.find({'_id' : document['_id']})
		student_answers = document['state']['student_answers'].iteritems()
		result[username].append(student_answers)





