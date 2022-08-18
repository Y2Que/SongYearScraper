
from statistics import mode
import requests
import re
import creds as c

#
# This function takes an input string and looks for the
# word release and a year within the text.
# The return value is 'None' or the year found
#
def search_for_release_year(strInput):

    # set unput string to lower case
    strInput = strInput.lower()

    # search for the word release before or after a year beginning with 19 or 20
    regexYear = re.search(r'(release.*(19|20)\d{2})|((19|20)\d{2}.*release)', strInput)
    # if release year found, get year
    if regexYear:
        releaseYear = re.search(r'(19|20)\d{2}', regexYear.group(0)).group(0)
    else:
        releaseYear = "None"

    return releaseYear

debugEnabled = False

query = "release date, song, Michael Jackson Billie Jean"

# use the first page in the search results.
page = 1

# constructing the URL
# doc: https://developers.google.com/custom-search/v1/using_rest
# calculating start, (page=2) => (start=11), (page=3) => (start=21)
pageStart = (page - 1) * 10 + 1
url = f"https://www.googleapis.com/customsearch/v1?key={c.API_KEY}&cx={c.SEARCH_ENGINE_ID}&q={query}&start={pageStart}"

# make the API request
data = requests.get(url).json()
results = []

# get the result items
search_items = data.get("items")
# iterate over 10 results found
for index, search_item in enumerate(search_items, start=1):
    try:
        long_description = search_item["pagemap"]["metatags"][0]["og:description"]
    except KeyError:
        long_description = "N/A"
    # get the page title
    title = search_item.get("title")
    # page snippet
    snippet = search_item.get("snippet")
    # alternatively, you can get the HTML snippet (bolded keywords)
    html_snippet = search_item.get("htmlSnippet")
    # extract the page url
    link = search_item.get("link")

    # look for release year
    release_year = search_for_release_year(long_description)
    if release_year == "None":
        release_year = search_for_release_year(snippet)

    if release_year != "None":
        results.append(int(release_year))

    # print the results
    if debugEnabled:
        print("="*10, f"Result #{index+pageStart-1}", "="*10)
        print(f"Title: {title}")
        print(f"Release Year: {release_year}")
        print(f"Snippet: {snippet}")
        print(f"Description: {long_description}")
        print(f"URL: {link}")

print(results)
print(mode(results))
