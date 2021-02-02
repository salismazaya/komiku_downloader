# https://github.com/salismazaya/komiku_downloader

import requests as r
from PIL import Image as PilImage
from io import BytesIO
from bs4 import BeautifulSoup as bs

ses = r.Session()
ses.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"

baseUrl = "https://komiku.id"

def search(query: str) -> list:
	rv = []
	html = ses.get("https://data3.komiku.id/cari/?post_type=manga&s=" + query.replace(" ", "+")).text
	soup = bs(html, "html.parser")
	data = soup.find_all("div", class_ = "kan")

	for manga in data:
		manga = manga.find("a", href = lambda x: x and "manga" in x)
		mangaName = manga.h3.text.strip()
		mangaId = manga["href"].split("/")[2]
		rv.append((mangaName, mangaId))

	return rv


def getEpisode(mangaId: str) -> list:
	rv = []
	html = ses.get("{}/manga/{}/".format(baseUrl, mangaId)).text
	soup = bs(html, "html.parser")
	data = soup.find("table", {"id":"Daftar_Chapter"}).find_all("a", href = lambda x: x and "ch" in x)

	for episode in data:
		episodeName = episode["title"]
		episodeId = episode["href"].split("/")[2]
		rv.append((episodeName, episodeId))

	rv.reverse()
	return rv


def getEpisodeImages(episodeId: str) -> list:
	rv = []
	html = ses.get("{}/ch/{}/".format(baseUrl, episodeId)).text
	soup = bs(html, "html.parser")
	data = soup.find("section", {"id":"Baca_Komik"}).find_all("img", alt = True)
	
	for image in data:
		imageName = image["alt"]
		imageUrl = image["src"]
		rv.append((imageName, imageUrl))

	return rv


def convertImagesUrlToPillowObject(imagesUrl: list) -> list:
	rv = []
	for imageUrl in imagesUrl:
		imageByte = r.get(imageUrl).content
		image = PilImage.open(BytesIO(imageByte))
		rv.append(image)

	return rv


def adjustImageSize(pillowImagesObject: list) -> list:
	rv = []
	sizeList = [x.size for x in pillowImagesObject]
	size = max(set(sizeList), key = sizeList.count)

	for image in pillowImagesObject:
		rv.append(image.resize((size[0], image.size[1])))

	return rv


