import feedparser
import justext
import pickle
import requests
import sys

face_data = OrderedDict()
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "news.pickle"), 'rb') as f:
    news_data = pickle.load(f)

def get_text(link):
    """
    Given an URL link, return the text for the stored article
    """
    response = requests.get(link)
    paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
    text = "\n\n".join([p.text for p in paragraphs if not p.is_boilerplate])
    return text

def collect(url, limit, filename="news.pickle"):
    """
    Saves the articles of an article into a pickle file that you can specify
    """
    # read RSS feed
    d = feedparser.parse(url)
    
    # grab each article
    texts = {}
    for entry in d["entries"][:limit]:
        link = entry["link"]
        print("downloading: " + link)
        text = get_text(link)
        texts[link] = text
    
    # pickle
    pickle.dump(texts, open(filename, "wb"))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python collect_rss.py <url> <filename>")
        sys.exit(1)
    
    # https://www.reuters.com/tools/rss
    # http://feeds.reuters.com/Reuters/domesticNews
    url = sys.argv[1]
    filename = sys.argv[2]
    collect(url, filename)

