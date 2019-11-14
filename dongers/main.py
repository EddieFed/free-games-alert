from bs4 import BeautifulSoup
import requests
import random


dongerlist = []
for page in range(1, 40): 
    r = requests.get('http://dongerlist.com/page/' + str(page))
    r = r.text
    
    soup = BeautifulSoup(r, 'html.parser')
    
    dongerlist_container = soup.find_all(class_='donger')
    
    for cont in dongerlist_container:
        dongerlist.append(cont.get_text())


dongerlist = '\n'.join(dongerlist)

file = open('donger.txt', 'r+')
file.write(dongerlist)        
file.close()

print(random.choice(dongerlist))
exit()
