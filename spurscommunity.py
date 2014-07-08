## Parser module

from bs4 import BeautifulSoup
import urllib, urllib2, cookielib
import stripper
import utilities

## Log in with session #####
def login(username, password):	
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	login_data = urllib.urlencode({'login' : username, 'password' : password})
	opener.open('http://spurscommunity.co.uk/index.php?login/login', login_data)

	return opener

## Find link to current ITK thread
def get_current_itk_thread(opener):
	resp = opener.open('http://spurscommunity.co.uk/index.php?forums/transfer-rumours.46/index.rss')
	html = resp.read()

	soup = BeautifulSoup(html)
	link = soup.item.link.string

	return link

## Parse current page
def parse_itk_thread(opener, link):

	post_should_be_saved = False

	resp = opener.open(link)
	html = resp.read()

	soup = BeautifulSoup(html)

	posts = soup.findAll("li", { "class" : "message" })

	for post in posts:
		poster = post.find('a', {'class': 'username'})
		content = post.findAll('article')
		ratings = post.findAll("ul", { "class" : "dark_postrating_outputlist" })

		for rating in ratings:
			s = BeautifulSoup(str(rating))
			for img in s.findAll('img'):
				if 'Informative' in img['alt']:
					post_should_be_saved = True


		if(post_should_be_saved):
			print utilities.fix_spurscommunity_url( str(poster) ) 
			#print str(content).strip('[]')
			print utilities.fix_spurscommunity_url( str(content) )
			print ratings
			#print stripper.strip_html( str(content).strip('[]') )
			post_should_be_saved = False


	next_page = get_next_page(soup)

	if next_page:
		site = 'http://www.spurscommunity.co.uk/'
		site += next_page
		parse_itk_thread(opener, site)
			


def get_current_page(soup):
	current_page = soup.find('a', { 'class': 'currentPage'})
	return current_page['href']

def get_next_page(soup):
	page_nav = soup.find("div", {"class" : "PageNav"})

	for a in page_nav.findAll('a', { 'class': 'text'}):
		if 'Next' in a.string:
			return a['href']

	return ''

