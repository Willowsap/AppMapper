from crawler import crawler
from urlMap import urlMap

crawler = crawler("https://www.appstate.edu")
crawler.startCrawling()
map = crawler.getMap()
map.writeToFolder("map")
#map.writeToFile("data.txt")
map.writeToJsonFileForD3()