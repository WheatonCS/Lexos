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
});


// BUBBLEVIZ - by Scott Kleinman
// BubbleViz is based on http://www.infocaptor.com/bubble-my-page.
$(function() {

    // Get user config variables
	minlength = $("#minlength").val();
	graphsize = $("#graphsize").val();
	
	// Loop through the token list, already filtered, to create a JavaScript array
	var tokens = [];

	$.each($(".words"), function(index, value) {
		// alert($(value).val());
		tokens.push($(value).val());
	});

	// Layout options
	var diameter = graphsize,
	    limit=5000,
	    format = d3.format(",d"),
	    color = d3.scale.category20c();

	var bubble = d3.layout.pack()
	    .sort(null)
	    .size([diameter, diameter])
	    .padding(1.5);

	// Add the image
	var svg = d3.select("#svgid").append("svg")
	    .attr("width", diameter)
	    .attr("height", diameter)
	    .attr("class", "bubble");

	var wordList=[];
	var wordCount=[];
	var wordMap={};
	var wordIdList=[];
	var wordTitleMap=[];
	var wordId=0;
	var wordStr="";
	var titleID=0;

	// Count the number of words
	var totalWords=tokens.length;

	// Loop through the list of words
	for (var i=0;i<tokens.length; i++) {
	  // Assign the current word to wordStr
	  wordStr=tokens[i];
	  try {
	  {
	    //If the wordStr is defined and >= the minimum word length
		if (typeof(wordStr)!="undefined" && wordStr.length>=minlength) {
	   
	        // If the wordStr is not defined in the wordMap object
			if (typeof(wordMap[wordStr])=="undefined"  ) {
	          // Add it
			  wordList.push(wordStr);
	          // Make the wordCount 1
			  wordCount.push(1);
	          // Adde the current wordID for the current wordStr in wordMap
			  wordMap[wordStr]=wordId;
	          // Add the current wordID to wordIdList 
			  wordIdList.push(wordId);
	          // Increment the current wordID
			  wordId++;
			}
	        // Otherwise, increment the wordCount for the current wordStr in the wordMAP
			else {
			  wordCount[wordMap[wordStr]]++;
			}
		}	
	  }
	  }
	  catch (err) {
	  
	  }
	}

	// Sort the wordId list
	wordIdList.sort(function(x, y) { 
			return -wordCount[x] + wordCount[y] 
		}
	);

	var data=[wordList,wordCount];

	var dobj=[];

	for (var di=0;di<data[0].length;di++) {
	  dobj.push({"key":di,"value":data[1][di]});
	}
	display_pack({children: dobj});

	function display_pack(root) {
	  var node = svg.selectAll(".node")
	      .data(bubble.nodes(root)
	      .filter(function(d) { return !d.children; }))
	    .enter().append("g")
	      .attr("class", "node")
	      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
		  .style("fill", function(d) { return color(data[0][d.key]); })
		  	.on("mouseover", function(d,i) {
			d3.select(this).style("fill", "gold"); 
			showToolTip(" "+data[0][i]+"<br />"+data[1][i]+" ",d.x+d3.mouse(this)[0]+50,d.y+d3.mouse(this)[1],true);
		})
		.on("mousemove", function(d,i) {

			// The line below attempts to adjust for centred graph; works best at 800px 
			// Original Line: tooltipDivID.css({top:d.y+d3.mouse(this)[1],left:d.x+d3.mouse(this)[0]+50});
			tooltipDivID.css({top:d.y+d3.mouse(this)[1]+272,left:d.x+d3.mouse(this)[0]+330});
		})	
	    .on("mouseout", function() {
			d3.select(this).style("fill", function(d) { return color(data[0][d.key]); });
			showToolTip(" ",0,0,false);
		});

	  node.append("circle")
	      .attr("r", function(d) { return d.r; });
	      //.style("fill", function(d) { return color(data[0][d.key]); });

	  node.append("text")
	      .attr("dy", ".3em")
	      .style("text-anchor", "middle")
		  .style("fill","black")
	      .text(function(d) { return data[0][d.key].substring(0, d.r / 3); });
	}
	   
	// Tooltip Functions

	function showToolTip(pMessage,pX,pY,pShow) {
	    if (typeof(tooltipDivID)=="undefined") {
	        tooltipDivID =$('<div id="messageToolTipDiv" style="position:absolute;display:block;z-index:10000;border:2px solid black;background-color:rgba(0,0,0,0.8);margin:auto;padding:3px 5px 3px 5px;color:white;font-size:12px;font-family:arial;border-radius: 5px;vertical-align: middle;text-align: center;min-width:50px;overflow:auto;box-shadow: 0 0 7px black;"></div>');
	//      tooltipDivID =$('<div id="messageToolTipDiv" style="position:absolute;display:block;z-index:10000;padding:5px 10px;color: white;border-radius: 10px;font-size: 12px;box-shadow: 0 0 7px black;vertical-align: middle;text-align: center;min-width:50px;overflow:auto;background: black;border: 1px solid white;"></div>');

		$('body').append(tooltipDivID);
	}

	if (!pShow) { tooltipDivID.hide(); return;}
	    //MT.tooltipDivID.empty().append(pMessage);
	    tooltipDivID.html(pMessage);
	    tooltipDivID.css({top:pY,left:pX});
	    tooltipDivID.show();
	}

	d3.select(self.frameElement).style("height", diameter + "px");
});