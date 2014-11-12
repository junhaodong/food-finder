from flask import Flask, request, url_for, redirect, render_template
import json, urllib2

app=Flask(__name__)

tumblrURL = "http://api.tumblr.com/v2/tagged?tag=%s&api_key=R3IuczppduJ\
h8tyKOeIISQnDdAR4jRl6CN5ascDxsX1kTpUBq9"

igURL = "https://api.instagram.com/v1/tags/%s/media/recent?client_id=d055f7c865394a4ab5c5cfe1f991f0c8"

#return list of image URLs
def getImageURLs(apiLink, tag):
	url = apiLink % (tag)
	data = urllib2.urlopen(url).read().decode("utf-8")
	result = json.loads(data)
	list = []
	if apiLink == tumblrURL:
		for s in result['response']:
			try:
				list.append(s['photos'][0]['alt_sizes'][1]['url'])
			except:
				pass
	elif apiLink == igURL:
		for s in result['data']:
			try:
				list.append(s['images']['standard_resolution']['url'])
			except:
				pass
	return list
		
@app.route("/")
def index():
	tumblrImages = getImageURLs(tumblrURL,"foodporn")
	igImages = getImageURLs(igURL,"foodporn")
	return render_template("index.html",tumblrImages=tumblrImages,igImages=igImages)
	
@app.route("/tagged/<tag>")
def tag(tag="foodporn"):
	tumblrStr = ""
	for s in getImageURLs(tumblrURL,tag):
		tumblrStr+= "<img src=%s>" % s
	return tumblrStr
	
if __name__=="__main__":
	app.debug=True
	app.run(host="0.0.0.0")
