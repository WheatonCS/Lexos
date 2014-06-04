$(function() {
	// Multiselect Dropdown Functionality
	$("#segmentlist").multiselect({
		noneSelectedText: "Select Segments",
		selectedText: "# of # checked"		
	});
});

function preprocess(dataset) { // Used to decode utf-8
	wordData = dataset['children'];

	for (var i = 0; i < wordData.length; i++) {
		wordData[i].name = decodeURIComponent(escape(wordData[i].name));
	}
}
		
// Return a flattened hierarchy containing all leaf nodes under the root.
function classes(root) {
	var classes = [];

	function recurse(name, node) {
		if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
		// Note: decodeURIComponent(escape(node.name)) decodes the utf-8 from python/jinja/etc.
		else classes.push({packageName: name, className: node.name, value: node.size});
	}

	recurse(null, root);
	return {children: classes};
}

// BUBBLEVIZ - by Scott Kleinman
// BubbleViz is based on http://www.infocaptor.com/bubble-my-page.

$(window).on("load", function() {
//$(function() {

	if (! $.isEmptyObject(dataset)) {
		preprocess(dataset);

		// Configure the graph
		var diameter = $("#graphsize").val(),
			format = d3.format(",d"),
			color = d3.scale.category20c();

		var bubble = d3.layout.pack()
			.sort(null)
			.size([diameter, diameter])
			.padding(1.5)
			;

		// Append the SVG
		var svg = d3.select("#viz").append("svg")
			.attr("width", diameter)
			.attr("height", diameter)
			.attr("class", "bubble");
				
		// Append the nodes
		var node = svg.selectAll(".node")
			.data(bubble.nodes(classes(dataset))
			.filter(function(d) { return !d.children; }))
			.enter().append("g")
			.attr("class", "node")
			.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
			
		// Create a d3.tip
		var tip = d3.tip()
			.attr('class', 'd3-tip')
			.html('')
			.direction('n') // Tip location
			.offset([0, 3]);

		svg.call(tip);

		// Append the bubbles
		node.append("circle")
			.attr("r", function(d) { return d.r; })
			.style("fill",function(d,i){return color(d.className);}) // Use packageName for clustered data
			.on("mouseover", function(d) {
				d3.select(this).style("fill", "gold");
				count = d.value;
				tip.html(d.className+"<br />"+count);
				tip.show();
			})
			.on("mousemove", function(d,i) {
				var xy = d3.mouse(svg.node());
				tip.style("left",(xy[0]+325)+"px").style("top", (xy[1]+200)+"px");
			})
			.on("mouseout", function() {
				d3.select(this).style("fill", function(d,i) { return color(d.className); });
				tip.hide();
			});

		// Append the labels
		node.append("text")
			.attr("dy", ".3em")
			.style("text-anchor", "middle")
			.text(function(d) { return d.className.substring(0, d.r / 3); })
			.on("mouseover", function(d) {
				d3.select(this.parentNode.childNodes[0]).style("fill", "gold");
				count = d.value;
				tip.html(d.className+"<br />"+count);
				tip.show();
			})
			.on("mousemove", function(d,i) {
				var xy = d3.mouse(svg.node());
				tip.style("left",(xy[0]+325)+"px").style("top", (xy[1]+200)+"px");
			})	
			.on("mouseout", function() {
				d3.select(this.parentNode.childNodes[0]).style("fill", function(d,i) { return color(d.className); });
				tip.hide();
			});

		// Set the graph height from the diameter
		d3.select(self.frameElement).style("height", diameter + "px");
	}
	$("#exspecto-bullae").fadeOut();
});