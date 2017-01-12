
var width = 3000,
    height = 1000;


var tooltip = d3.select('body').append('div')
                .attr('class', 'hidden tooltip');


d3.json("prices_100_words.json", function(data) {


var tooltip = d3.select('body').append('div')
                .attr('class', 'hidden tooltip');

var min_price = d3.min(data.topics, function(d) {return d.price;});
var max_price = d3.max(data.topics, function(d) {return d.price;});

var color = d3.scale.linear()
  .domain([min_price, max_price])
  .range(["#2525da","#ff0000"]);

var scale_x = d3.scale.linear()
  .domain([min_price, max_price])
  .range([0, width]);

var scale_y = d3.scale.linear()
  .domain([min_price, max_price])
  .range([height, 0]);

var collisionPadding = 6,
    clipPadding = 4,
    minRadius = 16, // minimum collision radius
    maxRadius = 65, // also determines collision search radius
    activeTopic; // currently-displayed topic

var r = d3.scale.sqrt()
    .domain([0, d3.max(data.topics, function(d) { return d.count; })])
    .range([0, maxRadius]);

var force = d3.layout.force()
    .charge(0)
    .size([width, height - 20])
    .on("tick", tick);

var node = d3.select(".g-nodes").selectAll(".g-node"),
    label = d3.select(".g-labels").selectAll(".g-label");

d3.select(".g-nodes")
    .attr("class", "g-overlay")
    .attr("width", width)
    .attr("height", height)
    .on("click", clear);

d3.select(window)
    .on("hashchange", hashchange);

d3.select("#g-form")
    .on("submit", submit);

updateTopics(data.topics);

hashchange();

// Update the known topics.
function updateTopics(topics) {
  topics.forEach(function(d) {
    d.r = r(d.count);
    d.cr = Math.max(minRadius, d.r);
    if (isNaN(d.k)) d.k = .5;
    // if x unset, set it to random (?)
    d.x = width - scale_x(d.price);

    d.bias = .4 - Math.max(.1, Math.min(.9, d.k));
  });

  force.nodes(data.topics = topics).start();
  updateNodes();
  updateLabels();
  tick({alpha: 0}); // synchronous update
}

// Update the displayed nodes.
function updateNodes() {
  node = node.data(data.topics, function(d) { return d.name; });

  node.exit().remove();

  var nodeEnter = node.enter().append("a")
      .attr("class", "g-node")
      .attr("xlink:href", function(d) { return "#" + encodeURIComponent(d.name); })
      .call(force.drag);

  var republicanEnter = nodeEnter.append("g")
      .attr("class", "g-republican");

  republicanEnter.append("circle")
  	.attr("r", function(d) { return r(d.count); })
  	.attr("fill", function(d) { return color(d.price); });

}

// Update the displayed node labels.
function updateLabels() {
  label = label.data(data.topics, function(d) { return d.name; });

  label.exit().remove();

  var labelEnter = label.enter().append("a")
      .attr("class", "g-label")
      .attr("href", function(d) { return "#" + encodeURIComponent(d.name); })
      .call(force.drag);

  labelEnter.append("div")
      .attr("class", "g-name")
      .text(function(d) { return d.name; });

  labelEnter.append("div")
      .attr("class", "g-value");

  label
      .style("font-size", "14px" )
      .style("width", function(d) { return d.r * 2.5 + "px"; });

  // Create a temporary span to compute the true text width.
  label.append("span")
      .text(function(d) { return d.name; })
      .each(function(d) { d.dx = Math.max(d.r * 2.5, this.getBoundingClientRect().width); })
      .remove();

  // Compute the height of labels when wrapped.
  label.each(function(d) { d.dy = this.getBoundingClientRect().height; });

  label
      .style("width", function(d) { return d.dx = Math.max(d.r*2, this.getBoundingClientRect().width/2);  })
      .style("color", "#cbca9d")
    .select(".g-value")
      .text(function(d) { return d.price.toFixed(0); });

}

// Simulate forces and update node and label positions on tick.
function tick(e) {
  node
      .each(bias(e.alpha * 105))
      .each(collide(0.5))
      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

  label
      .style("left", function(d) { return (d.x - d.dx / 2) + "px"; })
      .style("top", function(d) { return (d.y - d.dy / 2) + "px"; });
}

// A left-right bias causing topics to orient by party preference.
function bias(alpha) {
  return function(d) {
    d.x += d.bias * alpha;
  };
}

// Resolve collisions between nodes.
function collide(alpha) {
  var q = d3.geom.quadtree(data.topics);
  return function(d) {
    var r = d.cr + maxRadius + collisionPadding ,
        nx1 = d.x - r*10,
        nx2 = d.x + r*10,
        ny1 = d.y - r*10,
        ny2 = d.y + r*10;
    q.visit(function(quad, x1, y1, x2, y2) {
      if (quad.point && (quad.point !== d) && d.other !== quad.point && d !== quad.point.other) {
        var x = d.x - quad.point.x,
            y = d.y - quad.point.y,
            l = Math.sqrt(x * x + y * y),
            r = d.cr + quad.point.r + collisionPadding;
        if (l < r) {
          l = (l - r) / l * alpha;
          d.x -= x *= l;
          d.y -= y *= l;
          quad.point.x += x;
          quad.point.y += y;
        }
      }
      return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
    });
  };
}

// Fisherâ€“Yates shuffle.
function shuffle(array) {
  var m = array.length, t, i;
  while (m) {
    i = Math.floor(Math.random() * m--);
    t = array[m];
    array[m] = array[i];
    array[i] = t;
  }
  return array;
}

// Given two quantities a and b, returns the fraction to split the circle a + b.
function fraction(a, b) {
  var k = a / (a + b);
  if (k > 0 && k < 1) {
    var t0, t1 = Math.pow(12 * k * Math.PI, 1 / 3);
    for (var i = 0; i < 10; ++i) { // Solve for theta numerically.
      t0 = t1;
      t1 = (Math.sin(t0) - t0 * Math.cos(t0) + 2 * k * Math.PI) / (1 - Math.cos(t0));
    }
    k = (1 - Math.cos(t1 / 2)) / 2;
  }
  return k;
}

// Update the active topic on hashchange, perhaps creating a new topic.
function hashchange() {
  var name = decodeURIComponent(location.hash.substring(1)).trim();
}

// Trigger a hashchange on submit.
function submit() {
  var name = this.search.value.trim();
  location.hash = name ? encodeURIComponent(name) : "!";
  this.search.value = "";
  d3.event.preventDefault();
}

// Clear the active topic when clicking on the chart background.
function clear() {
  location.replace("#!");
}

// Rather than flood the browser history, use location.replace.
function click(d) {
  location.replace("#" + encodeURIComponent(d === activeTopic ? "!" : d.name));
  d3.event.preventDefault();
}

// When hovering the label, highlight the associated node and vice versa.
// When no topic is active, also cross-highlight with any mentions in excerpts.
function mouseover(d) {
  node.classed("g-hover", function(p) { return p === d; });
  if (!activeTopic) d3.selectAll(".g-mention p").classed("g-hover", function(p) { return p.topic === d; });

  tooltip.classed('hidden', false)
            .attr('style', 'left:' + (mouse[0] + 10) + 'px;' +
                           'top:' + (mouse[1] - 20) + 'px')
            .html(d.name + ": " + (value ? value : "no data"));

}

// When hovering the label, highlight the associated node and vice versa.
// When no topic is active, also cross-highlight with any mentions in excerpts.
function mouseout(d) {
  node.classed("g-hover", false);
  if (!activeTopic) d3.selectAll(".g-mention p").classed("g-hover", false);

  tooltip.classed('hidden', true);

}
});
