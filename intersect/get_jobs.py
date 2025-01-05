import httpx
from selectolax.parser import HTMLParser
from selectolax.lexbor import LexborHTMLParser


# url = 'https://books.toscrape.com/'
url = "https://www.cv-library.co.uk/ai-jobs-in-london?perpage=25&us=1"
# url = "https://uk.indeed.com/jobs?q=ai&l=london&from=searchOnHP&vjk=ca59d58f6db9887c"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    # "Accept-Language": "en-US,en;q=0.5",
    # "Accept-Encoding": "gzip, deflate",
    # "Connection": "keep-alive",
    # "Upgrade-Insecure-Requests": "1",
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "none",
    # "Sec-Fetch-User": "?1",
    # "Cache-Control": "max-age=0",
}

res = httpx.get(
    url,
    headers=headers,
    # proxy="http://132.148.167.243:37798",
)
print(res)
# html = HTMLParser(res.text)
# items = html.css('article.product_pod')
# for item in items:
#     print(item.css_first('h3 a').text())
