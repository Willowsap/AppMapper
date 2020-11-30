class infoPage {
  constructor() {
    this.state = {
      title : "Appstate.edu url Map",
      data : getData()
    }
  }
  getGraphSection(info) {
      let graphSection = document.createElement('div');
      graphSection.setAttribute('id', 'graphWrapper');
      for (const url in info) {
        let data = document.createElement('p')
        data.appendChild(document.createTextNode("URL: " + url))
        data.appendChild(document.createElement('br'))
        let links = "Links: "
        for (let i = 0; i < info[url].length; i++) {
          links += info[url][i] + ", "
        }
        data.appendChild(document.createTextNode(links))
        graphSection.appendChild(data)
      }
      graphSection.appendChild(document.createTextNode(info))
      return { section : "graphSection", content : graphSection };
  }
  createMap(canvas) {
    for (let i = 0; i < 5; i++) {

    }
  }
  loadPage() {
      document.getElementById("pageHeader").innerHTML = this.state.title;
      let graphSection = this.getGraphSection(this.state.data)
      document.getElementById(graphSection.section).appendChild(graphSection.content)
  }
}
let page = new infoPage();
page.loadPage();