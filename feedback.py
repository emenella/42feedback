from requests import Session
import requests
from bs4 import BeautifulSoup as bs

site = requests.get("https://signin.intra.42.fr/users/sign_in")
bs_content = bs(site.content, "html.parser")
token = bs_content.find("meta", {"name":"csrf-token"})["content"]
cookies = {
    'pro.id': 'bnVsbA%3D%3D--af7657a8234901541e1115b23c7a73d93a7191fd',
    '_ga': 'GA1.2.218227450.1624762099',
    '_gid': 'GA1.2.1608978402.1624762099',
    'user.id': 'bnVsbA%3D%3D--af7657a8234901541e1115b23c7a73d93a7191fd',
    '_intra_42_session_production': '169e08120692e438590a9edc18ef79bd',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://signin.intra.42.fr',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://signin.intra.42.fr/users/sign_in',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
}

data = {
  'utf8': '\u2713',
  'authenticity_token': str(token),
  'user[login]': 'emenella',
  'user[password]': '6Exetaquearles!',
  'commit': 'Sign in'
}

response = requests.post('https://signin.intra.42.fr/users/sign_in', headers=headers, cookies=cookies, data=data)
data = requests.get("https://profile.intra.42.fr/")
site = requests.get("https://profile.intra.42.fr/")
bs_content = bs(site.content, "html.parser")
title = bs_content.find("title")
print response.url
print title

