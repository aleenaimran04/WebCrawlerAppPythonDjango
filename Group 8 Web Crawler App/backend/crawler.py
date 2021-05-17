from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from ordered_set import OrderedSet
from .helpers import is_url_valid, get_clean_url, is_link_internal
from concurrent.futures import ThreadPoolExecutor

class Crawler():

    def __init__(self, url, depth=45):
        self.crawled_urls = OrderedSet([])
        if (is_url_valid(url)):
            url = get_clean_url(url, '')
            self.pool = ThreadPoolExecutor(max_workers=20)
            self.depth = depth
            self.index = 0
            self.crawled_urls.add(url)
            self.crawl(url)

    def crawl(self, url):
        found_urls = []
        try:
            page = urlopen(url)
            content = page.read()
            soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer('a'))
            for anchor in soup.find_all('a'):
                link = anchor.get('href')
                if is_url_valid(link):
                    link = get_clean_url(url, link)
                    if is_link_internal(link, url):
                        found_urls.append(link)
                else:
                    pass

        except HTTPError as e:
            print('HTTPError:' + str(e.code) + ' in ', url)
        except URLError as e:
            print('URLError: ' + str(e.reason) + ' in ', url)
        except Exception:
            import traceback
            print('Generic exception: ' + traceback.format_exc() + ' in ', url)

        cleaned_found_urls = set(found_urls)  
        self.crawled_urls |= cleaned_found_urls 
        if (len(self.crawled_urls) > self.depth):
            self.crawled_urls = self.crawled_urls[:self.depth]
            return
        else:
            self.index += 1
            if self.index < len(self.crawled_urls):
                self.crawl(self.crawled_urls[self.index])
            else:
                return
