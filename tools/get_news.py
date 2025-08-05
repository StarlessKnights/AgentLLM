from parent_classes.tool import Tool
import feedparser

class GetNews(Tool):
    name = "get_news"
    description = "gets the latest news articles"
    parameters = {}

    @staticmethod
    def run():
        rss_url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en"

        feed = feedparser.parse(rss_url)

        headlines = []
        for entry in feed.entries[:10]:
            headlines.append({
                "title": entry.title,
            })
        return {
            "status": "success",
            "headlines": headlines
        }
