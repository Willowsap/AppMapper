import os

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
        content += link + "\n"
      file.write(content)
      file.close()

  def writeUrlsWithErrors(self, filename):
    file = open(filename, "w")
    content = ""
    for url in self.errorUrls:
      content += url.getUrl() + ": " + url.getLinks()[0] + "\n"
    file.write(content)
    file.close()
