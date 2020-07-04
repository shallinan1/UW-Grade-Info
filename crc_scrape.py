"""
Skyler Hallinan
3/28/20
"""

import requests
import lxml.html as lh
import re

url = 'https://www.washington.edu/students/crscat/'
page = requests.get(url)

# Store the contents of the website under doc
doc = lh.fromstring(page.content)

allStrings = doc.xpath('//a/text()')

myRegex = r'[A-Z]\)'

reduced = [s for s in allStrings if re.search(myRegex, s)]

# Find text within parentheiss and remove space string
courses = [re.findall(r'\((.*?)\)',x)[-1].replace('\xa0', ' ') for x in reduced]
courses = sorted(courses, reverse = True, key = len)

with open("course_tags.txt", 'w') as f:
    for c in courses:
        f.write(c + '\n')
