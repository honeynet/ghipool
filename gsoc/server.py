from flask import Flask
import requests
import requests_cache

requests_cache.install_cache(backend="memory", expire_after=60*5)

feed_url = "https://github.com/honeynet-gsoc-bot.private.atom?token=AMG33F9IMED9w6imeyGDf4UXzkS-AfuVks6zeYdwwA=="

app = Flask(__name__)

@app.route("/")
def idx():
	return app.send_static_file("index.html")

@app.route("/feed")
def feed():
	return requests.get(feed_url).content

app.run(threaded=True)