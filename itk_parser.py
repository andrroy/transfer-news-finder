from bs4 import BeautifulSoup
import urllib, urllib2, cookielib
#import re
import config
import spurscommunity

#resp.read() is the straight html of the page you want to open, and you can use opener to view any page using your session cookie
# posts = soup.findAll("ol", { "class" : "discussionListItems" })

# Get username and password
username = config.username
password = config.password

# Login to sc
opener = spurscommunity.login(username, password)

# Get link to itk thread
link = spurscommunity.get_current_itk_thread(opener)


spurscommunity.parse_itk_page(opener, link)




#http://spurscommunity.co.uk/index.php?threads/the-daily-itk-discussion-thread-7th-july-2014.110344/page-2#post-4105130