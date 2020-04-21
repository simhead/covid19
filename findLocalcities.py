#!/usr/bin/python

import sys
import requests
import mysql.connector
from bs4 import BeautifulSoup

def getDbConn():
    myConn = mysql.connector.connect(
       host="34.208.95.154",
       user="root",
       password="changeme",
       db='covid19',
       port='32528'
    )

    return myConn

print(sys.argv[1:])

URL = 'https://www.dhhs.vic.gov.au/coronavirus-update-victoria-'+sys.argv[1]
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

p_tags = soup.find_all("p")
localcities_str = ""
localcities_list = []
connection = getDbConn()

for ix, p_tag in enumerate(p_tags, start=1):
    temp_p_tag = p_tag.text.strip()
    temp_p_tag = p_tag.text.rstrip()
    if "below." in p_tag.text:
        #print("QUITING the loop at ", ix)
        if "Local" in p_tags[ix+1].text:
            localcities_str = p_tags[ix+2].text
            jx = ix
            while jx > 0:
                if "Address:" in p_tags[jx].text:
                    break
                else:
                    #print(p_tags[jx+2].text)
                    localcities_list += [p_tags[jx+2].text]
                jx += 1
            #print('While loop ended')
        else:
            localcities_str = p_tags[ix+1].text
        break
    #print(ix, p_tag.name, p_tag.text, " checking:: ", temp_p_tag.endswith("below."))
try:
    cursor = connection.cursor()

    if len(localcities_list) > 0:
        for ix, localcity in enumerate(localcities_list):
            localcity_details = localcity.split("\n")
            #print(localcity_details)
            for jx, record in enumerate(localcity_details):
                city_strlist = record.split(" ")
                if len(city_strlist) > 1:
                    #print("string details::::: ", city_strlist)
                    mergename = city_strlist[0]
                    cases = city_strlist[1]
                    if len(city_strlist) > 2:
                        cases = city_strlist[2]
                    filedate = sys.argv[1]
                    if len(city_strlist) == 4:
                        mergename = city_strlist[0]+" "+city_strlist[1]
                        cases = city_strlist[3]
                    print(mergename.strip(), "LEN: ", len(city_strlist))
                    values_str = "('"+mergename.strip()+"','"+cases.strip()+"',STR_TO_DATE('"+filedate+"', '%d-%M-%Y'))"
                    sql = "INSERT INTO covid19.covid_daily (locality, cases, filedate) VALUES "+values_str
                    print(sql)
                    cursor.execute(sql)

            if ix+4 > len(localcities_list):
                break
        print("this is the case with <p> as stringlist")
    else:
        print (localcities_str)
        print("this is the case with <p> as single string format")

    
    #cursor.execute("INSERT INTO covid19.covid_daily (locality, cases, filedate) VALUES('MURRINDINDI', '1', '2020-04-01')")
    connection.commit() # Use this command after insert or update

    cursor.execute("""
        SELECT locality, cases, filedate FROM covid_daily
    """)
    result = cursor.fetchall()
    print(result)
finally:
    connection.close()

