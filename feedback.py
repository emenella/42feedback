#! /Users/emenella/.brew/bin/python3
import requests
from requests import adapters
from requests.models import Response
from requests.sessions import Session
from bs4 import BeautifulSoup as bs


def login(session: Session):
	response = session.get("https://signin.intra.42.fr")
	bs_content = bs(response.content, "html.parser")
	token = bs_content.find("input", {"name":"authenticity_token"})["value"]
	data = {
		'utf8': '\u2713',
		'authenticity_token': str(token),
		'user[login]': 'emenella',
		'user[password]': '6Exetaquearles!',
		'commit': 'Sign in'
	}
	response = session.post('https://signin.intra.42.fr/users/sign_in',data=data)

def logout(session: Session):
	response = session.get('https://profile.intra.42.fr/')
	bs_content = bs(response.content, "html.parser")
	token = bs_content.find("meta", {"name":"csrf-token"})["content"]
	data = {
		'_method': 'delete',
		'authenticity_token': str(token)
	}
	response = session.post('https://signin.intra.42.fr/users/sign_out',data=data)

def get_project(session: Session, login: str):
	headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://profile.intra.42.fr/',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'If-None-Match': 'W/"d632017c58c246eb0844bf6a409e37e5"',
	}
	response = session.get("https://profile.intra.42.fr/users/emenella", headers=headers)
	parser = bs(response.text, "html.parser")
	links_with_text = []
	for a in parser.find_all('span', {'class': 'marked-title'}):
		for b in a.find_all('a'):
			links_with_text.append(b.get('href'))
	return (links_with_text)

def get_feedback(session: Session, url: str):
	reponse = session.get(url)
	
	
	
def main():
	user = "hjordan"
	session = requests.session()
	login(session)
	logout(session)


main()