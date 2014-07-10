## Parser module

from bs4 import BeautifulSoup
import urllib, urllib2, cookielib, re
import stripper
import utilities
import objects

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
	# print "Initializing parsing on page %s" % link
	post_should_be_saved = False

	resp = opener.open(link)
	html = resp.read()

	soup = BeautifulSoup(html)

	# Find all posts
	posts = soup.findAll("li", { "class" : "message" })
	# Itterate every post
	for post in posts:
		poster = post.find('a', {'class': 'username'}) # Get user data
		content = post.findAll('article') # Get posts content
		ratings = post.findAll("ul", { "class" : "dark_postrating_outputlist" }) # Get ratings

		# Iterate ratings in post (Should be own function)
		for rating in ratings:
			s = BeautifulSoup(str(rating))
			for img in s.findAll('img'):
				if 'Informative' in img['alt']: # Keep it if post is rated informative
					post_should_be_saved = True

		# Save post if informative (saving should be own function)
		if(post_should_be_saved):
			raw_user_data =  utilities.fix_spurscommunity_url( str(poster) ) 
			# print get_username( str(raw_user_data) )
			# print get_user_url( str(raw_user_data) )

			raw_content_data = utilities.fix_spurscommunity_url( str(content) )
			
			# print get_context_url(raw_content_data)
			# print get_context_content(raw_content_data)
			# print get_context_poster(raw_content_data)
			# print get_post_content( str(raw_content_data).strip('[]') )			
			# print ratings = get_post_ratings( str(ratings) )

			#print stripper.strip_html( str(content).strip('[]') )
			post_should_be_saved = False

	# Get next page
	next_page = get_next_page(soup)

	if next_page:
		parse_itk_thread( opener, 'http://www.spurscommunity.co.uk/' + next_page )

	# return get_current_page(soup)
			


def get_current_page(soup):
	current_page = soup.find('a', { 'class': 'currentPage'})
	return current_page['href']

def get_next_page(soup):
	page_nav = soup.find("div", {"class" : "PageNav"})
	for a in page_nav.findAll('a', { 'class': 'text'}):
		if 'Next' in a.string:
			return a['href']
	return ''

def get_username(html):
	soup = BeautifulSoup(html)
	return soup.a.string

def get_user_url(html):
	soup = BeautifulSoup(html)
	return soup.a.get('href')

def get_context_poster(html):
	soup = BeautifulSoup(html)
	poster = soup.find("div", { "class" : "attribution type" })
	# poster = re.search( '>(.*) said:', str(poster) ).group(1)
	poster = re.search('>(.*) said:', str(poster)).group(1)
	if poster:
		return poster
	return None

def get_context_url(html):
	soup = BeautifulSoup(html)
	url = soup.find('a', { 'class': 'AttributionLink'})
	if url:
		return url['href']
	return None

def get_context_content(html):
	soup = BeautifulSoup(html)
	return soup.blockquote.string

def get_post_content(html):
	soup = BeautifulSoup(html)
	# Remove quote
	for tag in soup.find_all( "blockquote", { "class" : "quoteContainer" } ):
		tag.replaceWith('')
	#Remove username of quote
	for tag in soup.find_all( "div", {"class" : "attribution type"} ):
		tag.replaceWith('')
	return str(soup)

def get_post_ratings(html):
	soup = BeautifulSoup(html)
	print '-----------------------------'

	ratings = { '' : '' }

	for tag in soup.find_all( "li" ):
		try:
			ratings.update( { tag.img['alt'] : tag.strong.string } )
		except Exception:
			pass

	return ratings
	
	# return soup


