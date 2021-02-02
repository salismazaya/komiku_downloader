# https://github.com/salismazaya/komiku_downloader

import os
import random
import sys
import platform
import module
from concurrent.futures import ThreadPoolExecutor

mangaList = []
selectedChapter = []
successDownloaded = 0

if not os.path.exists("output"):
	os.mkdir("output")


def randomString(length):
	char = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
	rand = "".join([random.choice(char) for _ in range(length)])

	return rand


def main():
	os.system("clear" if platform.system() == "Linux" else "cls")
	print("\n\t\t[ Komiku Downloader ]\n")

	while True:
		query = input("   [?] enter query : ").strip()
		if query == "":
			print("   [!] blank input\n")
			continue

		data = module.search(query)

		if len(data) <= 0:
			print("   [!] {} not found\n".format(query))
		else:
			break

	for i, manga in enumerate(data):
		mangaList.append((manga[0], manga[1]))
		print("   {}). {}".format(i + 1, manga[0]))


	while True:
		select = input("   [?] select : ")
		if select.strip() == "":
			print("   [!] blank input\n")

		elif not select.isdigit() or int(select) < 1 or int(select) > len(mangaList):
			print("   [!] invalid input\n")
			
		else:
			break

	select = int(select)

	chapter = module.getEpisode(mangaList[select - 1][1])
	print("   [?] total chapter: {}".format(len(chapter)))


	while True:
		startFrom = input("\n   [?] start download from chapter : ").strip()
		if not startFrom.isdigit() or int(startFrom) < 1 or int(startFrom) > len(chapter):
			print("   [!] invalid input")

		else:
			startFrom = int(startFrom)
			break

	while True:
		upTo = input("   [?] up to chapter : ").strip()
		if not upTo.isdigit() or int(upTo) < startFrom or int(upTo) > len(chapter):
			print("   [!] invalid input")

		else:
			upTo = int(upTo)
			break

	folderOutput = randomString(6)
	os.mkdir("output/" + folderOutput)
	selectedChapter = chapter[startFrom - 1:upTo]
	print()
	with ThreadPoolExecutor(max_workers = 10) as t:
		t.map(lambda x: process(x, len(selectedChapter), folderOutput), selectedChapter)

	print("\n   [+] done! file saved in : output/" + folderOutput)


def process(arg, totalList, folderOutput):
	try:
		global successDownloaded
		nameAndImagesUrl = module.getEpisodeImages(arg[1])
		imagesUrl = [x[1] for x in nameAndImagesUrl]
		imagesPillowObject = module.convertImagesUrlToPillowObject(imagesUrl)
		imagesPillowObject = module.adjustImageSize(imagesPillowObject)
		imagesPillowObject[0].save("output/{}/{}.pdf".format(folderOutput, arg[1]), save_all = True, append_images = imagesPillowObject[1:])
		successDownloaded += 1

		persen = round(successDownloaded / totalList * 100, 1)
		sys.stdout.write("\r   [+] downloaded : {}%".format(persen))
		sys.stdout.flush()
	except Exception as e:
		print(e)

main()