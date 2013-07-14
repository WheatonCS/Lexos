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

	$(".rollinginput").keypress(function(evt) {
		var theEvent = evt || window.event;
		var key = theEvent.keyCode || theEvent.which;
		if (key != 8) {
			if ($(this).val().length > 0 && $("#inputletter").prop('checked')) {
				theEvent.returnValue = false;
				if(theEvent.preventDefault) theEvent.preventDefault();
			}
		}
	});
	$("#rollingwindowsize").keypress(function(evt) {
		var theEvent = evt || window.event;
		var key = theEvent.keyCode || theEvent.which;
		if (key != 8) {
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

			var xhr = new XMLHttpRequest();

			xhr.open("GET", document.URL+'_data', false);
			xhr.send();

			var dataArray = eval(xhr.response);

			var margin = {top: 20, right: 20, bottom: 30, left: 50},
				width = 940 - margin.left - margin.right,
				height = 500 - margin.top - margin.bottom;


			var x = d3.scale.linear()
					.range([0, width]);

			var y = d3.scale.linear()
					.range([height, 0]);

			var xAxis = d3.svg.axis()
					.scale(x)
					.orient("bottom");

			var yAxis = d3.svg.axis()
					.scale(y)
					.orient("left");

			var downx = Math.NaN;
			var downscalex;

			var line = d3.svg.line()
					.x(function(d) { return x(d[0]); })
					.y(function(d) { return y(d[1]); });
					// .on("mousedown", function(d) {
					// 	var p = d3.svg.mouse(svg[0][0]);
					// 	downx = x.invert(p[0]);
					// 	downscalex = x;
					// });

			var svg = d3.select("#rwagraphdiv").append("svg:svg")
					.attr("width", width + margin.left + margin.right)
					.attr("height", height + margin.top + margin.bottom)
				.append("g")
					.attr("transform", "translate(" + margin.left + "," + margin.top + ")");


			x.domain(d3.extent(dataArray, function(d) { return d[0] }));

			if ($("#yaxisstart").prop("checked")) {
				y.domain([0, d3.max(dataArray, function(d) { return d[1] })]);
			}
			else {
				y.domain(d3.extent(dataArray, function(d) { return d[1] }));
			}


			svg.append("g")
					.attr("class", "x axis")
					.attr("transform", "translate(0," + height + ")")
					.call(xAxis);

			svg.append("g")
					.attr("class", "y axis")
					.call(yAxis)

			svg.append("path")
					.datum(dataArray)
					.attr("class", "line")
					.attr("d", line);

			svg.append("rect")
					.attr("class", "pane")
					.attr("width", w)
					.attr("height", h)
					.call(d3.behavior.zoom().on("zoom", zoom));

		}
		else {
			alert($("#rwagraphdiv").text());
		}
	}

	makeRWAGraph();
});