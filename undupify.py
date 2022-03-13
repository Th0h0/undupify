import argparse
import regex
from urllib.parse import urlparse
import os

currentPath = os.path.dirname(__file__)
os.chdir(currentPath)

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=str, required=False, help= 'file containing all URLs to clean')
parser.add_argument("--output", "-o", action='store_true', help='output file path')

args = parser.parse_args()

alreadySeen = {}

globalUrlFootprint = regex.compile('(?<=(\?|\&).*=)(.*?)(?=(\&|$))')
parametersName = regex.compile('(?<=(\?|&))(.*?)(?==)')     #Extract value at the right [1]
doubleSlashes = regex.compile('(?<=[a-z0-9])(\/.*?\/.*?)(?=(\/|\?))') # => .search().group()

if args.output:
    output = open(args.output, "w")
else:
    output = open("cleaned-URLS.txt", "w")

def getGlobalFootprint(url):
    urlWithEmptyParam = globalUrlFootprint.sub('',url)
    return urlWithEmptyParam

def getParameterNames(url):
    match = parametersName.findall(url)
    parameters = [elem[1] for elem in match]
    return parameters

def getBetweenTwoSlashes(url):
    contentBetweenTwoSlashes = doubleSlashes.search(url)

    if contentBetweenTwoSlashes:
        return contentBetweenTwoSlashes.group()
    else:
        None

def isDuplicate(url, alreadySeen):
    parsing = urlparse(url)
    completeHostname = parsing.netloc
    hostDirectory = alreadySeen.get(completeHostname)

    if hostDirectory:
        footprintSet = hostDirectory[0]
        if getGlobalFootprint(url) in footprintSet:
            #Heuristic 2 : URLs are necessarily duplicate if they just differ from parameters' values
            return True
        else:
            hostDirectory[0].add(getGlobalFootprint(url))
            doubleSlashesContent = getBetweenTwoSlashes(url)
            parametersName = getParameterNames(url)
            twoSlashesContentDirectory = hostDirectory[1].get(doubleSlashesContent)

            if twoSlashesContentDirectory:

                if frozenset(parametersName) in twoSlashesContentDirectory:
                    #Heuristic 3 : URLs are very likely to be duplicate if they have the same content between two first double slashes & have exact same query parameters
                    return True

                else:
                    twoSlashesContentDirectory.add(frozenset(parametersName))

                    # To modify : potentially add other heuristics to determine if there's something to do here
                    ###Define new heuristic here
                    return False

            else:

                hostDirectory[1][doubleSlashesContent] = {frozenset(parametersName)}

                ##Define new heuristic here
                # Input info : host already exists, no met URLs had the same global footprint and contained the same content between two slashes
                # This above case could happen in case URLs have less than two slashes in their path & if only parameter is different

                return False


    else:
        #Heuristic 1 : URLs are not duplicate if they have different hosts

        doubleSlashesContent = getBetweenTwoSlashes(url)
        if doubleSlashesContent:
            dictContent = {doubleSlashesContent: {frozenset(getParameterNames(url))} }
        else:
            dictContent = {}
        alreadySeen[completeHostname] = (set([getGlobalFootprint(url)]), dictContent)
        return False

def main():

    URLS = open(args.file, "r")

    for url in URLS:
        url = url.replace('\n', '')
        parsing = urlparse(url)
        if not isDuplicate(url, alreadySeen):
            output.write(f"{url}\n")
    output.close()


if __name__ == '__main__':
    main()