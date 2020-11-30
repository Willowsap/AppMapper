import os

class urlMap:
  def __init__(self, rootUrl):
    self.rootUrl = rootUrl
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

  def writeToWebFile(self):
    file = open("scripts/getData.js", "w")
    content = "function getData() {\n\treturn {"
    for url in self.urls:
      content += "\n\t\t\"" + url.getUrl().replace("\r", "").replace("\n", "").replace("\"", "'") + "\" : ["
      if len(url.getLinks()) == 0:
        content += "\"\", "
      else:
        for link in url.getLinks():
          content += "\"" + link.replace("\r", "").replace("\n", "").replace("\"", "'") + "\", "
      content = content[:-2]
      content += "],"
    content += "\n\t}\n}"
    file.write(content)
    file.close()

  def writeToJsonFile(self):
    file = open("scripts/data.json", "w")
    content = "{\n\t\"node\": ["
    for url in self.urls:
      content += "\n\t\t{\n\t\t\t\"id\": \""
      content += self.formatUrl(url.getUrl())
      content +="\"\n\t\t},"
    content = content[:-1] #get rid of trailing comma
    content += "\n\t],\n\t\"edges\": ["
    for url in self.urls:
      for link in url.getLinks():
        link = self.rootUrl + link
        if self.contains(link):
          content += "\n\t\t { \"from\": \""
          content += self.formatUrl(url.getUrl())
          content += "\", \"to\": \""
          content += self.formatUrl(link)
          content += "\" },"
    content = content[:-1] #get rid of trailing comma
    content += "\n\t]\n}"
    file.write(content)
    file.close()

  def formatUrl(self, url):
    return url.replace("\r", "").replace("\n", "").replace("\"", "'")

  def writeToFile(self, filename):
    file = open(filename, "w")
    content = ""
    for url in self.urls:
      content += url.getUrl() + "\n"
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
        content += self.rootUrl + link + "\n"
      file.write(content)
      file.close()

  def writeUrlsWithErrors(self, filename):
    file = open(filename, "w")
    content = ""
    for url in self.errorUrls:
      content += url.getUrl() + ": " + url.getLinks()[0] + "\n"
    file.write(content)
    file.close()
