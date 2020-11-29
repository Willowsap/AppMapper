from crawler import crawler

crawler = crawler("https://www.appstate.edu")
crawler.startCrawling()
crawler.writeErrors("errors.txt")