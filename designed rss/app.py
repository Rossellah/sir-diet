from flask import Flask, render_template
import feedparser

app = Flask(__name__)

# RSS Feeds
rss_feeds = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'abs_cbn': 'https://news.abs-cbn.com/rss/feed',
    'gma': 'https://www.gmanetwork.com/news/rss/news/',
    'tv5': 'https://www.tv5.com.ph/rss/news'
}

# Custom Links for Specific Publications
custom_links = {
    'abs_cbn': [
        ("Oil prices up in 3rd week of Feb", "https://www.abs-cbn.com/news/business/2025/2/17/oil-prices-up-in-3rd-week-of-feb-0939"),
        ("Amihan, shear line, ITCZ, easterlies affect PH", "https://www.abs-cbn.com/news/weather-traffic/2025/2/17/amihan-shear-line-itcz-easterlies-affect-ph-0813"),
        ("8 standout moments from Biniverse World Tour", "https://www.abs-cbn.com/lifestyle/culture/2025/2/17/8-standout-moments-from-biniverse-world-tour-2025-philippines-1016")
    ],
    'gma': [
        ("Top Stories", "https://www.gmanetwork.com/news/topstories/"),
        ("GMA News Latest", "https://www.gmanetwork.com/news/"),
    ],
    'tv5': [
        ("Pagbabasura sa PUV Modernization", "https://news.tv5.com.ph/recent/watch/Mybai_gu59g/pagbabasura-sa-puv-modernization-ipinananawagan-ng-piston-sa-sona-ni-pbbm--frontline-pilipinas/PL5HOfFlVmenYgTeZyV4SRand70EjT79oP"),
    ]
}

def get_news(publication):
    try:
        print(f"Fetching news from {publication}...")
        feed = feedparser.parse(rss_feeds[publication])

        articles = []
        if feed.entries:
            for article in feed.entries[:3]:  # Limit to 3 articles
                articles.append({
                    'title': article.get("title", "No Title"),
                    'published': article.get("published", "No Date"),
                    'summary': article.get("summary", "No Summary"),
                    'link': article.get("link", "#")
                })
        else:
            print(f"No entries found in the feed for {publication}.")

        # Add custom links if available
        if publication in custom_links:
            for title, link in custom_links[publication]:
                articles.append({
                    'title': title,
                    'published': "Custom Link",
                    'summary': "",
                    'link': link
                })

        return articles

    except Exception as e:
        print(f"Error fetching news from {publication}: {str(e)}")
        return []

@app.route("/")
def index():
    return render_template("home.html", articles=[], publication="Home")

@app.route("/bbc")
def bbc_news():
    articles = get_news('bbc')
    return render_template("home.html", articles=articles, publication="BBC News")

@app.route("/abs-cbn")
def abs_cbn_news():
    articles = get_news('abs_cbn')
    return render_template("home.html", articles=articles, publication="ABS-CBN News")

@app.route("/cnn")
def cnn_news():
    articles = get_news('cnn')
    return render_template("home.html", articles=articles, publication="CNN News")

@app.route("/fox")
def fox_news():
    articles = get_news('fox')
    return render_template("home.html", articles=articles, publication="Fox News")

@app.route("/gma")
def gma_news():
    articles = get_news('gma')
    return render_template("home.html", articles=articles, publication="GMA News")

@app.route("/tv5")
def tv5_news():
    articles = get_news('tv5')
    return render_template("home.html", articles=articles, publication="TV5 News")

if __name__ == '__main__':
    app.run(port=5000, debug=True)