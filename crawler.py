from urlMap import urlMap
from node import node
import urllib2

class crawler:
  def __init__(self, rootUrl):
    self.map = urlMap(rootUrl)
    self.rootUrl = rootUrl
  
  def printData(self, data):
    print(self.getPage(data))
  
  def startCrawling(self):
    self.crawl(self.rootUrl)

  def crawl(self, url):
    while (url[-1] == '/'):
      url = url[0:-1]
    url = url.replace(" ", "%20")
    if self.map.contains(url):
      return
    page = self.getPage(url)
    if page[0:5] == "ERROR":
      self.map.addUrl(node(url, [page]))
      return
    links = self.formatLinks(self.removeDuplicates(self.findLinks(page)))
    self.map.addUrl(node(url, links))
    newLinks = self.map.newLinks(links)
    if len(newLinks) > 0:
      for link in newLinks:
        self.crawl(self.rootUrl + link)
    else:
      return

  def getPage(self, url):
    try:
      response = urllib2.urlopen(url) 
      page = response.read()
      response.close()
    except urllib2.HTTPError, e:
      page = "ERROR-HTTP: " + str(e.code)
    except urllib2.URLError, e:
      page = "ERROR-URL: " + str(e.reason)
    except Exception:
      page = "ERROR-UNKNOWN"
    return page

  def findLinks(self, contents):
    links = []
    parts = contents.split("<a href=\"")
    del parts[0]
    for p in parts:
      if p[0] == "/":
        links.append(p.split("\">")[0])
    return links
  
  def formatLinks(self, links):
    formattedLinks = []
    for link in links:
      if len(link) < 1 or link == "/":
        continue
      while (link[-1] == '/'):
        link = link[0:-1]
      link = link.replace(" ", "%20")
      formattedLinks.append(link)
    return formattedLinks

  def removeDuplicates(self, links):
    newList = []
    for link in links:
      if link not in newList:
        newList.append(link)
    return newList

  def getMap(self):
    return self.map

  def addRoot(self, links):
    for link in links:
      link = self.rootUrl + link
    return links