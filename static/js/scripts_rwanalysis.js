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
			$("#rwasubmiterrormessage3").show().fadeOut(1200, "easeInOutCubic");
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
		var empty = $("input").filter(function() {
			return this.value == '' && (this.type == 'text' || this.type == 'number');
		});
		numEmpty = empty.length;
		if ($(".minifilepreview.enabled").length == 0) {
			$("#rwasubmiterrormessage2").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else if (numEmpty > 0 && !(numEmpty == 1 && empty[0].id == 'rollingsearchwordopt' && $("#rollingaverage").prop('checked')) ) {
			$("#rwasubmiterrormessage1").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
	});

	function makeRWAGraph() {
		if ($("#rwagraphdiv").text() == 'True') {
			$("#rwagraphdiv").removeClass('hidden');
			$("#rwagraphdiv").text('');

			// size of the graph variables
			var margin = {top: 20, right: 20, bottom: 30, left: 60},
				width = 940 - margin.left - margin.right,
				height = 500 - margin.top - margin.bottom


			// scales your x-axis. input domain is the range of possible input data values (here, d3.extent returns the largest and
			// smallest values found within dataArray)
			// and the range is the possible output values. basically this makes it so that no matter what size your graph, values
			// will be scaled according to the width we've defined above
			var x = d3.scale.linear()
				.range([0, width])
				.domain(d3.extent(dataArray, function(d) { return d[0] }));

			// essentially doing the same thing, but slightly lowering/increasing min/max values so that our y-axis is better centered
			var yExtent = d3.extent(dataArray, function(d) { return d[1] })
			yExtent[0] = yExtent[0] * 0.9;
			yExtent[1] = yExtent[1] * 1.1;

			var y = d3.scale.linear()
				.range([height, 0])
				.domain(yExtent);

			// allows user to perform zoom action. .x(x) sets the x scale to be the one you zoom, the extent sets the scale's allowed
			// range, and .on("zoom", redraw()) says that on the call zoom, the result of the function redraw() (selecting all the 
			// necessary elements of chart) will be passed to zoom/d3.behavior.zoom() (I think? not positive on this)
			var zoom = d3.behavior.zoom()
				.x(x)
				.scaleExtent([1, Number.POSITIVE_INFINITY])
				.on("zoom", redraw);

			// creates an svg, and sets it to the #rwagraphdiv from rwanalysis.html, basically assigning what goes into that div
			svg = d3.select('#rwagraphdiv')
			// our div is an svg, and we are creating an svg image in our svg variable (which is the div #rwagraphdiv) with this width/height
			.append("svg:svg")
				.attr('width', width + margin.left + margin.right)
				.attr('height', height + margin.top + margin.bottom)
			// g allows you to group together elements and perform actions that apply to all of them at once
			// here, we are grouping the svg as one element, so that our call to zoom will work on the entire graph/svg image as a whole
			.append("svg:g")
				.attr("transform", "translate(" + margin.left + "," + margin.top + ")")
				.call(zoom);

			// adds a rectangle to our svg, sets our assigned width and height and sets it's class to "plot"
			//plot doesn't come up here, but in css styling
			svg.append("svg:rect")
				.attr("width", width)
				.attr("height", height)
				.attr("class", "plot");

			// creates a variable x axis, assigns the scale to x and orients it to the bottom, with 5 tick marks
			var xAxis = d3.svg.axis()
				.scale(x)
				.orient("bottom")
				.ticks(5);

			// adds our xAxis to our svg g (group of elements) and uses transform to put it in the right spot(not sure why height?)
			svg.append("svg:g")
				.attr("class", "x axis")
				.attr("transform", "translate(0, " + height + ")")
				.call(xAxis);

			// x-axis label
			svg.append("text")
    			.attr("class", "x label")
    			.attr("class", "label")
    			.attr("text-anchor", "end")
    			.attr("x", width)
    			.attr("y", height - 6)
    			.text("first letter/word/line in window");

			// does the same thing with y axis
			var yAxis = d3.svg.axis()
				.scale(y)
				.orient("left")
				.ticks(10);
			// does the same thing with y axis
			svg.append("g")
				.attr("class", "y axis")
				.call(yAxis);
			
			// y axis label
			svg.append("text")
    			.attr("class", "y label")
    			.attr("class", "label")
    			.attr("text-anchor", "end")
    			.attr("y", 6)
    			.attr("dy", ".75em")
    			.attr("transform", "rotate(-90)")
    			.text("average/ratio");


      		// creates a variable clip which holds the clipPath. this is a set of restrictions for where our image is visible to the user
			// so here, we restrict the visibility of our svg image to a rectangle bound by the four attr coordinates listed below
			var clip = svg.append("svg:clipPath")
				.attr("id", "clip")
				.append("svg:rect")
				.attr("x", 0)
				.attr("y", 0)
				.attr("width", width)
				.attr("height", height);

			// we create a variable called ChartBody that holds everything in our svg g (so basically our whole graph) and gives it our
			// clipPath attribute 
			var chartBody = svg.append("g")
				.attr("clip-path", "url(#clip)");

			// specifies the path data using path data generator method, each x,y coordinate is from our dataArray/d, but processed 
			// through var x or var y to get the appropriately scaled value
			var line = d3.svg.line()
				.x(function(d) { return x(d[0]); })
				.y(function(d) { return y(d[1]); });

      		// adds a path to our ChartBody that takes the form of a line (attr "d" assigns the shape of the path) 
			// and gets it's data (datum) from the variable dataArray, which was passed in to this js from rwanalysis.html
			chartBody.append("svg:path")
				.datum(dataArray)
				.attr("class", "line")
				.attr("d", line);

			// creates scatterplot overlay for line graph and adds browser automatic tooltip for begining of each window
			var dots = svg.append("svg:g").attr("class", "dotgroup").selectAll(".dot") 
      			.data(dataArray)
    		    .enter()
    		    .append("circle")
      			.attr("class", "dot")
      			.attr("r", 1.5)
      			.attr("cx", function(d) {return x(d[0]);})
      			.attr("cy", function(d) {return y(d[1]);})
      			.attr("clip-path", "url(#clip)")
      			.append("svg:title")
      			.text(function(d) {
      				return "("+d[0]+", "+d[1]+")";
      			;});

			// redraw() function called earlier. 
			function redraw() {
				svg.select(".x.axis").call(xAxis);
				svg.select(".y.axis").call(yAxis);
				svg.select(".line")
					.attr("class", "line")
					.attr("d", line);
				svg.selectAll(".dot")
      				.attr("class", "dot")
      				.attr("r", 1.5)
      				.attr("cx", function(d) {return x(d[0]);})
      			 	.attr("cy", function(d) {return y(d[1]);});
      				}

      		

		}
	}

	makeRWAGraph();
});