import requests as r
from bs4 import BeautifulSoup as bs

def get(url, **kwargs):
	data = r.get(url, **kwargs)
	data.bs4 = bs(data.text, "html.parser")
	return data

def post(url, **kwargs):
	data = r.post(url, **kwargs)
	data.bs4 = bs(data.text, "html.parser")
	return data
