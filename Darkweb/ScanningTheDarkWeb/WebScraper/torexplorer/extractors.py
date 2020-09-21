import re
import validators
from torexplorer.helpers import validate_bitcoin_wallet
import hashlib
import requests
from torexplorer import settings as settings


def extract_crypto_wallets(html):
    # ethereum = re.compile(r'(0x[a-fA-F0-9]{40})', re.DOTALL | re.MULTILINE)
    # dogecoin = re.compile(r'D{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}', re.DOTALL | re.MULTILINE)
    # monero = re.compile(r'4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}', re.DOTALL | re.MULTILINE)
    bitcoin = re.compile(r'([1,3][123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{26,35})', re.MULTILINE | re.DOTALL)
    bitcoins = []
    coins = set(re.findall(bitcoin, html))
    for coin in coins:
        if validate_bitcoin_wallet(coin):
            bitcoins.append(coin) 
    return bitcoins


def extract_onion_links(html):
    try:
        short = re.compile(r'[a-z2-7]{16}\.onion', re.DOTALL | re.MULTILINE)
        longer = re.compile(r'[a-z2-7]{56}\.onion', re.DOTALL | re.MULTILINE)
        links = re.findall(short, html)
        links.extend(re.findall(longer, html))
        return set(links)
    except:
        return None


def extract_email_addresses(html):
    email = re.compile(r'([\w.-]+@[\w.-]+\.\w+)', re.MULTILINE)
    emails = set(re.findall(email, html))
    valid = []
    for e in emails:
        if '.png' in e:
            pass
        elif validators.email(e):
            valid.append(e)
    return valid


def extract_pgp_blocks(html):
    pgp = re.compile(r"(-----BEGIN [^-]+-----[A-Za-z0-9+\/=\s]+-----END [^-]+-----)", re.MULTILINE)
    return re.findall(pgp, html)

# Thanks to @jms_dot_py for this code
def extract_google_codes(html):
    extracted_codes = []
    google_adsense_pattern = re.compile(r"pub-[0-9]{1,}", re.IGNORECASE)
    google_analytics_pattern = re.compile(r"ua-\d+-\d+", re.IGNORECASE)
    extracted_codes.extend(google_adsense_pattern.findall(html))
    extracted_codes.extend(google_analytics_pattern.findall(html))
    extracted_codes = list(dict.fromkeys(extracted_codes))
    return extracted_codes

# Variables for requests made outside of scraper
headers = {'User-Agent': settings.USER_AGENT}
proxies = {'http': settings.HTTP_PROXY, 'https': settings.HTTP_PROXY}


def find_favicon_hash(website):
    hash = hashlib.md5()
    url = '{0}/favicon.ico'.format(website)
    resp = requests.get(url, headers=headers, proxies=proxies)
    if resp and resp.status_code == 200:
        hash.update(resp.content)
        return hash.hexdigest()
    else:
        return None


def find_robots_information(website):
    url = '{0}/robots.txt'.format(website)
    resp = requests.get(url, headers=headers, proxies=proxies)
    if resp and resp.status_code == 200:
        disallow = []
        lines = resp.text.split('\n')
        for line in lines:
            if 'Disallow' in line:
                disallow.append(line)
        robots = list(filter(None, [str(i.split(': ')[1]).strip('\r').rstrip('/') for i in disallow]))
        return robots