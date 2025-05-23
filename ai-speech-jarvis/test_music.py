import webbrowser
import urllib.parse

song = "kesariya"
url = f"https://open.spotify.com/search/{urllib.parse.quote(song)}"
webbrowser.open(url)
