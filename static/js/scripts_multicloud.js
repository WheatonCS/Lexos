$(function() {
	// Multiselect Dropdown Functionality
	$("#segmentlist").multiselect({
		noneSelectedText: "Select Segments",
		selectedText: "# of # checked"		
	});


	$('.multicloud-upload').change(function(ev) {
		filename = ev.target.files[0].name;

		$(this).siblings('.bttnfilelabels').html(filename);
	});

});


$(window).on("load", function() {
//$(function() {

	// Decrease the first wordScale domain numbers to increase size contrast
	wordScale = d3.scale.linear().domain([1,5,50,500]).range([10,20,40,80]).clamp(true);
	wordColor = d3.scale.linear().domain([10,20,40,80]).range(["blue","green","orange","red"]);

	numSegments = dataset.length;

	$('<ul id="sortable">').appendTo('#multicloud-container');

	for (i = 0; i < numSegments; i++) {
		$('<li class="ui-state-default" id="cloud'+i+'">').appendTo('#sortable');
		//$('#exspecto-nubes').html('Loading '+i+ ' of '+numSegments+'...');
		
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
		wordCounts = constructWordCounts(children);

		function draw(words) {
			viz = d3.select("#svg" + i);
			
			viz.append("g")
				.attr("transform", "translate(150,190)")
			.selectAll("text")
				.data(words)
			.enter().append("text")
				.style("font-size", function(d) { return d.size + "px"; })
				.style("fill", function(d) { return wordColor(d.size); })
				.style("opacity", .75)
				.attr("text-anchor", "middle")
				.attr("transform", function(d) {
					return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
				})
				.text(function(d) { return decodeURIComponent(escape(d.text)); })
			.append("svg:title")
				.text(function(d){return wordCounts[d.text];});

			viz.append("text")
				.data(label)
				.style("font-size", 14)
				.style("font-weight", 900)
				.attr("x", 60) //100
				.attr("y", 20) //15
				.text(function(d) { return label; }) 
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
	$("#exspecto-nubes").fadeOut();

	function constructWordCounts(list) {
		wordCounts = {};

		for (var i = 0; i < list.length; i++) {
			word = list[i].text;
			count = list[i].size;

			wordCounts[word] = count;
		}

		return wordCounts;
	}
	
	$( "#sortable" ).sortable({ revert: 100 });
	$( "#sortable" ).disableSelection();
	$( "#sortable" ).sortable({ cursor: "pointer" });
	$( ".ui-state-default" ).hover(function() {
		$( ".ui-state-default" ).css("cursor", "pointer");
	});
});