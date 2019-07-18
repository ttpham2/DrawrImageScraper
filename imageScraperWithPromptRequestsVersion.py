from bs4 import BeautifulSoup
from io import BytesIO
from time import sleep
import requests
import os
import sys
import shutil

default_dir = os.path.join(os.path.expanduser("~"),"Drawr")
if not os.path.exists(default_dir):
    os.makedirs(default_dir)

print("Enter the home url of drawr user")
user_input = input()
if user_input.find("http://") is -1:
	user_input = "http://" + user_input

req = requests.get(user_input,headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0'})
html_doc = req.text
nextPage = True
count = 0
while nextPage is True:
	count = count + 1
	print(count)
	#if(count % 2) is 0:
	#	sleep(5)
	soup = BeautifulSoup(html_doc, "html.parser")
	
	img_list = []
	
	for item in soup.find_all("div", class_="entryArea"):
		desc = item.find("div", class_="entryAreaInner")
		desc = item.find("div", class_="entryAreaImg")
		desc = desc.img['src']
		img_list.append(desc)
	
		
	user_dir = os.path.join(default_dir,soup.title.get_text())
	if not os.path.exists(user_dir):
		os.makedirs(user_dir)
	
	itr = 0
	for img in img_list:
		img_url = img_list[itr]
		filename = os.path.join(user_dir, img_url.split("/")[-1])
		img_data = requests.get(img_url, stream=True, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0'})
		f = open(filename,"wb")
		img_data.raw.decode_content = True
		#for chunk in img_data.iter_content(chunk_size=1024):
		#	f.write(chunk)
		#	f.flush()
		f.write(img_data.content)
		#shutil.copyfileobj(BytesIO(img_data.raw), f)
		f.close()
		print("Wrote image to" + filename)
		sleep(.3)
		itr = itr + 1
	
	page_links = []
	
	for item in soup.find_all("li", class_="left-food-link"):
		link = item.a
		page_links.append(link)
	
	#page_links[0] = newer page; page_links[1] = older page
	#first page doesn't have a newer page link, and last page doesn't have a older page link
	#as such, those items will be None in page_links
	if page_links[1] is None:
		nextPage = False
	else:
		link = link['href']
		link = "http://drawr.net" + link
	if nextPage is True:
		sleep(2)
		req = requests.get(link,headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0'})
		html_doc = req.text
	

print("finished")



	
