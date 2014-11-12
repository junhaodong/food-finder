from flask import Flask, request, url_for, redirect, render_template
import json, urllib

app=Flask(__name__)

tumblrURL = "http://api.tumblr.com/v2/tagged?tag=%s&api_key=R3IuczppduJ\
h8tyKOeIISQnDdAR4jRl6CN5ascDxsX1kTpUBq9"

igURL = "https://api.instagram.com/v1/tags/search?q=snowy&access_token=\
ACCESS-TOKEN"


##TO DO
# need to resize images to scale
# figure out ig api (if possible)
##

#return list of image URLs
def getImageURLs(apiLink, tag):
        url = apiLink % (tag)
        data = urllib.urlopen(url).read()
        result = json.loads(data)
        list = []
        for s in result['response']:
                try:
                        list.append(s['photos'][0]['alt_sizes'][1]['url'])
                except:
                        pass
        return list
                
@app.route("/")
def index():
        return render_template("index.html",tumblrImages=getImageURLs(tumblrURL,"food"))
        
@app.route("/tagged/<tag>")
def tag(tag="foodporn"):
        tumblrStr = ""
	for s in getImageURLs(tumblrURL,tag):
                tumblrStr+= "<img src=%s>" % s
        return tumblrStr
        
if __name__=="__main__":
        app.debug=True
	app.run(host="0.0.0.0")
