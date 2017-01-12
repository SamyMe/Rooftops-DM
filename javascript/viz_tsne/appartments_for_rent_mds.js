
function process_data(error, data_json) {
  // main svg def
  var svg = d3.select("svg"),
      width = +svg.attr("width"),
      height = +svg.attr("height");
  var g = svg.append("g");

  // min and max
  var minX=1e12, maxX=-1e12, minY=1e12, maxY=-1e12;
  var minPrice=1e12, maxPrice=-1e12, minArea=1e12, maxArea=-1e12;
  for(i = 0; i < data_json.length; i++) {
    minX = Math.min(minX, data_json[i].x);
    maxX = Math.max(maxX, data_json[i].x);
    minY = Math.min(minY, data_json[i].y);
    maxY = Math.max(maxY, data_json[i].y);
    minPrice = Math.min(minPrice, data_json[i].price);
    maxPrice = Math.max(maxPrice, data_json[i].price);
    minArea = Math.min(minArea, data_json[i].area);
    maxArea = Math.max(maxArea, data_json[i].area);
  }

  // scales
  var xScale = d3.scaleLinear()
                 .domain([minX-3, maxX+3])
                 .range([100, width-10]);
  var yScale = d3.scaleLinear()
                 .domain([minY-1, maxY+1])
                 .range([50, height-10]);
  var innerColorScale = d3.scaleLinear()
                          .domain([minPrice, 3000])
                          .range([0, 1]);
  var outerColorScale = d3.scaleLinear()
                          .domain([0, 0.5, 1])
                          .interpolate(d3.interpolateRgb)
                          .range(["blue", "yellow", "red"]);
  var colorScale = function(x){
    return outerColorScale(innerColorScale(x));
  };
  var circleSize = 4, defaultOpacity = .4;
  var curZoom = 1;

  // data init
  var points = [];
  for(i = 0; i < data_json.length; i++){
    var point = {x: xScale(data_json[i].x),
                 y: yScale(data_json[i].y),
                 color: colorScale(data_json[i].price),
                 codepostal: data_json[i].codepostal,
                 nomagence: data_json[i].nomagence,
                 price: data_json[i].price,
                 area: data_json[i].area,
                 url: data_json[i].url,
                 id: data_json[i].id,}
    points.push(point);
  }

  // tooltips
  var tooltip = d3.select('body').append('div')
                  .attr('class', 'hidden tooltip');

  // append the points
  g.selectAll("circle")
      .data(points)
    .enter().append("circle")
      .attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; })
      .attr("r", circleSize)
      .attr("fill-opacity", defaultOpacity)
      .style("fill", function(d) { return d.color; })
        .on('mousemove', function(d) {
          var mouse = d3.mouse(svg.node())
                        .map(function(d) { return parseInt(d); });
          tooltip.classed('hidden', false)
            .attr('style', 'left:' + (mouse[0] + 20) + 'px;' +
                           'top:' + (mouse[1] - 20) + 'px')
            .html("Price: " + d.price + " €/month"
                  + "</br>Area: " + d.area + " m²"
                  + "</br>Agency: " + d.nomagence
                  + "</br>Code Postal: " + d.codepostal
                  + "</br>Id: " + d.id);
          d3.select(this).style("fill-opacity", 1);

        })
        .on('mouseout', function(d) {
          tooltip.classed('hidden', true);
          d3.select(this).style("fill-opacity", defaultOpacity);
        })
  			.on("click", function(d) {
          window.open(d.url);
        });

  // zoom def
  svg.call(d3.zoom()
           .scaleExtent([.5, 32])
           .on("zoom",function() {
              g.attr("transform", d3.event.transform)
              g.selectAll("circle")
                .attr("r", function(){
                return circleSize / Math.sqrt(d3.event.transform.k);
              });
            }));

  // creation of the legend
  var legend = svg.append("g").attr("class", "legend");
  function add_legend_field(legend, idx, color, label) {
    var pad = 10
    var shift = 18
    legend.append("rect")
      .attr("x", 10)
      .attr("y", idx * shift + pad)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", color);
    legend.append("text")
      .attr("x", 35)
      .attr("y", idx * shift + 15 + pad)
      .text(function(d) { return label;})
  }
  for (var i = 0, legendPrice = 250; i < 11; i++) {
    add_legend_field(legend, i, colorScale(legendPrice), legendPrice);
    legendPrice += 250;
  }
  add_legend_field(legend, 11, colorScale(legendPrice), legendPrice + "+");
}

// queue to load the files efficiently
queue()
  .defer(d3.json,"https://raw.githubusercontent.com/Bennettson/Rooftops/master/clean/data/plots/final_data_mds_euclidean.json")
  .await(process_data);
