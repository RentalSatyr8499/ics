# Fuzzer skeleton code

import args, urllib.request, uvicorn

def fuzz(args):
    """Fuzz a target URL with the command-line arguments specified by ``args``."""
    fileName = args[args.index("-w")+1]
    URLTemplate = givenBaseURLreturnURLTemplate(args[args.index("-u")+1])

    words = givenFileReturnWords(fileName)
    validURLs = findValidUrls(words, URLTemplate)

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
    for i in words:
        pass


# do not modify this!
if __name__ == "__main__":
    arguments = args.parse_args()
    fuzz(arguments)
