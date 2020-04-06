from module import bs4_r, parsing
import requests as r
import os, random, sys

class Class:
	def __init__(self):
		self.data = []
		self.angka = 0
		self.img = []
		self.t_size = 0
		self.random_s = self.random_string()
	
	@staticmethod
	def random_string():
		string = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
		string = "".join([random.choice(string) for _ in range(10)])
		return string
		
	def home(self):
		os.system("clear")
		print("\t\t[ Komiku Downloader ]")
		print("\t\t[ Coded by: salism3 ]\n")
		inp = input(" [?] Enter Query: ")
		self.manga_list(inp)
		for _ in range(10):
			try:
				pilih = int(input(" >>> "))
				if pilih > len(self.data) or pilih < 1:
					raise Exception
				break
			except:
				pass
		else:
			exit(" [!] DAH LAH MALESS ")
		
		self.get_manga(self.data[pilih - 1])
	
	def manga_list(self, data):
		query = data.replace(" ", "+")
		data = bs4_r.get(f"https://komiku.co.id/?post_type=manga&s={query}")
		self.data = parsing.get_list_manga(data)
		for i, x in enumerate(self.data):
			print(f" {i + 1}). {x[0]}")
		
	def get_manga(self, data):
		nama, url = data
		data = bs4_r.get(url)
		self.latest = parsing.get_latest_chapter(data)
		print(f"\n [+] Selected: {nama}")
		print(f" [+] Latest Chapter {self.latest}")
		print(" 1). Download All Chapter")
		print(" 2). Download Some Chapter")
		for _ in range(10):
			try:
				pilih = int(input(" >>> "))
				if pilih > 3 or pilih < 1:
					raise Exception
				break
			except:
				pass
		else:
			exit(" [!] DAH LAH MALESS ")
		self.path = input(" [?] Path to save manga: ")
		if pilih == 1:
			self.download_all_chapter(url)
		elif pilih == 2:
			self.download_some_chapter(url)
	
	def download_all_chapter(self, url):
		os.mkdir(f"{self.path}/{self.random_s}")
		print(f"\n [!] Downloading {self.latest} Chapter")
		name = bs4_r.get(url).bs4.find("title").text
		data = parsing.get_manga_url(bs4_r.get(url))
		data.reverse()
		try:
			for i, x in enumerate(data):
				self.download(i, x)
			print("\n\n [!] Done!!!")
			print(f" [!] Your files saved in: {self.path}/{self.random_s}")
		except:
			print("\n [!] ERRORRRR")
			print(f" [!] Your files saved in: {self.path}/{self.random_s}")
			exit()

	def download_some_chapter(self, url):
		print()
		for _ in range(10):
			try:
				start = int(input(" [?] Start from chapter : "))
				if start < 1 or start > self.latest:
					raise Exception
				break
			except:
				pass
		else:
			exit(" [!] DAH LAH MALESS ")
		for _ in range(10):
			try:
				end = int(input(" [?] End : "))
				if end < start or end > self.latest:
					raise Exception
				break
			except:
				pass
		else:
			exit(" [!] DAH LAH MALESS ")
		os.mkdir(f"{self.path}/{self.random_s}")
		print(f"\n [!] Downloading {end - start + 1} Chapter")
		name = bs4_r.get(url).bs4.find("title").text
		data = parsing.get_manga_url(bs4_r.get(url))
		data.reverse()
		data = data[start - 1:end]
		try:
			for i, x in enumerate(data):
				self.download(i, x)
			print("\n\n [!] Done!!!")
		except:
			print("\n [!] ERRORRRR")
			print(f" [!] Your files saved in: {self.path}/{self.random_s}")
			exit()
		
	def download(self, i, oh):
		url = oh
		name = oh.split("/")[-2]
		url = bs4_r.get(url).bs4.find("a")["href"]
		data = r.get(url).content
		self.t_size += len(data) // 1_000_000
		self.img.append(name)
		open(f"{self.path}/{self.random_s}/{name}.pdf", "wb").write(data)
		sys.stdout.write(f"\r [+] Total Downloaded Chapter: {i + 1}\n [+] Total Size: {self.t_size} mb")
		sys.stdout.flush()
	
gas = Class()
gas.home()