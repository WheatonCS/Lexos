// Show the milestone input when the milestone checkbox is checked


function updateMSopt() {
	if ($("#rollinghasmilestone").is(':checked')) {
		$("#rollingmilestoneopt").show();
	} else {
		$("#rollingmilestoneopt").hide();
	}
}

// Make the graph
function makeRWAGraph() {
	var tooltip = d3.select("body").select("div.rwtooltip");
	if ($("#rwagraphdiv").text() == 'True') {
		$("#rwagraphdiv").removeClass('hidden');
		$("#rwagraphdiv").text('');	// Empties out place holder

		d3.selectAll('.save-png').on("click", (function (){
			var $container = $('#rwagraphdiv'),
			// Canvg requires trimmed content
			content = $container.html().trim(),
			canvas = document.getElementById('svg-canvas');

			// Draw svg on canvas
			canvg(canvas, content);

			// Change img from SVG representation
			var theImage = canvas.toDataURL("image/png");
			jQuery('#rwagraphsvg').attr('src', theImage);

			// Open a new window with the image
			var w = window.open();
			var img = $("#rwagraphsvg").clone().css("display", "block");
			var html = $("<div/>");
			html.append("<h3 style='font-size: 30px; margin-left: 0px'>Right click image and choose to open image in new tab</h3>");
			html.append("<h3 style='font-size: 14px; margin-left: 40px'>PNG: Right click and choose to save the image</h3>");
			html.append("<h3 style='font-size: 14px; margin-left: 40px'>PDF: Select your browser's print operation and choose print to PDF</h3>");
			html.append(img);

			$(w.document.body).html(html);
		})); // End Save

		//resume making the graph
		// Size of the graph variables
		var margin = {top: 50, right: 20, bottom: 180, left: 70},
			margin2 = {top: 520, right: 20, bottom: 20, left: 70},
			width = 940 - margin.left - margin.right,
			height = 640 - margin.top - margin.bottom,
			height2 = 640 - margin2.top - margin2.bottom;

		// Scales your x-axis
		var x = d3.scale.linear()
			.range([0, width])
			.domain(d3.extent(dataLines[0], function(d) { return d[0] }));
		// Does same for minigraph below
		var x2 = d3.scale.linear()
			.range([0, width])
			.domain(d3.extent(dataLines[0], function(d) { return d[0] }));

		// Iterates through dataLines lists to find min and max of all values for y-axis
		var yMINS = [];
		var yMAXS = [];

		// Finds max and min y vals for determinine range of y axis
		for (var i=0; i < dataLines.length; i++) {
			yMINS[i] = d3.min(dataLines[i], function(d) { return d[1] });
			yMAXS[i] = d3.max(dataLines[i], function(d) { return d[1] });
		}
		// Defines extent of y axis
		var yExtent = [];
		yExtent[0] = d3.min(yMINS);
		yExtent[1] = d3.max(yMAXS);

		// Makes y axis
		var y = d3.scale.linear()
			.range([height, 0])
			.domain(yExtent);
		// Makes mini y axis
		var y2 = d3.scale.linear()
			.range([100, 0])
			.domain(yExtent);

		// Brushed on brush   // Redraws graph focus to the data contained within brush
		function brushed() {
				x.domain(brush.empty() ? x2.domain() : brush.extent());
				focus.selectAll(".line").attr("d", line);
				focus.select(".x.axis").call(xAxis);
				focus.selectAll(".dot")
					.attr("cx", function(d) {return x(d[0]);})
  				.attr("cy", function(d) {return y(d[1]);});
		}

		// Brush  // Makes brush and binds it to minigraph xaxis
		var brush = d3.svg.brush()
			.x(x2)
			.on("brush", brushed);

		// Color chart
		var colorChart = [
			"red",
			"orange",
			"gold",
			"green",
			"blue",
			"purple"
		];

		/////////////////////////////////////////////////////////////

		// Creates an svg
		svg = d3.select('#rwagraphdiv')
			.append("svg:svg")
				.attr('width', width + margin.left + margin.right)
				.attr('height', height + margin.top + margin.bottom + 100)
				.attr("id", "rwagraphsvg")
				.attr("xmlns", "http://www.w3.org/2000/svg");

		svg.append("rect")
			.attr("width", "100%")
		    .attr("height", "100%")
			.attr("fill", "white");

		var focus = svg.append("g")
				.attr("class", "focus")
				.attr("id", "rwagraphsvg")
				.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		// Adds a rectangle to our svg
		focus.append("svg:rect")
			.attr("width", width)
			.attr("height", height)
			.attr("class", "plot")
			.attr("fill", "gray")
			.attr("opacity", .1);

		// Creates a variable x axis
		var xAxis = d3.svg.axis()
			.scale(x)
			.orient("bottom")
			.ticks(5);

		// Adds our xAxis to our svg g (group of elements)
		focus.append("svg:g")
			.attr("class", "x axis")
			.attr("transform", "translate(0, " + height + ")")
			.call(xAxis);

		// Does the same thing with y axis
		var yAxis = d3.svg.axis()
			.scale(y)
			.orient("left")
			.ticks(10)
			.tickSize(- width, 0, 0);

		focus.append("g")
			.attr("class", "y axis")
			.call(yAxis);

		// y axis label
		focus.append("text")
			.attr("class", "y label")
			.attr("class", "label")
			.attr("text-anchor", "end")
			.attr("x", -180)
			.attr("y", -70)
			.attr("dy", ".75em")
			.attr("transform", "rotate(-90)")
			.text(yAxisLabel);

  		// Creates a variable clip which holds the clipPath
  		var clip = focus.append("svg:clipPath")
			.attr("id", "clip")
			.append("svg:rect")
			.attr("x", 0)
			.attr("y", 0)
			.attr("width", width)
			.attr("height", height);

		// We create a variable called ChartBody
		var chartBody = focus.append("g")
			.attr("class", "chartBody")
			.attr("clip-path", "url(#clip)")
			.on("mousemove", function() {
				var infobox = d3.select(".infobox");
				var coord = [0, 0];
				coord = d3.mouse(this);
					infobox.style("left", coord[0]  + 15 + "px");
					infobox.style("top", coord[1] + "px");
				});

		// Creates scatterplot overlay for line graph and adds browser automatic
		// tooltip for beginning of each window
		if (! noDots){
			for (var i=0; i < dataLines.length; i++) {
				focus.append("g").attr("class", "dotgroup").selectAll(".dot")
  					.data(dataLines[i])
		    		.enter()
		    		.append("circle")
  					.attr("class", "dot")
  					.attr("r", 2)
  					.attr("cx", function(d) {return x(d[0]);})
  					.attr("cy", function(d) {return y(d[1]);})
  					.style("fill", colorChart[i])
  					.on("mouseover", function(d) {
						  tooltip.transition()
               .duration(200)

               .style("opacity", 1);
          tooltip.html(function()

		  		{
			  		return "(" + d[0] + ", " + d[1].toFixed(2) + ")";
				})

               .style("left", (d3.event.pageX) + "px")
               .style("top", (d3.event.pageY) + "px")
		  .on("mouseout", function(d) {
          tooltip.transition()
               .duration(200)
               .style("opacity", 0);
      });
						d3.select(this)
							.style("stroke", "black")
							.style("stroke-width", 3)
							.attr("r", 3);
						d3.select(".infobox")
							.style("display", "block");

						})
  					.on("mousemove", function() {
						var infobox = d3.select(".infobox");
						var coord = [0, 0];
						coord = d3.mouse(this);
							infobox.style("left", coord[0] + 15 + "px");
							infobox.style("top", coord[1] + 380 + "px");
						})
  					.on("mouseout", function() {
						d3.select(this)
							.style("stroke", "none")
							.style("stroke-width", "none")
							.attr("r", 2);
						d3.select(".infobox")
							.style("display", "none");
							})
  					.attr("clip-path", "url(#clip)");
			}
		}

		// Specifies the path data
		var line = d3.svg.line()
			.x(function(d) { return x(d[0]); })
			.y(function(d) { return y(d[1]); });

		// Create legend
		var rwlegend = svg.selectAll(".rwlegend")
  			.data(dataLines)
			.enter()
			.append("g")
  			.attr("class", "rwlegend")
  			.attr("transform", "translate(120,20)");

  		var i = 0;
  		if (! BandW){
  			//append legend rectangles
				rwlegend.append("g:rect")
  				.attr("x", function(d, i) { return i * 145;})
  				.attr("width", 18)
  				.attr("height", 15)
  				.style("fill", function() { i++; return colorChart[i-1];});
  		} else {
  			rwlegend.append("g:rect")
  				.attr("x", function(d, i) { return i * 145;})
  				.attr("width", 18)
  				.attr("height", 15)
  				.style("fill", function() { i++; return "black";});
  		}

  		var j = 0;

			// draw legend text
			rwlegend.append("g:text")
  				.attr("x", function(d, i) { return i * 145 -5;})
  				.attr("y", 9)
  				.attr("dy", ".35em")
  				.style("text-anchor", "end")
  				.text(function() {j++; return legendLabels[j-1]});

  		if (!BandW){
  			// adds a path to our ChartBody
			for (var i=0; i < dataLines.length; i++) {
				chartBody.append("svg:path")
					.datum(dataLines[i])
					.attr("class", "line")
					.attr("d", line)
					.attr("stroke", colorChart[i])
					.attr("fill", "none");
			}
		} else {
			for (var i=0; i < dataLines.length; i++) {
				chartBody.append("svg:path")
					.datum(dataLines[i])
					.attr("class", "line")
					.attr("d", line)
					.attr("stroke", "black")
					.attr("fill", "none");
			}
		}

		////////////////////////////////////////////////////////////

		var context = svg.append("g")
				.attr("id", "rwagraphsvg")
				.attr("class", "context")
				.attr("width", width)
				.attr("height", 100)
				.attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");


		context.append("rect")
			.attr("width", width)
			.attr("height", 100)
			.attr("class", "plot")
			.attr("fill", "gray")
			.attr("opacity", .1);

		// creates a variable x axis
		var xAxis2 = d3.svg.axis()
			.scale(x2)
			.orient("bottom")
			.ticks(5);

		// adds our xAxis to our svg g (group of elements)
		context.append("svg:g")
			.attr("class", "x2 axis")
			.attr("transform", "translate(0, " + height2 + ")")
			.call(xAxis2);

		// x-axis label
		context.append("text")
			.attr("class", "x label")
			.attr("class", "label")
			.attr("text-anchor", "middle")
			.attr("x", 420)
			.attr("y", height2+margin2.bottom+15)
			.text(xAxisLabel);

		// brush ability
		context.append("g")
  			.attr("class", "x brush")
  			.call(brush)
			.selectAll("rect")
  			.attr("y", -6)
  			.attr("height", height2 + 7);

		// creates a variable clip which holds the clipPath
  		var clipTwo = context.append("svg:clipPath")
			.attr("id", "clip2")
			.append("svg:rect")
			.attr("x", 0)
			.attr("y", 0)
			.attr("width", width)
			.attr("height", 100);

		// we create a variable called ChartBody
		var chartBody2 = context.append("g")
			.attr("class", "chartBody2")
			.attr("clip-path", "url(#clip2)");

		// specifies the path data
		var line2 = d3.svg.line()
			.x(function(d) { return x2(d[0]); })
			.y(function(d) { return y2(d[1]); });

  		// adds a path to our ChartBody

  		if (! BandW){
			for (var i=0; i < dataLines.length; i++) {
				chartBody2.append("svg:path")
					.datum(dataLines[i])
					.attr("class", "line")
					.attr("d", line2)
					.attr("stroke", colorChart[i])
					.attr("fill", "none");
			}
		} else {
			for (var i=0; i < dataLines.length; i++) {
				chartBody2.append("svg:path")
					.datum(dataLines[i])
					.attr("class", "line")
					.attr("d", line2)
					.attr("stroke", "black")
					.attr("fill", "none");
			}
		}

		//////////////////////////////////////////////////////////

		//download svg
			d3.selectAll(".download-svg-chrome").on("click", (function (){
			var e = document.createElement('script');
			if (window.location.protocol === 'https:') {
    			e.setAttribute('src', 'https://raw.github.com/NYTimes/svg-crowbar/gh-pages/svg-crowbar.js');
			} else {
    			e.setAttribute('src', 'http://nytimes.github.com/svg-crowbar/svg-crowbar.js');
			}
			e.setAttribute('class', 'svg-crowbar');
			document.body.appendChild(e);
		}));

		d3.selectAll(".download-svg-other").on("click", function() {

			d3.select(this).attr("href", "data:image/svg+xml;charset=utf-8;base64," + btoa(unescape(encodeURIComponent(
		svg.node().parentNode.innerHTML))));

			//document.append("<h3 style='font-size: 30px; margin-left: 0px'>Right click image and choose to open image in new tab</h3>");
//	html.append("<h3 style='font-size: 14px; margin-left: 40px'>PNG: Right click and choose to save the image</h3>");
//	html.append("<h3 style='font-size: 14px; margin-left: 40px'>PDF: Select your browser's print operation and choose print to PDF</h3>");
		});

	} // End if

} // End function makeRWAGraph()


/* document.ready() Functions */
$(function() {
	var tooltip = d3.select("body").append("div")
				.attr("class", "rwtooltip")
				.style("opacity", 0);
	// Call update milestone on page load
	updateMSopt();

	// Bind the function to the checkbox
	$("#rollinghasmilestone").click(updateMSopt);

	// Handle the return to top links
	$('.to-top').click(function(){
	    $("html, body").animate({ scrollTop: 0 }, 800);
	    return false;
	});

	//$("#rollingsearchword, #rollingsearchwordopt").css({"left": "25%", "position": "relative"});

	// Make the graph when the Get Graph button is clicked
	makeRWAGraph();

	$("#getgraph").click(function(e) {

		/* Validation */

		if (numActiveDocs ==0) {
			e.preventDefault();
			msg = "Please select a document to analyze.";
	      	$('#error-modal-message').html(msg);
	      	$('#error-modal').modal();
		}

		if ($("#rollingwindowsize")[0].value=="" || $("#rollingsearchword")[0].value=="") {
			e.preventDefault();
		 	msg = "Please fill out the 'Search Pattern(s)' and 'Size of Rolling Window' fields.";
	      	$('#error-modal-message').html(msg);
	      	$('#error-modal').modal();
		}

		if ($("#inputword").prop('checked') && $("#windowletter").prop('checked')) {
			e.preventDefault();
		    msg = 'You cannot use tokens for search terms when analyzing a window of characters. ';
		    msg += 'The window setting has been changed to a window of tokens.';
		    $('#error-modal-message').html(msg);
		    $('#error-modal').modal();
			$("#windowword").click();
		}

	});

	/* On-Click Validation */
	$("#radiowindowletter").click(function() {
		if ($("#inputword").prop('checked')) {
			$("#windowword").click();
		    msg = 'You cannot use a window of characters when analyzing a token. ';
		    msg += 'The setting has been changed to a window of tokens.';
		    $('#error-modal-message').html(msg);
		    $('#error-modal').modal();
		}
	});

	/* Other UI functionality */

	// Fixes bug where you cannot click second text box in firefox
	$("#rollingsearchwordopt, #rollingsearchword").hover(function() {
		$(this).focus();
	});

	// Sets the value of the hidden input
	$(".minifilepreview").click(function() {
		$("#filetorollinganalyze").val($(this).prop('id'));
	});

	// Shows the second textbox when rolling ratio gets clicked
	$("#radioratio").click(function() {
		$(".rollingsearchwordoptdiv").removeClass("hidden");
	});

	// Removes the second textbox when rolling ratio is not selected
	$("#radioaverage").click(function() {
		$(".rollingsearchwordoptdiv").addClass("hidden");
	});

	// Transfers the value when the input field is checkd
	$("#radioinputletter").click(function() {
		var oldVal = $(".rollinginput").val();
		$(".rollinginput").val(oldVal);
	});

	// Keyboard navigation
	$(".rollinginput").keyup(function(evt) {
		var theEvent = evt || window.event;
		var key = theEvent.keyCode || theEvent.which;
		if (key != 8) { // 8 is backspace
			if ($(this).val().length > 1 && $("#inputletter").prop('checked')) {
				$(this).val($(this).val().slice(0,1));
			}
		}
	});

	// Keyboard navigation
	$("#rollingwindowsize").keypress(function(evt) {
		var theEvent = evt || window.event;
		var key = theEvent.keyCode || theEvent.which;
		if (key != 8) { // 8 is backspace
			key = String.fromCharCode( key );
			var regex = /[0-9]|\./;
			if( !regex.test(key) ) {
				theEvent.returnValue = false;
				if(theEvent.preventDefault) theEvent.preventDefault();
			}
		}
	});
});