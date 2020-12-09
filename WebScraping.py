import requests 
from bs4 import BeautifulSoup 
import pprint #pretty print

# get and parse the data from the site
num_pag = 1
res = requests.get('https://news.ycombinator.com/news') 
soup = BeautifulSoup(res.text,'html.parser')

links = soup.select('.storylink')
subtext = soup.select('.subtext')

# order the list of articles by number of votes
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k:k['votes'],reverse=True)

def create_custom_hn(links,subtext):
    hn = []
    num_pag = 1
    while num_pag < 3:
        for idx,item in enumerate(links): # enumerate: needed to access the links and the subtext elements.
            title = item.getText()
            href = item.get('href', None) # if the link is broken.
            vote = subtext[idx].select('.score')
            if len(vote):
                points = int(vote[0].getText().replace(' points',''))
                if points > 99:
                    hn.append({'title':title, 'link':href, 'votes':points})
        num_pag += 1
        res = requests.get('https://news.ycombinator.com/news?p=' + str(num_pag)) 
        soup = BeautifulSoup(res.text,'html.parser')
        links = soup.select('.storylink')
        subtext = soup.select('.subtext')
    
    return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hn(links,subtext))
