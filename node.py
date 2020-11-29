class node:
  def __init__(self, url, links):
    self.url = url
    self.links = links

  def addLink(self, link):
    self.links.append(link)

  def getUrl(self):
    return self.url
  
  def getLinks(self):
    return self.links

  def printUrl(self):
    print(self.url)

  def printLinks(self):
    print(self.links)