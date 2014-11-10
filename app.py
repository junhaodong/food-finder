from flask import Flask, request, url_for, redirect, render_template
import json, urllib

app=Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/tagged/<tag>")
def tag(tag="foodporn"):
	url = "http://api.tumblr.com/v2/tagged?tag=%s&api_key=R3IuczppduJh8tyKOeIISQnDdAR4jRl6CN5ascDxsX1kTpUBq9"
	url = url%(tag)
	request = urllib.urlopen(url)
	s = request.read()
	result = json.loads(s)
	retstring = ""
	for s in result["response"]:
		print(s)
		try: 
			retstring = retstring + "<img src=%s>"%(s['photos'][0]['original_size']['url'])
			print(retstring)
		except:
			pass
	return retstring


if __name__=="__main__":
	app.debug=True
	app.run(host="0.0.0.0")
