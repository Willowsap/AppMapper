import os
import networkx as nx
import matplotlib.pyplot as plt

class urlMap:
  def __init__(self):
    self.urls = []
    self.errorUrls = []

  def addUrl(self, node):
    self.urls.append(node)
    if len(node.getLinks()) > 0:
      l = node.getLinks()[0]
      if l[0:5] == "ERROR":
        self.errorUrls.append(node)

  def contains(self, url):
    for node in self.urls:
      if node.getUrl() == url:
        return True
    return False

  def newLinks(self, links):
    newLinks = []
    for link in links:
      if not self.contains(link) and link not in newLinks:
        newLinks.append(link)
    return newLinks

  def genGraph(self):
    G = nx.Graph()
    G.add_nodes_from(self.genNodes())
    G.add_edges_from(self.genEdges())
    nx.draw(G, with_labels=False, font_weight='bold')
    plt.show()

  def genEdges(self):
    edges = []
    for url in self.urls:
      for link in url.getLinks():
        if self.contains(link): #and (self.formatUrl(link), self.formatUrl(url.getUrl())) not in edges:
          edges.append((self.formatUrl(url.getUrl()), self.formatUrl(link)))
    return edges
  
  def genNodes(self):
    nodes = []
    for url in self.urls:
      nodes.append(url.getUrl())
    return nodes
  
  def writeToJsonFileForD3(self):
    file = open("scripts/d3data.json", "w")
    content = "{\n\t\"nodes\": ["
    for url in self.urls:
      content += "\n\t\t{ \"id\": \""
      content += self.formatUrl(url.getUrl())
      content +="\", \"group\": 1},"
    content = content[:-1] #get rid of trailing comma
    content += "\n\t],\n\t\"links\": ["
    for url in self.urls:
      for link in url.getLinks():
        if self.contains(link):
          content += "\n\t\t { \"source\": \""
          content += self.formatUrl(url.getUrl())
          content += "\", \"target\": \""
          content += self.formatUrl(link)
          content += "\", \"value\": 1 },"
    content = content[:-1] #get rid of trailing comma
    content += "\n\t]\n}"
    file.write(content)
    file.close()

  def writeToJsonFile(self):
    file = open("scripts/data.json", "w")
    content = "{\n\t\"nodes\": ["
    for url in self.urls:
      content += "\n\t\t{\n\t\t\t\"id\": \""
      content += self.formatUrl(url.getUrl())
      content +="\"\n\t\t},"
    content = content[:-1] #get rid of trailing comma
    content += "\n\t],\n\t\"edges\": ["
    for url in self.urls:
      for link in url.getLinks():
        if self.conains(link):
          content += "\n\t\t { \"from\": \""
          content += self.formatUrl(url.getUrl())
          content += "\", \"to\": \""
          content += self.formatUrl(link)
          content += "\" },"
    content = content[:-1] #get rid of trailing comma
    content += "\n\t]\n}"
    file.write(content)
    file.close()

  def writeToFolder(self, folderName):
    if not os.path.exists(os.getcwd() + "\\" + folderName):
      os.mkdir(folderName)
    for url in self.urls:
      fileName = url.getUrl()[7:].replace("/", "").replace("\\", "").replace("\"", "").replace("<", "").replace("> ", "").replace(":", "").replace("?", "").replace("*", "").replace("|", "").replace("\r", "").replace("\n", "") + ".txt"
      file = open(folderName + "/" + fileName, "w")
      content = url.getUrl() + "\n\n"
      for link in url.getLinks():
        content += link + "\n"
      file.write(content)
      file.close()
      
  def writeUrlsToFile(self, filename):
    file = open(filename, "w")
    content = ""
    for url in self.urls:
      content += url.getUrl() + "\n"
    file.write(content)
    file.close()
  
  def writeUrlsWithErrors(self, filename):
    file = open(filename, "w")
    content = ""
    for url in self.errorUrls:
      content += url.getUrl() + ": " + url.getLinks()[0] + "\n"
    file.write(content)
    file.close()

  def formatUrl(self, url):
    return url.replace("\r", "").replace("\n", "").replace("\"", "'")