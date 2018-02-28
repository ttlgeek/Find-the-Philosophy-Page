#! python3

import bs4
import requests
import urllib
import time

target_url = "https://en.wikipedia.org/wiki/Philosophy"

def find_first_link(url):
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")

    # stores the first link found in the article, if the article contains no
    # links this value will remain None
    article_link = None

    # Find all the direct children of content_div that are paragraphs
    for element in content_div.find_all("p", recursive=False):
        # Find the first anchor tag that's a direct child of a paragraph.
        # It's important to only look at direct children, because other types
        # of link, e.g. footnotes and pronunciation, could come before the
        # first link to an article. Those other link types aren't direct
        # children though, they're in divs of various classes.
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get('href')
            break

    if not article_link:
        return

    # Get url from relative article_link url
    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)

    return first_link

def continue_crawl(search_history, target_url, max_steps=25):
    if search_history[-1] == target_url:
        print("We've found the target article!")
        return False
    elif len(search_history) > max_steps:
        print("The search has exceeded the provided maximum steps, aborting search!")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("We've arrived at an article we've already seen, aborting search!")
        return False
    else:
        return True



start_url = ''


while "wikipedia.org" not in start_url:
	start_url = input('Please enter a valid wikipedia article URL: ')

maximum_steps = 0
while maximum_steps <= 0:
	maximum_steps = int(input("Please provide number of maximum steps: "))

article_chain = [start_url]

while continue_crawl(article_chain, target_url, maximum_steps):
    print(article_chain[-1])

    first_link = find_first_link(article_chain[-1])
    if not first_link:
        print("We've arrived at an article with no links, aborting search!")
        break

    article_chain.append(first_link)

    time.sleep(2) # Slow things down to not DDoS wikipedia servers.