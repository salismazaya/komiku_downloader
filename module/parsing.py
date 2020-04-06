def sorting_manga(data):
	name = data.find("h3").text.lstrip()
	url = data["href"]
	return (name, url)

def get_list_manga(data):
	data = [sorting_manga(x) for x in data.bs4.find_all("a", href = lambda x: "co.id/manga/" in x)]
	return data

def get_latest_chapter(data):
	data  = data.bs4
	data = data.find_all("span", string = lambda x: x and "Chapter" in x)[3].text
	data = data.split(" ")[1]
	return int(data)
		
def get_comic_image(data):
	data = data.bs4
	data = data.find_all("img", alt = lambda x: x and "gambar urutan" in x)
	name = [int(x["alt"].split("urutan ")[1]) for x in data]
	img = [x["src"] for x in data]
	return list(zip(name, img))

def get_manga_url(data):
	data = data.bs4
	data = data.find_all("a", href = lambda x: "pdf.komiku.co.id" in x)
	data = [x["href"] for x in data]
	return data
	
