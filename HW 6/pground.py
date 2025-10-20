import urllib.request
request = urllib.request.Request("http://localhost:5001/FUZZ")
validCodes = [450]
validURLs = []

try:
    response = urllib.request.urlopen(request)
    if response.getcode() in validCodes:
        print(f"http://localhost:5001/FUZZ gave code {response.getcode()}.")

except urllib.error.HTTPError as e:
    if e.code in validCodes:
        print(f"http://localhost:5001/FUZZ gave code {e.code}.")
