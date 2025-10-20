# Fuzzer

import args, urllib.request

debug = False

def fuzz(args):
    """Fuzz a target URL with the command-line arguments specified by ``args``."""
    words = createWordList(args.wordlist)

    # --extensions feature
    if args.extensions:
        toAdd = []
        for word in words:
            for extension in args.extensions:
                toAdd.append(word + extension)
        words += toAdd

    URLTemplate = createURLTemplate(args.url)
    requestTemplate = createRequestTemplate(args)
    validURLs = findValidUrls(words, URLTemplate, requestTemplate, args.match_codes)

    for i in validURLs:
        print(f"{i[0]} {i[1]}")

def createWordList(fileName):
    with open(fileName, "r") as f: 
        words = f.read().strip().split("\n")
    return words

def createURLTemplate(baseURL):
    i = baseURL.find("FUZZ")
    return [baseURL[0:i], baseURL[i+4:]]

def createRequestTemplate(args):
    requestTemplate = urllib.request.Request(args.url)

    # --methods feature
    if args.method: requestTemplate.method = args.method.upper()
    else: 
        requestTemplate.method = 'GET'

    # --header feature
    if args.headers: 
        for header in args.headers:
            header = header.split(":")
            requestTemplate.add_header(header[0], header[1])
    
    # --data feature
    if args.data: 

        if debug: print(f"Attempting to add {args.data.encode("utf-8")} as data.")

        requestTemplate.data = args.data.encode("utf-8")
        requestTemplate.add_header('Content-Type', 'text/plain')

    if debug: print(f"The Request object has {requestTemplate.data} as data.")

    return requestTemplate

def findValidUrls(words, URLTemplate, requestTemplate, validCodes):
    validURLs = []

    if debug: print(f"validCodes: {validCodes}")

    for word in words:
        currURL = URLTemplate[0] + word + URLTemplate[1]

        #if debug: print(f"Trying {word}: {currURL}")
        
        try:
            request = requestTemplate
            request.full_url = currURL

            response = urllib.request.urlopen(request)

            # -mc feature
            if debug: print(f"code: {response.getcode()}")
            if response.getcode() in validCodes:
                validURLs.append([response.getcode(), currURL])

        except urllib.error.HTTPError as e: # ensures that we still identify valid urls even if their response packet has no location header
            if e.code in validCodes: validURLs.append([e.code, currURL])

    return validURLs


# do not modify this!
if __name__ == "__main__":
    arguments = args.parse_args()
    fuzz(arguments)
