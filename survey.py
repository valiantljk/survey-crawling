#Written by Jialin Liu
#Email: valiantljk@gmail.com
#Date and Time: Sep 15, 10pm - Sep 16, 4am, 2017

#How to run: 
#          python survey.py start_id number_of_query output
#For example if you run 
#          python survey.py 1001 10 1001_10.xlsx,
#then you will get 10 records starting from 00000001001, and the results will be saved in 1001_10.xlsx

#For first running on my computer, you may need to install some python packages, e.g., mechanize, bs4, html5lib
#The code requires python 2.x, bc mechanize only works in python 2, not python 3

import time
import mechanize
from bs4 import BeautifulSoup
import sys
import xlsxwriter

def login(username,context,projectid):
 '''
  credentials:
   username
   context
   projectid
 '''
 try:
  br = mechanize.Browser()
  first_url='testurl'
  br.open(first_url)
  br.select_form(nr=0)
  br.form['intid'] = username
  br.form['context'] = context
  br.submit() # now in page requesting project info
  br.select_form(nr=0)
  br.form['PROJECT']=[projectid,] # needs a list for the listoption in html 
  br.submit() # now in page requesting record id info
  return br
 except Exception as e:
  print ("something wrong in login")
  #print e
  import sys
  sys.exit()

def get_record_by_id(br, id):
 '''
 parameters:
  br: browser instance, obtained after br.submit()
  id: 10 digits string, e.g., '0000001001'
 '''
 error=0
 try: 
  br.select_form(nr=0)
  br.form['RECNO'] =str(id)
  req=br.submit(name='IACTION-8') # now at the interview call page 
 except Exception as e:
  #print e
  print ("something wrong in opening by id:%s"%id)
  sys.exit()
 try:
  text=req.read() # read html
  soup = BeautifulSoup(text,'lxml') # choose lxml parser 
  phone=soup.find("input",{"name":"CMD1_PhoneNo"})['value']
  recnumb=soup.find("input",{"name":"RECNUMB"})['value']
  spans = soup.find_all('span', {'class' : 'RECALLEDTEXT'})
  lines = [span.get_text() for span in spans]
  fname=lines[-2]
  lname=lines[-1]
  if(id!=recnumb):
    print ("id %s is not equal recnumb %s"%(id,recnumb))
  rec={"fname":fname,"lname":lname,"phone":phone,"id":id,}
 except Exception as e:
   #print e
   print ('parsing error in id:%s'%id)
   error=1
   pass
 if (error==1):
  rec={"fname":"null","lname":"null","phone":"null","id":id,}
 br.back()
 return rec


def write_excel(record,excel_name):
    import xlsxwriter
    try:
        workbook = xlsxwriter.Workbook(excel_name)
        worksheet = workbook.add_worksheet()
        row = 0
        col = 0
        for r in record:
            col=0
            for key in r.keys():
                worksheet.write(row,col,r[key])
                col+=1
            row+=1
        workbook.close()
    except Exception as e:
        print ("excel writing error:%s"%excel_name)
        exit()

if __name__ == "__main__":
 if (len(sys.argv)<4):
    print ("start_id, number_of_record, output_filename")
    exit()
 startid=int(sys.argv[1])
 num=int(sys.argv[2])
 excelname=str(sys.argv[3])
 username='testuser'
 projectid='testproject'
 context='testtest'
 br=login(username,context,projectid)
 total_start_time=time.time()
 record=list()
# inputs=list()
# num_cores = multiprocessing.cpu_count()
# inputs=['000000'+str(startid+i) for i in range(num)]
# record=Parallel(n_jobs=num_cores)(delayed(get_record_by_id)(br,i) for i in inputs)
 for i in range(num):
  #start=time.time()
  nextid='000000'+str(startid+i)
  #print "%d:id:%s"%(i,nextid)
  #(br,rec)=get_record_by_id(br,nextid)
  rec=get_record_by_id(br,nextid)
  #end=time.time()
  #print rec,",%.2fsec"%(end-start)
  #if (i%10==0):
  print (rec)
  record.append(rec)

 tt=time.time()-total_start_time
 print ("Total query cost:%.2fsec"%(tt))
 print ("Writing to excel %s"%excelname)
 write_excel(record,excelname)
