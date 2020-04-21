import requests
from bs4 import BeautifulSoup

localcities = []

URL = 'https://www.dhhs.vic.gov.au/coronavirus-update-victoria-15-april-2020'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

#results = soup.find(class='field field--name-field-dhhs-rich-text-text field--type-text-long field--label-hidden field--item')

#print(results.prettify())

#job_elems = soup.find_all('div', class_='field field--name-field-dhhs-rich-text-text field--type-text-long field--label-hidden field--item')

#for ix, job_elem in enumerate(job_elems, start=1):
    #print(ix, job_elem, end='\n'*2)
    # returns first occurrence of Substring 
    #print(ix, job_elem)
    #localcities = job_elem.get_text(separator=" ").strip()
    print (len(localcities))
    #for jx, localcity in enumerate(localcities, start=1):
    #    print(jx, localcity)
    #word = 'geeks for geeks'
    #result = word.find('for')
    print ("Substring '/ul' found at index:", result ) 
    print("length of string: ", len(job_elem)) 

#for tag in soup.find_all("p"):
#    print("{0}: {1}".format(tag.name, tag.text))
p_tags = soup.find_all("p")
localcities_str = ""
for ix, p_tag in enumerate(p_tags, start=1):
    #print(ix, p_tag.name, p_tag.text, " checking:: ", p_tag.text.endswith("below."))
    if p_tag.text.endswith("below."):
        print("QUITING the loop at ", ix)
        localcities_str = p_tags[ix+1].text
        break

print (localcities_str)
