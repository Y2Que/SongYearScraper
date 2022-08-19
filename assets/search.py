
from statistics import mode
import requests
import re
import creds as c

#
# This function takes an input string and looks for the
# word release and a year within the text.
#
# Inputs are results of google API
#
# Returns 'None' or the year found
#
def find_release_year(strDescription, strSnippet):

    # define search strings
    strRegex     = r'(release.*(19|20)\d{2})|((19|20)\d{2}.*release)'
    strRegexYear = r'(19|20)\d{2}'

    # set unput string to lower case
    strSnippet = strSnippet.lower()
    strDescription = strDescription.lower()

    # search for the word release before or after a year beginning with 19 or 20
    resultFound = re.search(strRegex, strDescription)
    # search description if not found in snippet
    if not resultFound: resultFound = re.search(strRegex, strSnippet)

    # if release year found, get year
    if resultFound:
        releaseYear = re.search(strRegexYear, resultFound.group(0)).group(0)
    else:
        releaseYear = "None"

    return releaseYear

#
#
#
def parse_google_results(strData, searchResults):

    results = []

    # iterate over Google search results
    for index, result in enumerate(searchResults, start=1):
        try:
            description = result["pagemap"]["metatags"][0]["og:description"]
        except KeyError:
            description = "N/A"

        snippet = result.get("snippet") # page snippet

        # build results
        match (strData):
            case 'date':
                # look for release year
                release_year = find_release_year(description, snippet)
                # add results to list
                if release_year != "None": results.append(release_year)
            case 'artist':
                pass
            case 'albumartist':
                pass
            case 'bpm':
                pass
            case 'genre':
                pass
            case _:
                print('Unknown metadata tag')

    return mode(results)

#
#
#
def print_google_results(searchResults):
    # iterate over Google search results
    for index, result in enumerate(searchResults, start=1):
        try:
            description = result["pagemap"]["metatags"][0]["og:description"]
        except KeyError:
            description = "N/A"

        title = result.get("title")     # get the page title
        snippet = result.get("snippet") # page snippet
        link = result.get("link")       # extract the page url
        # alternatively, you can get the HTML snippet (bolded keywords)
        #html_snippet = search_item.get("htmlSnippet")

        # print the results
        print("="*10, f"Result #{index+pageStart-1}", "="*10)
        print(f"Title: {title}")
        print(f"Snippet: {snippet}")
        print(f"Description: {description}")
        print(f"URL: {link}")

#
# Function googles input string and returns results
#
def google(strData, strQuery):

    # use the first page in the search results
    strData = strData.lower()
    page = 1

    # add key terms to imporve Google results
    match(strData):
        case 'date':
            strQuery = f"{strQuery}, song, release year"
        case 'artist':
            strQuery = f"{strQuery}, song, artists"
        case 'albumartist':
            strQuery = f"{strQuery}, song, album artist"
        case 'bpm':
            strQuery = f"{strQuery}, song, beats per minute"
        case 'genre':
            strQuery = f"{strQuery}, song, genre"
        case _:
            print('Unknown metadata tag')

    # constructing the URL
    # doc: https://developers.google.com/custom-search/v1/using_rest
    # calculating start, (page=2) => (start=11), (page=3) => (start=21)
    pageStart = (page - 1) * 10 + 1
    url = f"https://www.googleapis.com/customsearch/v1" \
        f"?key={c.API_KEY}" \
        f"&cx={c.SEARCH_ENGINE_ID}" \
        f"&q={strQuery}" \
        f"&start={pageStart}"
    data = requests.get(url).json()  # make the API request
    search_items = data.get("items") # get the result items

    #print_google_results(search_items)
    
    final_result = parse_google_results(strData, search_items)

    return final_result