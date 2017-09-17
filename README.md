# survey-crawling
simple python code for crawling a survey website to extract all user information

#Written by Jialin Liu 
#Email: valiantljk@gmail.com
#Date and Time: Sep 15, 10pm - Sep 16, 4am, 2017

#How to run:
        '''python
          python survey.py start_id number_of_query output
        '''
#For example if you run
        '''python
          python survey.py 1001 10 1001_10.xlsx,
        '''
#then you will get 10 records starting from 00000001001, and the results will be saved in 1001_10.xlsx

#For first running on my computer, you may need to install some python packages, e.g., mechanize, bs4, html5lib
#The code requires python 2.x, bc mechanize only works in python 2, not python 3

