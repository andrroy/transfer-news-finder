from bs4 import BeautifulSoup
import urllib, urllib2, cookielib
#import re
import config

#resp.read() is the straight html of the page you want to open, and you can use opener to view any page using your session cookie
# posts = soup.findAll("ol", { "class" : "discussionListItems" })

username = config.username
password = config.password

## Log in with session #####
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'login' : username, 'password' : password})
opener.open('http://spurscommunity.co.uk/index.php?login/login', login_data)
resp = opener.open('http://spurscommunity.co.uk/index.php?forums/transfer-rumours.46/')
html = resp.read()


## Find link to current ITK thread
def get_current_itk_thread():
    resp = opener.open('http://spurscommunity.co.uk/index.php?forums/transfer-rumours.46/index.rss')
    html = resp.read()

    soup = BeautifulSoup(html)
    link = soup.item.link.string

    return link






link = get_current_itk_thread()


resp = opener.open(link)
html = resp.read()

soup = BeautifulSoup(html)

##	Go through posts in thread
posts = soup.findAll('article')

for post in posts:
    print "<hr>"
    print post


## End


#	http://spurscommunity.co.uk/index.php?forums/the-summer-2014-transfer-rumours-archive.93/index.rss
#	Find <link> of first <item>
#	For each site 
#	Identify posts
#	Get ratings
#	Do stuff with data
#	Go to next page