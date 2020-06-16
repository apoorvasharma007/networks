#Apoorva Sharma
'''
In this program the fundamental task is to query a webpage and parse it , extracting all the hyperlinks on the webpage. This enables us to do a lot many amazing things like making an index of webpages to deploy a search engine or to scrape useful data from a webpage, etc. I have used BS4 which has library functions of Beautiful Soup module which makes parsing webpages easier. I have used the default html.parser for parsing the webpages.

'''
import requests # For querying a webpage. 
from bs4 import BeautifulSoup  # For parsing the webpage using html.parser



def crawl(base_url,max_pages): #the function crawl , given a webpage , collects all the hyperlinks on that page.  
	page = 1                   # This program can crawl the webpages linked to the starting page . The user will set a limit on how many pages should be crawled.
	url_dict = {base_url: 0}   # Since two hyperlinks might loop back to the same webpage, I have used a map to make sure each webpage is visited only once.
	list_of_url = [base_url]   # Stores list of URL's.
	for url in list_of_url: 
		if url_dict.get(url) == 0 and page <= max_pages:
			url_dict[url] = 1      # Map structure to ensure each webpage is visited only once. When start crawling on a page, mark it visited. 
			webpage = requests.get(url) # Queries a webpage from the python script.
			webpage_text = webpage.text # Extracts all the HTML text from the webpage.   
			bs = BeautifulSoup(webpage_text,features="html.parser")  # Invokes a html.parser to parse the html extracted.
			print("LINKS ON PAGE %d ARE-- \n"%(page) )   
			for link in bs.findAll('a'):    # Parsing the webpage for hyperlinks contained in the anchor tag. 
				title = link.string         
				href = url + link.get('href') # Store the address of this page to crawl it further, if required.
				url_dict[href]=0              # Mark the address as unvisited in the map. 
				list_of_url.append(href) 
				print(title)                  # Print the hyperlink and its title.
				print(href)                     
			page+=1
			print()		


url="https://www."+input("ENTER URL (FORMAT: google.com) : ") +"/"    # Take in put of a url from the user.

maxPages=int(input("MAXIMUM WEB PAGES TO CRAWL: "))                   # Query for number of pages to be crawled.
print("CRAWLING : " + url + "\n" )
crawl(url,maxPages)		 # Crawl the specifed number of pages beginning from the given URL.
