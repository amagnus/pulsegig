# script to download content using various apis
# author : Appu Shaji ( contact me at appoose at gmail )
# license : GPLv3 
# date : 20th Feb 2013

import urllib
import requests


def searchImage(searchTerm):
	rootUrl = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='
	apiKey = 'replace your api key here' # not needed if want < 64 images. Have not implemented the paid account version
	opUrlKey = 'unescapedUrl'

	searchUrl = rootUrl + urllib.quote(searchTerm) +'&start='+str(8)+'&userip=MyIP&rsz=8&imgtype=photo&safe=active'
	try:
		response = requests.get(searchUrl).json()
		dataInfo = response['responseData']['results']
	except (IndexError,TypeError,ValueError,NameError):  
		print 'skipping'
		return

	currUrl = dataInfo[1][opUrlKey]
	return str(currUrl)