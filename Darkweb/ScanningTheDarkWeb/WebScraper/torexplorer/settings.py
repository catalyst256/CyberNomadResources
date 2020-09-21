BOT_NAME = 'torexplorer'

SPIDER_MODULES = ['torexplorer.spiders']
NEWSPIDER_MODULE = 'torexplorer.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False


DOWNLOADER_MIDDLEWARES = {
   'torexplorer.middlewares.ProxyMiddleware': 400,
}


CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS = 3
DOWNLOAD_TIMEOUT = 30

# This is where you define your Tor enabled proxy
HTTP_PROXY = 'http://192.168.157.134:8118'