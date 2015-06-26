$(function() {
	$("form").submit(function(){
		if ($("input[name='segmentlist']:checked").length < 1) {
			$("#vizsubmiterrormessage").show().fadeOut(3000,"easeInOutCubic");
			return false;
		}
	});

	// Show the loading icon before submit
	$("form").submit(function(e) {
    	var self = this;
    	e.preventDefault();
    	$("#status-prepare").css({"visibility": "visible", "z-index": "400000"});
//    	$("#exspecto-bulla").show(); 
        self.submit();
     	return false; //is superfluous, but I put it here as a fallback
	});

});

$(function(){function updateMaxWordsOpt() {
		if ($("#vizmaxwords").is(':checked')){
			$("#vizmaxwordsopt").show();
		}else {
			$("#vizmaxwordsopt").hide();
		}
	}
updateMaxWordsOpt();
$("#vizmaxwords").click(updateMaxWordsOpt);
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

$(document).ready(function(){
	$("#allCheckBoxSelector").click(function(){
		if (this.checked) {
			$(".minifilepreview:not(:checked)").trigger('click');
		} else {
			$(".minifilepreview:checked").trigger('click');
		}
	});

	var prev = -1; //initialize variable
	$("#vizcreateoptions").selectable({       
		filter: "label",  //Makes the label tags the elts that are selectable
		selecting: function(e , ui){
			var currnet = $(ui.selecting.tagName, e.target).index(ui.selecting);   //gets index of current taget label
			if (e.shiftKey && prev > -1) {      //if you were holding the shift key and there was a box previously clicked
				//take the slice of labels from index prev to index curr and give them the 'ui-selected' class
				$(ui.selecting.tagName,e.target).slice(Math.min(prev,currnet)+1, Math.max(prev,currnet)+1).addClass('ui-selected');
				prev = -1;  //reset prev index
			}else{
				prev = currnet;  //set prev to current if not shift click
			}
		},
		stop: function() {
			//when you stop selecting, all inputs with the class 'ui-selected' get clicked
			$(".ui-selected input", this).trigger("click"); 
		}
	});
});

// BUBBLEVIZ - by Scott Kleinman
// BubbleViz is based on http://www.infocaptor.com/bubble-my-page.

$(window).on("load", function() {
//$(function() {

	if (! $.isEmptyObject(dataset)) {
		preprocess(dataset);
		$("#status-prepare").css("visibility", "hidden");

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
});