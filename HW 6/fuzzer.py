# Fuzzer

import args, urllib.request, uvicorn

debug = True

def fuzz(args):
    print(args)
    """Fuzz a target URL with the command-line arguments specified by ``args``."""
    URLTemplate = givenBaseURLreturnURLTemplate(args.url)
    words = givenFileReturnWords(args.wordlist)
    validURLs = findValidUrls(words, URLTemplate)

    if args.extensions:
        for word in words:
            for extension in args.extensions:
                words.append(word + "." + extension)

    for i in validURLs:
        print(f"{i[0]} {i[1]}")

def givenFileReturnWords(fileName):
    with open(fileName, "r") as f: 
        words = f.read().strip().split("\n")
    return words

def givenBaseURLreturnURLTemplate(baseURL):
    i = baseURL.find("FUZZ")
    return [baseURL[0:i-1], baseURL[i+4:]]

def findValidUrls(words, URLTemplate):
    validURLs = []
    for word in words:

        if debug: print(f"Trying {word}.")

        currURL = URLTemplate[0] + word + URLTemplate[1]
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
