$(function() {
	$(".minifilepreview").click(function() {
		$(this).siblings(".minifilepreview").removeClass('enabled');
		$(this).addClass('enabled');
		$("#filetorollinganalyze").val($(this).prop('id'));
	});

	$("#radioratio").click(function() {
		var timeToToggle = 150;
		$(".rollingsearchwordoptdiv").fadeIn(timeToToggle);
	});
	$("#radioaverage").click(function() {
		var timeToToggle = 150;
		$(".rollingsearchwordoptdiv").fadeOut(timeToToggle);
	});

	$("#radioinputletter").click(function() {
		var oldVal = $(".rollinginput").val();
		$(".rollinginput").val(oldVal);
	});

	$("#radioinputword").click(function() {
		if ($("#windowletter").prop('checked')) {
			$("#windowword").click();
		}
	});

	$("#radiowindowletter").click(function() {
		if ($("#inputword").prop('checked')) {
			$("#rwasubmiterrormessage3").show().fadeOut(2500, "easeInOutCubic");
			return false;
		}
	});


	$(".rollinginput").keyup(function(evt) {
		var theEvent = evt || window.event;
		var key = theEvent.keyCode || theEvent.which;
		if (key != 8) { // 8 is backspace
			if ($(this).val().length > 1 && $("#inputletter").prop('checked')) {
				$(this).val($(this).val().slice(0,1));
			}
		}
	});

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

	$("form").submit(function() {
		if ($(".minifilepreview.enabled").length < 1) {
			$("#rwasubmiterrormessage2").show().fadeOut(2500, "easeInOutCubic");
			return false;
		}
		else {
			if ($('#rollingsearchword').val() == '' || $('rollingwindowsize').val() == '') {
				$('#error-message').text("All inputs must be filled out!");
				$('#error-message').show().fadeOut(1500);
				return false;
			}
			else if ($('rollingsearchwordopt').val() == '' && !$('#rollingratio').prop('checked')) {
				$('#error-message').text("A second token must be selected to find a ratio!");
				$('#error-message').show().fadeOut(1500);
				return false;
			}
		}
		var rollingwindowsize = $("#rollingwindowsize").val();
		if (Math.abs(Math.round(rollingwindowsize)) != rollingwindowsize){
			$('#error-message').text("Invalid input! Make sure the size is an integer!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else {
			return true;
		}
	});

	$('#generateRWmatrix').click( function() {
		return true;
	});

	function makeRWAGraph() {
		if ($("#rwagraphdiv").text() == 'True') {
			$("#rwagraphdiv").removeClass('hidden');
			$("#rwagraphdiv").text('');

			// size of the graph variables
			var margin = {top: 50, right: 20, bottom: 180, left: 70},
				margin2 = {top: 520, right: 20, bottom: 20, left: 70},
				width = 940 - margin.left - margin.right,
				height = 640 - margin.top - margin.bottom,
				height2 = 640 - margin2.top - margin2.bottom;

			// scales your x-axis
			var x = d3.scale.linear()
				.range([0, width])
				.domain(d3.extent(dataLines[0], function(d) { return d[0] }));

			var x2 = d3.scale.linear()
				.range([0, width])
				.domain(d3.extent(dataLines[0], function(d) { return d[0] }));

			// iterates through dataLines lists to find min and max of all values for y-axis
			var yMINS = [];
			var yMAXS = [];

			for (var i=0; i < dataLines.length; i++) {
				yMINS[i] = d3.min(dataLines[i], function(d) { return d[1] });
				yMAXS[i] = d3.max(dataLines[i], function(d) { return d[1] });
			};
			

			var yExtent = []
			yExtent[0] = d3.min(yMINS) * 0.9;
			yExtent[1] = d3.max(yMAXS) * 1.1;


			var y = d3.scale.linear()
				.range([height, 0])
				.domain(yExtent);

			var y2 = d3.scale.linear()
				.range([100, 0])
				.domain(yExtent);

			// brushed on brush
			function brushed() {
  				x.domain(brush.empty() ? x2.domain() : brush.extent());
  				focus.selectAll(".line").attr("d", line);
  				focus.select(".x.axis").call(xAxis);
  				focus.selectAll(".dot")
  					.attr("cx", function(d) {return x(d[0]);})
      				.attr("cy", function(d) {return y(d[1]);});
			}

			//brush
			var brush = d3.svg.brush()
    			.x(x2)
    			.on("brush", brushed);

    		// Color chart
			var colorChart = [
				"red",
				"orange",
				"yellow",
				"green",
				"blue",
				"purple"
			];

			var dotColorList = [];

			/////////////////////////////////////////////////////////////

			// creates an svg
			svg = d3.select('#rwagraphdiv')
				.append("svg:svg")
					.attr('width', width + margin.left + margin.right)
					.attr('height', height + margin.top + margin.bottom + 100)
					.attr("id", "rwagraphdiv")
					.attr("xmlns", "http://www.w3.org/2000/svg");
				
			var focus = svg.append("g")
					.attr("class", "focus")
					.attr("id", "rwagraphdiv")
					.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

			// adds a rectangle to our svg
			focus.append("svg:rect")
				.attr("width", width)
				.attr("height", height)
				.attr("class", "plot")
				.attr("fill", "gray")
				.attr("opacity", .1);

			// creates a variable x axis
			var xAxis = d3.svg.axis()
				.scale(x)
				.orient("bottom")
				.ticks(5);

			// adds our xAxis to our svg g (group of elements)
			focus.append("svg:g")
				.attr("class", "x axis")
				.attr("transform", "translate(0, " + height + ")")
				.call(xAxis);

			// does the same thing with y axis
			var yAxis = d3.svg.axis()
				.scale(y)
				.orient("left")
				.ticks(10);

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

      		// creates a variable clip which holds the clipPath
      		var clip = focus.append("svg:clipPath")
				.attr("id", "clip")
				.append("svg:rect")
				.attr("x", 0)
				.attr("y", 0)
				.attr("width", width)
				.attr("height", height);

			// we create a variable called ChartBody
			var chartBody = focus.append("g")
				.attr("class", "chartBody")
				.attr("clip-path", "url(#clip)")
				.on("mousemove", function() { 
					var infobox = d3.select(".infobox");
					var coord = [0, 0];
					coord = d3.mouse(this)
						infobox.style("left", coord[0]  + 15 + "px");
						infobox.style("top", coord[1] + "px");
					});

			// creates scatterplot overlay for line graph and adds browser automatic tooltip for begining of each window
			for (var i=0; i < dataLines.length; i++) {
				focus.append("g").attr("class", "dotgroup").selectAll(".dot") 
      				.data(dataLines[i])
    		    	.enter()
    		    	.append("circle")
      				.attr("class", "dot")
      				.attr("r", 3)
      				.attr("cx", function(d) {return x(d[0]);})
      				.attr("cy", function(d) {return y(d[1]);})
      				.style("fill", colorChart[i])
      				.on("mouseover", function(d) {
						d3.select(this)
							.style("stroke", "black")
							.style("stroke-width", 5)
							.attr("r", 5);
						d3.select(".infobox")
							.style("display", "block");
						d3.select("p")
							.text(function() {
								return "(" + d[0] + ", " + d[1] + ")";
							});
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
							.attr("r", 3);
						d3.select(".infobox")
							.style("display", "none");
							})
      				.attr("clip-path", "url(#clip)");
      		};

			// specifies the path data
			var line = d3.svg.line()
				.x(function(d) { return x(d[0]); })
				.y(function(d) { return y(d[1]); });

			//create legend
			var rwlegend = svg.selectAll(".rwlegend")
      			.data(dataLines)
    			.enter()
    			.append("g")
      			.attr("class", "rwlegend")
      			.attr("transform", "translate(120,20)");


      		var i = 0;

      		//append legend rectangles
  			rwlegend.append("g:rect")
      				.attr("x", function(d, i) { return i * 145;})
      				.attr("width", 18)
      				.attr("height", 15)
      				.style("fill", function() { i++; return colorChart[i-1];});

      		var j = 0; 

  			// draw legend text
  			rwlegend.append("g:text")
      				.attr("x", function(d, i) { return i * 145 -5;})
      				.attr("y", 9)
      				.attr("dy", ".35em")
      				.style("text-anchor", "end")
      				.text(function() {j++; return legendLabels[j-1]});


      		// adds a path to our ChartBody 
			for (var i=0; i < dataLines.length; i++) {
				chartBody.append("svg:path")
					.datum(dataLines[i])
					.attr("class", "line")
					.attr("d", line)
					.attr("stroke", colorChart[i])
					.attr("fill", "none");
			};

			////////////////////////////////////////////////////////////

			var context = svg.append("g")
					.attr("id", "rwagraphdiv")
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
      		

			for (var i=0; i < dataLines.length; i++) {
				chartBody2.append("svg:path")
					.datum(dataLines[i])
					.attr("class", "line")
					.attr("d", line2)
					.attr("stroke", colorChart[i])
					.attr("fill", "none");
			};	


			//////////////////////////////////////////////////////////
			
			//download svg
 			d3.select("#svg-Chrome").on("click", (function (){ 
    			var e = document.createElement('script'); 
    			if (window.location.protocol === 'https:') { 
        			e.setAttribute('src', 'https://raw.github.com/NYTimes/svg-crowbar/gh-pages/svg-crowbar.js'); 
    			} else { 
        			e.setAttribute('src', 'http://nytimes.github.com/svg-crowbar/svg-crowbar.js'); 
    			} 
    			e.setAttribute('class', 'svg-crowbar'); 
    			document.body.appendChild(e); 
			}));


			d3.select("#svg-Other").on("click", function() {

				d3.select(this).attr("href", "data:image/svg+xml;charset=utf-8;base64," + btoa(unescape(encodeURIComponent(
					svg.attr("version", "1.1")
						.attr("xmlns", "http://www.w3.org/2000/svg")
					.node().parentNode.innerHTML))));

			});

		}
	}

	makeRWAGraph();
});