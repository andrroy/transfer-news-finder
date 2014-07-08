# Utility class

def fix_spurscommunity_url(html):
	domain = 'http://www.spurscommunity.co.uk/'
	html = html.replace('index.php', 'http://www.spurscommunity.co.uk/index.php')
	return html