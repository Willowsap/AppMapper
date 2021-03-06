let xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    document.getElementById("container").appendChild(chart(JSON.parse(this.responseText)));
  }
};
xmlhttp.open("GET", "https://student2.cs.appstate.edu/sapphirewe/AppMapper/scripts/d3data.json", true);
xmlhttp.send();

function chart(data) {
  const height = window.innerHeight - window.innerHeight * 0.1;
  const width = window.innerWidth - window.innerWidth * 0.1;
  const links = data.links.map(d => Object.create(d));
  const nodes = data.nodes.map(d => Object.create(d));
  const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(width / 2, height / 2));

  const tooltipDiv = d3
    .select('body')
    .append('div')
    .style('position', 'absolute')
    .style('z-index', '1')
    .style('visibility', 'hidden')
    .style('background-color', 'white')
    .style('pointer-events', 'none')
    .text('test text')

  const svg = d3.create("svg")
    .attr("viewBox", [0, 0, width, height]);

  const link = svg.append("g")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke-width", d => Math.sqrt(d.value));

  const node = svg.append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr('class', 'node')
    .attr("r", 10)
    .attr("fill", color)
    .on('mouseover', function(d, i)  {
      console.log('node: ', nodes[i.index]);
      tooltipDiv
        .style('visibility', 'visible')
        .text(nodes[i.index].id);
    })
    .on('mousemove', function(d) {
      tooltipDiv
        .style('left', (d.pageX) + "px")
        .style('top', (d.pageY) + "px");
    })
    .on('mouseout', function(d) {
      tooltipDiv
        .style('visibility', 'hidden');
    })
    .call(drag(simulation));

  d3.select('body').select('svg').selectAll('g').selectAll('.node')
    .on('mouseover', function(d)  {
      console.log(d)
      tooltipDiv
        .style('visibility', 'visible')
    })
    .on('mousemove', function(d) {
      console.log(d)
      tooltipDiv
        .style('left', (d.pageX) + "px")
        .style('top', (d.pageY) + "px");
    })
    .on('mouseout', function(d) {
      console.log(d)
      tooltipDiv
        .style('visibility', 'hidden');
    })

  node.append("title")
      .text(d => d.id);

  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);
    node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);
  });
  return svg.node();
}

const drag = (simulation) => {
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }
  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }
  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }
  return d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);
}

const color = () => {
  const scale = d3.scaleOrdinal(d3.schemeCategory10);
  return d => scale(d.group);
}