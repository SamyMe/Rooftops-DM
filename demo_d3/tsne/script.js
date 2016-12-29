  var w = 900, 
    h = 600;  
	
	var svg = d3.select("body").append("svg").attr({width:w, height:h});


	// --- Manual Scale Definition --- //

	var scalex = d3.scale.linear()
					.domain([-20,20])
					.range([0, w])

	var scaley = d3.scale.linear()
					.domain([-20,20])
					.range([h, 0])


	// -- TSNE INIT PART -- //

	var opt = {}
	opt.epsilon = 10; // epsilon is learning rate (10 = default)
	opt.perplexity = 30; // roughly how many neighbors each point influences (30 = default)
	opt.dim = 2; // dimensionality of the embedding (2 = default)
	var tsne = new tsnejs.tSNE(opt); // create a tSNE instance
	// initialize data. Here we have 3 points and some example pairwise dissimilarities
	var dists = [[10.0, 5, 0.2], [13, 11, 0.3], [8, 21, 1.0]];
	tsne.initDataDist(dists);

	// -------------------- //

	var y = 0  // Y is an array of 2-D points that you can plot

	for(var k = 0; k < 10; k++) {
		tsne.step(); // every time you call this, solution gets better
		y = tsne.getSolution();
		
		console.log(y[0],y[1],y[2]);
		// updatePts(y) // Here it executes only one time
		}
	
	updatePts(y)


	// --------- //

	function updatePts(data){
		svg.selectAll("circle")
			.data(data)
			.enter()
			.append("circle")
				.attr({
					cx: function(d){ return scalex(d[0]);},
					cy: function(d){ return scaley(d[1]);},
					r: 10,
					"fill": "#666666",})	

	}