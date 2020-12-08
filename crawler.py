from urlMap import urlMap
from node import node
import urllib2

class crawler:
  def __init__(self, rootUrl):
    self.map = urlMap()
    self.rootUrl = rootUrl
  
  def printData(self, data):
    print(self.getPage(data))
  
  def startCrawling(self):
    self.crawl(self.rootUrl, [])

  def crawl(self, url, parents):
    if self.map.contains(url):
      return
    page = self.getPage(url)
    newParents = list(parents)
    newParents.append(url)
    if page[0:5] == "ERROR":
      self.map.addUrl(node(url, [page]))
      return
    links = self.allowed(self.formatLinks(self.removeDuplicates(self.findLinks(page))), parents)
    self.map.addUrl(node(url, links))
    newLinks = self.map.newLinks(links)
    if len(newLinks) > 0:
      for link in newLinks:
        self.crawl(link, newParents)
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
    if url == self.rootUrl:
      return page
    else:
      return self.removeHeaderAndFooter(page)

  def allowed(self, links, parents):
    newLinks = []
    for link in links:
      if link not in parents:
        newLinks.append(link)
    return newLinks

  def findLinks(self, contents):
    newLinks = []
    parts = contents.split("<a href=\"")
    del parts[0]
    for p in parts:
      if p[0] == "/":
        newLinks.append((p.split("\">")[0]))
    newLinks = self.addRoot(newLinks)
    #print(newLinks)
    return newLinks
  
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
    newLinks = []
    for link in links:
      newLinks.append(self.rootUrl + link)
    return newLinks
  
  def removeHeaderAndFooter(self, page):
    parts = page.split("<!-- Begin Header Area -->")
    if len(parts) < 2:
      return page
    header = parts[1]
    afterHeader = header.split("<!-- End Header Area -->")
    if len(afterHeader) < 2:
      return page
    lowerPage = afterHeader[1]
    lowerPageParts = lowerPage.split("<!--Begin Footer -->")
    if len(lowerPageParts) < 2:
      return lowerPage
    return lowerPageParts[0]
