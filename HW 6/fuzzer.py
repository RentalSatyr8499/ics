# Fuzzer

import args, urllib.request, uvicorn

debug = False

def fuzz(args):
    """Fuzz a target URL with the command-line arguments specified by ``args``."""
    URLTemplate = givenBaseURLreturnURLTemplate(args.url)
    words = givenFileReturnWords(args.wordlist)
    
    if args.extensions:
        toAdd = []
        for word in words:
            for extension in args.extensions:
                toAdd.append(word + extension)
        words += toAdd

    validURLs = findValidUrls(words, URLTemplate)

    for i in validURLs:
        print(f"{i[0]} {i[1]}")

def givenFileReturnWords(fileName):
    with open(fileName, "r") as f: 
        words = f.read().strip().split("\n")
    return words

def givenBaseURLreturnURLTemplate(baseURL):
    i = baseURL.find("FUZZ")
    return [baseURL[0:i], baseURL[i+4:]]

def findValidUrls(words, URLTemplate):
    validURLs = []
    for word in words:
        currURL = URLTemplate[0] + word + URLTemplate[1]

        if debug: print(f"Trying {word}: {currURL}")

        try:
            response = urllib.request.urlopen(currURL)
            validURLs.append([response.getcode(), currURL])
        except urllib.error.HTTPError as e:
            pass
    return validURLs


# do not modify this!
if __name__ == "__main__":
    arguments = args.parse_args()
    fuzz(arguments)
