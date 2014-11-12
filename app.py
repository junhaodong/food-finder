from flask import Flask, request, url_for, redirect, render_template
import json
try:
	import urllib2
except:
	import urllib.request as urllib2


app=Flask(__name__)

tumblrURL = "http://api.tumblr.com/v2/tagged?tag=%s&api_key=R3IuczppduJ\
h8tyKOeIISQnDdAR4jRl6CN5ascDxsX1kTpUBq9"

igURL = "https://api.instagram.com/v1/tags/%s/media/recent?client_id=d055f7c865394a4ab5c5cfe1f991f0c8"


#return list of image URLs
def getImageURLs(apiLink, tag):
	url = apiLink % (tag)
        data = urllib2.urlopen(url).read()
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
		
@app.route("/", methods=["GET","POST"])
def index():
	if request.method=="POST":
		search = request.form["search"].replace(' ','')
                if len(search) > 0:
                        return redirect(url_for("tagged",tag = search))
        return tagged("foodporn")
	
@app.route("/tagged/<tag>")
def tagged(tag, error=None):
        if tag == None:
                return redirect(url_for("/"))
        try:
                tumblrImages = getImageURLs(tumblrURL,tag)
                igImages = getImageURLs(igURL,tag)
        except:
                error = "Enter a valid tag to search with!"
                return tagged("foodporn",error)
                #return render_template("index.html", error=error)
	return render_template("index.html", tumblrImages=tumblrImages, igImages=igImages, query=tag, error=error)

	
if __name__=="__main__":
	app.debug=True
	app.run(host="0.0.0.0")
