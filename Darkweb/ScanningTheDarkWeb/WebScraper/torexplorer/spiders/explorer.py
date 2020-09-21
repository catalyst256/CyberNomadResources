import scrapy
from scrapy.loader import ItemLoader
from torexplorer.items import TorexplorerItem
from torexplorer.helpers import load_server_list, detect_webpage_encoding
from torexplorer.extractors import extract_crypto_wallets, extract_email_addresses, extract_google_codes, extract_onion_links, extract_pgp_blocks
from torexplorer.extractors import find_favicon_hash, find_robots_information
import datetime


class ExplorerSpider(scrapy.Spider):
    name = 'explorer'

    handle_httpstatus_list = [401, 403, 404]

    def __init__(self, filename=None):
        self.start_urls = load_server_list(filename=filename)

    def parse(self, response):
        loader = ItemLoader(
            item=TorexplorerItem(), response=response
        )
        loader.add_xpath('title', '//title/text()')
        if not response.request.meta.get('redirect_urls'):
            loader.add_value('url', response.url)
        else:
            loader.add_value('url', response.request.meta['redirect_urls'][0])
            loader.add_value('redirected_url', response.url)
            loader.add_value('redirects', response.request.meta.get('redirect_urls', None))
        encoding = detect_webpage_encoding(response.body)
        loader.add_value('status', response.status)
        loader.add_value('last_checked', datetime.datetime.utcnow())
        loader.add_value('encoding', encoding)
        loader.add_value('headers', response.headers.to_unicode_dict())
        if extract_onion_links(response.body.decode(encoding)):
            loader.add_value('links', extract_onion_links(response.body.decode(encoding)))
        loader.add_value('bitcoin', extract_crypto_wallets(response.body.decode(encoding)))
        loader.add_value('pgp', extract_pgp_blocks(response.body.decode(encoding)))
        loader.add_value('google', extract_google_codes(response.body.decode(encoding)))
        loader.add_value('email', extract_email_addresses(response.body.decode(encoding)))
        favicon = find_favicon_hash(response.url)
        if favicon:
            loader.add_value('favicon', favicon)
        robots = find_robots_information(response.url)
        if robots:
            loader.add_value('robots', robots)
        yield loader.load_item()
