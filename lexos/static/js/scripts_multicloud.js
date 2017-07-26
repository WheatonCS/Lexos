$(document).ready(function(){
	// Add tooltip to the DOM
	var tooltip = d3.select("body").append("div")
				.attr("class", "d3tooltip tooltip right")
				.style("opacity", 0);
	d3.select(".d3tooltip").attr("role", "tooltip");

	// Error handler (legacy code)
/*	$("form").submit(function(e){
		if ($("#multicloudtopicfile").is(":checked") && $("#mcfilesselectbttnlabel").html() == ""){
			$('#error-message').text("No MALLET topic file uploaded.");
			$('#error-message').show().fadeOut(3000, "easeInOutCubic");
			return false;
		} else if ($("#multiclouduserfiles").is(":checked") && $("input[name='segmentlist']:checked").length < 1) {
			$('#error-message').text("No documents selected from actives.");
			$('#error-message').show().fadeOut(3000, "easeInOutCubic");
			return false;
		} else{
			$("#status-visualize").css({"visibility":"visible", "z-index": "400000"});
			return true;
		}
	});*/

	// Show filename of uploaded file
	$('.multicloud-upload').change(function(ev) {
		filename = ev.target.files[0].name;
		$('#bttnlabel').html(filename);
	});

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
			$(".ui-selected input").trigger("click"); 
		}
	});

	// Display the document selection options on page load
	$("#multicloud-selection").show();
	$("#multicloud-upload").hide();
});

function renderClouds(dataset, wordCounts) {
	// Decrease the first wordScale domain numbers to increase size contrast
	wordScale = d3.scale.linear().domain([1,5,50,500]).range([10,20,40,80]).clamp(true);
	wordColor = d3.scale.linear().domain([10,20,40,80]).range(["blue","green","orange","red"]);

	numSegments = dataset.length;
	//console.log(numSegments + ' segments');

	$('<ul id="sortable">').appendTo('#multicloud-container');

	for (i = 0; i < numSegments; i++) {
		$('<li class="ui-state-default" id="cloud'+i+'">').appendTo('#sortable');
		
		viz = d3.select("#cloud"+i).append("svg")
				.attr("width", 300)
				.attr("height", 380)
				.attr("id", "svg" + i);
	}
		
	for (i = 0; i < numSegments; i++) {
		statusText = d3.select("#status");
		segment = dataset[i];
		label = segment["name"];
		children = segment["children"];
		/* This array is now generated on the server and supplied in the 
		   ajax response. However, the client-side function is kept for reference. */ 
		//wordCounts = constructWordCounts(children);

		function draw(words) {
			// Create the tooltip
			var tooltip = d3.select("body").select("div.d3tooltip").attr("id",i);

			var viz = d3.select("#svg" + i);
			
			viz.append("g")
				.attr("transform", "translate(150,190)")
				.attr("class", "bigG"+i)
			.selectAll("text")
				.data(words)
			.enter().append("text")
				.attr("id", function(d) {return wordCounts[d.text]; })
				.attr("title", i)
				.style("font-size", function(d) { return d.size + "px"; })
				.style("fill", function(d) { return wordColor(d.size); })
				.style("opacity", .75)
				.style('cursor', 'pointer')
				.attr("text-anchor", "middle")
				.attr("transform", function(d) {
					return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
				})
				.text(function(d) { 
					//return decodeURIComponent(escape(d.text)); 
					return d.text; 
				})
				.on("mouseover", function(d) {
					tooltip.transition()
			        	.duration(200)
			            .style("opacity", 1);
			        tooltip.html('<div class="tooltip-arrow"></div><div class="tooltip-inner">'+(d.text)+': '+(d.size)+'</div>');		       
				})
	    		.on("mousemove", function(d) {
	        		return tooltip
	            	.style("left", (d3.event.pageX + 5) + "px")
	            	.style("top", (d3.event.pageY - 20) + "px");
	      		})
	      		.on("mouseout", function(d) {
	          		tooltip.transition()
	               	.duration(200)
	               	.style("opacity", 0);
	      		});

			viz.append("text")
				.data(label)
				.style("font-size", 14)
				.style("font-weight", 900)
				.attr("x", 65) //100
				.attr("y", 20) //15
				//.attr("x", function(){ return 150-this.getBBox().width/2; })
				.text(function(d) {
					return escape(label); 
					//return decodeURIComponent(escape(label)); 
				});			
		}

		d3.layout.cloud().size([280, 290])
				.words(children)
				.rotate(function() { return ~~(Math.random() * 2) * 5; })
				.fontSize(function(d) { return wordScale(d.size); })
				.on("end", draw)
				.start();
	}

	if ($("#svg0")[0]) { 
		$( "#tips" ).html("<p>Drag the clouds to rearrange them.</p>");
	}

	/* For reference: the wordCounts array is now generated server-side. */
	/*function constructWordCounts(list) {
		wordCounts = {};

		for (var i = 0; i < list.length; i++) {
			word = list[i].text;
			count = list[i].size;

			wordCounts[word] = count;
		}

		return wordCounts;
	}*/

	$( "#sortable" ).sortable({ revert: 100 });
	$( "#sortable" ).disableSelection();


}

// Make pre-Ajax implementation work
$(window).on("load", function(dataset, wordCounts) {
	renderClouds(dataset);
});