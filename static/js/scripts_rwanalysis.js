$(function() {
	$(".minifilepreview").click(function() {
		$(this).siblings(".minifilepreview").removeClass('enabled');
		$(this).addClass('enabled');
		$("#filetorollinganalyze").val($(this).prop('id'));
	});

	$("#radioratio").click(function() {
		var timeToToggle = 150;
		$(".rollingsearchwordoptdiv").fadeIn(timeToToggle);
		$(".rollingsearchwordoptdiv").css('display', 'inline');
	});
	$("#radioaverage").click(function() {
		var timeToToggle = 150;
		$(".rollingsearchwordoptdiv").fadeOut(timeToToggle);
	});

	$("#radioinputletter").click(function() {
		var oldVal = $(".rollinginput").val();
		$(".rollinginput").val(oldVal.slice(0,1));
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
	});

	function makeRWAGraph() {
		if ($("#rwagraphdiv").text() == 'True') {
			$("#rwagraphdiv").removeClass('hidden');
			$("#rwagraphdiv").text('');

			// size of the graph variables
			var margin = {top: 20, right: 20, bottom: 180, left: 70},
				margin2 = {top: 520, right: 20, bottom: 20, left: 70},
				width = 940 - margin.left - margin.right,
				height = 640 - margin.top - margin.bottom,
				height2 = 640 - margin2.top - margin2.bottom;

			// scales your x-axis
			var x = d3.scale.linear()
				.range([0, width])
				.domain(d3.extent(dataArray, function(d) { return d[0] }));

			var x2 = d3.scale.linear()
				.range([0, width])
				.domain(d3.extent(dataArray, function(d) { return d[0] }));

			// essentially doing the same thing
			var yExtent = d3.extent(dataArray, function(d) { return d[1] });
			yExtent[0] = yExtent[0] * 0.9;
			yExtent[1] = yExtent[1] * 1.1;

			var y2Extent = d3.extent(dataArray, function(d) { return d[1] });
			y2Extent[0] = y2Extent[0] * 0.9;
			y2Extent[1] = y2Extent[1] * 1.1;

			var y = d3.scale.linear()
				.range([height, 0])
				.domain(yExtent);

			var y2 = d3.scale.linear()
				.range([100, 0])
				.domain(y2Extent);

			// brushed on brush
			function brushed() {
  				x.domain(brush.empty() ? x2.domain() : brush.extent());
  				focus.select(".line").attr("d", line);
  				focus.select(".x.axis").call(xAxis);
  				focus.selectAll(".dot")
  					.attr("cx", function(d) {return x(d[0]);})
      				.attr("cy", function(d) {return y(d[1]);});
  				};

			//brush
			var brush = d3.svg.brush()
    			.x(x2)
    			.on("brush", brushed);

    		// redraw on zoom
			function redraw() {
				focus.select(".x.axis").call(xAxis);
				focus.select(".y.axis").call(yAxis);
				focus.select(".line")
					.attr("class", "line")
					.attr("d", line);
				focus.selectAll(".dot")
      				.attr("class", "dot")
      				.attr("r", 1.5)
      				.attr("cx", function(d) {return x(d[0]);})
      			 	.attr("cy", function(d) {return y(d[1]);});
      			};

    		//zoom
    		var zoom = d3.behavior.zoom()
				.x(x)
				.scaleExtent([1, Number.POSITIVE_INFINITY])
				.on("zoom", redraw);

			/////////////////////////////////////////////////////////////

			// creates an svg
			svg = d3.select('#rwagraphdiv')
				.append("svg:svg")
					.attr('width', width + margin.left + margin.right)
					.attr('height', height + margin.top + margin.bottom + 30)
				
			var focus = svg.append("g")
					.attr("class", "focus")
					.attr("transform", "translate(" + margin.left + "," + margin.top + ")")
					.call(zoom);

			// adds a rectangle to our svg
			focus.append("svg:rect")
				.attr("width", width)
				.attr("height", height)
				.attr("class", "plot");

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
						infobox.style("left", coord[0] + 15 + "px");
						infobox.style("top", coord[1] + "px");
					});

			// creates scatterplot overlay for line graph and adds browser automatic tooltip for begining of each window
			var dots = focus.append("g").attr("class", "dotgroup").selectAll(".dot") 
      			.data(dataArray)
    		    .enter()
    		    .append("circle")
      			.attr("class", "dot")
      			.attr("r", 1.5)
      			.attr("cx", function(d) {return x(d[0]);})
      			.attr("cy", function(d) {return y(d[1]);})
      			.on("mouseover", function(d) {
					d3.select(this)
						.style("fill", "#0068af")
						.attr("r", 3);
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
						infobox.style("top", coord[1] + 300 + "px");
					})
      			.on("mouseout", function() {
					d3.select(this)
						.style("fill", "gray")
						.attr("r", 1.5);
					d3.select(".infobox")
						.style("display", "none");
						})
      			.attr("clip-path", "url(#clip)");

			// specifies the path data
			var line = d3.svg.line()
				.x(function(d) { return x(d[0]); })
				.y(function(d) { return y(d[1]); });

      		// adds a path to our ChartBody 
      		chartBody.append("svg:path")
				.datum(dataArray)
				.attr("class", "line")
				.attr("d", line);

			////////////////////////////////////////////////////////////

			var context = svg.append("g")
					.attr("class", "context")
					.attr("width", width)
					.attr("height", 100)
					.attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");

			context.append("rect")
				.attr("width", width)
				.attr("height", 100)
				.attr("class", "plot");

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
      		chartBody2.append("svg:path")
				.datum(dataArray)
				.attr("class", "line")
				.attr("d", line2);

			//////////////////////////////////////////////////////////
		}
	}

	makeRWAGraph();
});