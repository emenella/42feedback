#! /Users/emenella/.brew/bin/python3
from math import fabs
import re
from readline import replace_history_item
import requests
import os
from requests import adapters
from requests.models import Response
from requests.sessions import Session
from bs4 import BeautifulSoup as bs
from lxml import etree
from dotenv import load_dotenv
import json

load_dotenv()
jsonFile = open("data.json", "w")

headers = {
	'authority': 'profile.intra.42.fr',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
	'cache-control': 'max-age=0',
	# Requests sorts cookies= alphabetically
	# 'cookie': '_intra_42_session_production=ba9b1b4ce7dece57c69bb8257302eca2; _ga=GA1.1.451156037.1643927522; user.id=NzcxMTM%3D--0cd1bb825949f0731cf0e37e74860efec5ce3eec; locale=fr; _ga_BJ34XNRJCV=GS1.1.1650568194.26.1.1650568241.0',
	'if-none-match': 'W/"23a262e955568219ffb788a54a2d94f9"',
	'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"Windows"',
	'sec-fetch-dest': 'document',
	'sec-fetch-mode': 'navigate',
	'sec-fetch-site': 'none',
	'sec-fetch-user': '?1',
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
}

def login(session: Session):
	response = session.get("https://signin.intra.42.fr")
	bs_content = bs(response.content, "html.parser")
	token = bs_content.find("input", {"name":"authenticity_token"})["value"]
	data = {
		'utf8': '\u2713',
		'authenticity_token': str(token),
		'user[login]': os.getenv("LOGIN"),
		'user[password]': os.getenv("PASSWORD"),
		'commit': 'Sign in'
	}
	response = session.post('https://signin.intra.42.fr/users/sign_in',data=data)
	print("Login " + str(response.status_code))

def logout(session: Session):
	response = session.get('https://profile.intra.42.fr/')
	bs_content = bs(response.content, "html.parser")
	token = bs_content.find("meta", {"name":"csrf-token"})["content"]
	data = {
		'_method': 'delete',
		'authenticity_token': str(token)
	}
	response = session.post('https://signin.intra.42.fr/users/sign_out',data=data)
	print("Logout " + str(response.status_code))

def get_project(session: Session, url: str):
	response = session.get(url, headers=headers)
	# print(response.text)
	dom = etree.HTML(response.text)
	links_with_text = dom.xpath('//div[2]/div[1]/div/div/span/a')
	result = {}
	for link in links_with_text:
		print(link.text)
		result += get_feedback(session, link.get('href'))
	return result

def get_feedback(session: Session, url: str):
	reponse = session.get(url)
	dom = etree.HTML(reponse.text)
	nbRetry = len(dom.xpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div[2]/div/*"))
	corrector = []
	feedback = []
	reply = []
	result = {}
	for i in range(nbRetry):
		corrector.append(dom.xpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div[2]/div/div[{}]/div/div[6]/div/div[2]/div[1]/b[1]/a/@href".format(i)))
		corrector.append(dom.xpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div[2]/div/div[{}]/div/div[7]/div/div[2]/div[1]/b[1]/a/@href".format(i)))
		corrector.append(dom.xpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div[2]/div/div[{}]/div/div[8]/div/div[2]/div[1]/b[1]/a/@href".format(i)))
		feedback.append(dom.xpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div[2]/div/div[{}]/div/div[6]/div/div[2]/div[2]/span/text()".format(i)))
		feedback.append(dom.xpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div[2]/div/div[{}]/div/div[7]/div/div[2]/div[2]/span/text()".format(i)))
		feedback.append(dom.xpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div[2]/div/div[{}]/div/div[8]/div/div[2]/div[2]/span/text()".format(i)))
		reply.append(dom.xpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div[2]/div/div[{}]/div/div[6]/div/div[2]/div[4]/text()".format(i)))
		reply.append(dom.xpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div[2]/div/div[{}]/div/div[7]/div/div[2]/div[4]/text()".format(i)))
		reply.append(dom.xpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div[2]/div/div[{}]/div/div[8]/div/div[2]/div[4]/text()".format(i)))
	corrector = list(filter(None, corrector))
	feedback = list(filter(None, feedback))
	reply = list(filter(None, reply))
	for i in range(len(corrector)):
		obj = {
			"corrector": corrector[i],
			"feedback": feedback[i],
			"reply": reply[i]
		}
		newKey, newValue =	corrector[i], False
		z = newKey in result and newValue == result[newKey]
		json.dump(obj, jsonFile)
	return result
	
def explore(session: Session, url: str):
	users = {}
	new_key, new_value = url, False
	z = new_key in users and new_value == users[new_key]
	for key in users.keys():
		print(key)
		if users[key] != True:
			tmp = get_project(session, users[key])
			users += tmp
		
	

def main():
	user = "https://profile.intra.42.fr/users/vgallois"
	session = requests.session()
	login(session)
	explore(session, user)
	logout(session)

if __name__ == "__main__":
	main()