from bs4 import BeautifulSoup
import urllib.request
import os
import sys

default_dir = os.path.join(os.path.expanduser("~"),"Drawr")
if not os.path.exists(default_dir):
    os.makedirs(default_dir)

if(len(sys.argv) > 1):
	for i in range(1,len(sys.argv)):
		html_doc = open(sys.argv[i], "rb")
		nextPage = True
		while nextPage: 
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
				img_data = urllib.request.urlopen(img_url)
				f = open(filename,"wb")
				f.write(img_data.read())
				f.close()
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
			html_doc = urllib.request.urlopen(link)
			
		
	

else:
	print("No arguments found")


	
