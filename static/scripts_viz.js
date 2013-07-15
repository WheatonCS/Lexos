$(function() {

	// Spinner Functionality
	$( "#minlength" ).spinner({
		step: 1,
		min: 0
	});
	$( "#graphsize" ).spinner({
		step: 10,
		min: 100,
		max: 3000
	});
	
	// Multiselect Dropdown Functionality
	$("#segmentlist").multiselect({
		noneSelectedText: "Select Segments",
		selectedText: "# of # checked"	
	});

	// Ensure that the default pointer is used
	$('.container').css('cursor', 'default');

});


// BUBBLEVIZ - by Scott Kleinman
// BubbleViz is based on http://www.infocaptor.com/bubble-my-page.

$(function() {
	// Append tooltip div to body
	var tooltip = d3.select("body")
		.append("div")
		.style("position", "absolute")
		.style("z-index", "10")
		.style("visibility", "hidden")
		.attr("class", "bubbletip")
		.text("Default");

	// Configure the graph
	var diameter = $("#graphsize").val(),
		format = d3.format(",d"),
		color = d3.scale.category20c();

	var bubble = d3.layout.pack()
		.sort(null)
		.size([diameter, diameter])
		.padding(1.5);

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
		.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

	// Append the bubbles
	node.append("circle")
		.attr("r", function(d) { return d.r; })
		.style("fill",function(d,i){return color(d.className);}) // Use packageName for clustered data
		.on("mouseover", function(d) {
			d3.select(this).style("fill", "gold");
			tooltip.html(d.className+"<br />"+d.value);
			tooltip.style("visibility", "visible");
		})
		.on("mousemove", function(d,i) {
			tooltip.style("top", (event.pageY-35)+"px").style("left",(event.pageX+10)+"px");
		})	
		.on("mouseout", function() {
			d3.select(this).style("fill", function(d,i) { return color(d.className); });
			tooltip.style("visibility", "hidden");
		});

	// Append the labels
	node.append("text")
		.attr("dy", ".3em")
		.style("text-anchor", "middle")
		.text(function(d) { return d.className.substring(0, d.r / 3); })
		.on("mouseover", function(d) {
			d3.select(this.parentNode.childNodes[0]).style("fill", "gold");
			tooltip.html(d.className+"<br />"+d.value);
			tooltip.style("visibility", "visible");
		})
		.on("mousemove", function(d,i) {
			tooltip.style("top", (event.pageY-35)+"px").style("left",(event.pageX+10)+"px");
		})	
		.on("mouseout", function() {
			d3.select(this.parentNode.childNodes[0]).style("fill", function(d,i) { return color(d.className); });
			tooltip.style("visibility", "hidden");
		});

	// Return a flattened hierarchy containing all leaf nodes under the root.
	function classes(root) {
		var classes = [];

		function recurse(name, node) {
			if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
			else classes.push({packageName: name, className: node.name, value: node.size});
		}

		recurse(null, root);
		return {children: classes};
	}

	// Set the graph height from the diameter
	d3.select(self.frameElement).style("height", diameter + "px");
});