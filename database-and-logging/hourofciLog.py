from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask import abort
import re

import psycopg2

# Collects user information
import getpass
# Collect timestamp
import time
import datetime

from flask_cors import CORS

lesson_list = ['template','gateway','big-data','computational-thinking','cyberinfrastructure','geospatial-data','interdisciplinary-communication',
               'parallel-computation','spatial-modeling-analytics','spatial-thinking']
lesson_level_list = ['template','gateway','beginner','advanced']
# question_list = ['Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8',]

app = Flask(__name__)
api = Api(app)
# v7
CORS(app)

# Logging
# records the user's ip, datetime, and answer for a specific question
class logging(Resource):
    def get(self, user_agent, lesson, lesson_level, question, answer): 
        
        # PARAMETERS VALIDATION 
        
        # The values of lesson, lesson_level, and question should be from our lesson design
        if lesson not in lesson_list:
            abort(404, description="Invalid Lesson Values")
            
        if lesson_level not in lesson_level_list:
            abort(404, description="Invalid Lesson Level Values")
            
        # if question not in question_list:
        if not re.fullmatch(r'[1-9][A-Z]', question):
            abort(404, description="Invalid Question Values")
        
        # "Answer" values should not be included ');' (will stop the insert function in the database)
        # Match the types in the database
        answer = str(answer)
        if ');' in answer.replace(" ", ""):
            abort(404, description="Invalid Answer Values")  
        # Question: I tried answer including ');' but there is no error. ');' will be recorded in the answer column
        
        # GET USER INFO

        # Date 
        date_log = datetime.datetime.today().strftime('%Y-%m-%d')
            
        # Time
        time_log = time.strftime("%H:%M:%S", time.gmtime(time.time()))
        
    
        # DATABASE CONNECTION AND LOGGING
        
        # Create a connection
        logdb_connection = psycopg2.connect(user = "hourofciuser",
                                  password = "hourofcipassword",
                                  host = "check.hourofci.org",
                                  port = "5432",
                                  database = "hourofci")
        
        # Needed for connection
        cursor = logdb_connection.cursor()
        
        # Calls a function in SQL that logs these values
        cursor.callproc('logging', (user_agent, date_log, time_log, lesson, lesson_level, question, answer))
        
        # Commit the insert
        logdb_connection.commit()

# Logging for test
# records the user's ip, datetime, and answer for a specific question
class logging_test(Resource):
    def get(self, user_agent, lesson, lesson_level, question, answer): 
        
        # PARAMETERS VALIDATION 
        
        # The values of lesson, lesson_level, and question should be from our lesson design
        if lesson not in lesson_list:
            abort(404, description="Invalid Lesson Values")
            
        if lesson_level not in lesson_level_list:
            abort(404, description="Invalid Lesson Level Values")
            
        # if question not in question_list:
        if not re.fullmatch(r'[1-9][A-Z]', question):
            abort(404, description="Invalid Question Values")
        
        # "Answer" values should not be included ');' (will stop the insert function in the database)
        # Match the types in the database
        answer = str(answer)
        if ');' in answer.replace(" ", ""):
            abort(404, description="Invalid Answer Values")  
        # Question: I tried answer including ');' but there is no error. ');' will be recorded in the answer column
        
        # GET USER INFO

        # Date 
        date_log = datetime.datetime.today().strftime('%Y-%m-%d')
            
        # Time
        time_log = time.strftime("%H:%M:%S", time.gmtime(time.time()))
        
    
        # DATABASE CONNECTION AND LOGGING
        
        # Create a connection
        logdb_connection = psycopg2.connect(user = "hourofciuser",
                                  password = "hourofcipassword",
                                  host = "check.hourofci.org",
                                  port = "5432",
                                  database = "hourofci")
        
        # Needed for connection
        cursor = logdb_connection.cursor()
        
        # The only difference
        # Calls a function in SQL that logs these values
        cursor.callproc('logging2', (user_agent, date_log, time_log, lesson, lesson_level, question, answer))
        
        # Commit the insert
        logdb_connection.commit()

# Welcome page: check if the service works    
@app.route('/')
def welcome():
    # return render_template('ping_alive.html')  # render a template
    return 'Hello World!'

# Setup the Api resource routing
api.add_resource(logging, '/<user_agent>/<lesson>/<lesson_level>/<question>/<answer>') 
api.add_resource(logging_test, '/test/<user_agent>/<lesson>/<lesson_level>/<question>/<answer>') 
