"""
Skyler Hallinan
3/28/20

Function takes in UW transcript as PDF format and writes csv with grade
information after parsing through data

Input: UW Unofficial Transcript in pdf form (.pdf)
Output: CSV containing course, quarter, and grade information from transcript

TODO: Add grades from transfer courses or courses in progress (if useful)
"""

def transcript2csv(transcript):
    import PyPDF2
    import pandas as pd
    import re
    
    # Defining global constants used for array truncation
    GRADE_STR_IDX = 6
    GRADE_STR_LEN = 9
    QUART_STR_LEN = 4
    QUART_STR_IDX = 2
    
    # Define end of transcript character (omitting info from current quarter)
    END_STR = "****************************************************"
    
    # Define variable to hold constants correspnding to UW quarter labels
    quarters = ('AUTUMN', 'WINTER', 'SPRING', 'SUMMER')
    
    # Creating a pdf file and reader object 
    pdfFileObj = open(transcript, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    
    # Initialize empty string to hold our pdf text
    pdfText = "";
    
    # Extract text from all pages of the pdfReader object
    for i in range(pdfReader.getNumPages()):
        pdfText += pdfReader.getPage(i).extractText()
        
    # Closing the pdf file object 
    pdfFileObj.close() 
    
    # Removing in progress quarters by splitting on end character and keeping first element
    pdfText = pdfText.rsplit(END_STR, 1)[0]
    
    # Split text by linebreaks into an array
    splitText = re.split('\n', pdfText)
    
    # Trim white space
    splitText = list(map(str.strip, splitText))
    
    # Find indeces in the array correpsponding to start of new quarters
    indeces = [i for i, si in enumerate(splitText) if si.startswith(quarters)]
    
    # Load in course tag information (list of all course tags at UW)
    with open("course_tags.txt", 'r') as f:
        courses = [line.rstrip('\n') for line in f]
        
    # Store as tuple for checking if strings start with these tags
    # Also add a space charaacter at the end to prevent matches with non course tags
    coursesTup = tuple([c + " " for c in courses])
        
    # Empty array to hold grade information    
    gradeInfo = []
    
    # Iterate through all indeces of our split text
    for i in range(indeces[0], len(splitText)):
        
        # Access text in splitText list at index i
        curText = splitText[i]
        
        # Check if the string is a quarter
        if (curText.startswith(quarters)):
            
            # Set string list regarding curent quarter information
            currentQuarter = curText.split()
            
            # Create slice to combine Major names (if they have a space)
            strRange = slice(QUART_STR_IDX, len(currentQuarter) + QUART_STR_IDX - QUART_STR_LEN + 1)
        
            # Combine strings
            currentQuarter[strRange] = [' '.join(currentQuarter[strRange])]
            
        # Check if the string is a valid course tag
        elif (curText.startswith(coursesTup)):
            
            # Find course tag that matches start of our string
            tagMatch = [c for c in courses if curText.startswith(c)][0]
            
            # Create regex to match this string and split it
            matchRegex = '(' + tagMatch + ')(.+)'
            
            # Split string based on defined regex
            splitString = re.split(matchRegex, curText)
            
            # Filter out empty strings
            splitString = list(filter(None, splitString))
            
            # Combine all components into one row for our dataframe
            pdRow = currentQuarter + [splitString[0]] + splitString[1].split()
            
            # Define range to truncate our row
            strRange = slice(GRADE_STR_IDX, len(pdRow) + GRADE_STR_IDX - GRADE_STR_LEN + 1)
            
            pdRow[strRange] = [' '.join(pdRow[strRange])]
            
            # Append to our matrix and increment
            gradeInfo.append(pdRow)
            
#    
#    # Iterate through all indeces corresponding to quarters taken
#    for i in indeces:
#        
#        # Split first row into array
#        dfRow = splitText[i].split()
#        
#        # Set cur String (basicall a do-while)
#        idx = i + 1
#        curString = splitText[idx]
#        
#        # Check that we are stil looking at a class with a course tag (instead of QTR)
#        while(curString.startswith(tuple(courses))):
#            
#            # Find course tag that matches start of our string
#            tagMatch = [c for c in courses if curString.startswith(c)][0]
#            
#            # Create regex to match this string and split it
#            matchRegex = '(' + tagMatch + ')(.+)'
#            
#            # Split string based on defined regex
#            splitString = re.split(matchRegex, curString)
#            
#            # Filter out empty strings
#            splitString = list(filter(None, splitString))
#            
#            # Combine all components into one row for our dataframe
#            pdRow = dfRow + [splitString[0]] + splitString[1].split()
#            
#            # Define range to truncate our row
#            strRange = slice(STR_IDX, len(pdRow) + STR_IDX - STR_LEN + 1)
#            
#            pdRow[strRange] = [' '.join(pdRow[strRange])]
#            
#            # Append to our matrix and increment
#            gradeInfo.append(pdRow)
#            idx += 1
#            curString = splitText[idx]
    
    
    # Setting column names
    columnNames = ['Quarter', 'Year', 'Major', 'Num', 'Course', 'Number', 'Title', 'Credits', 'Grade']
    
    # Creating pandas dataframe to hold grade info
    df = pd.DataFrame(gradeInfo, columns = columnNames)
    
    df.to_csv("grades.csv", index = False)
    
transcript2csv("test.pdf")

