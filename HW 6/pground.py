import urllib.request
request = urllib.request.Request("http://localhost:5001/FUZZ")
request.data = "haiiii".encode("utf-8")
request.add_header('Content-Type', 'text/plain')

response = urllib.request.urlopen(request)
