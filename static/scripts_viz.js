$(function() {
	$(".navbaroption").click(function() {
		$(this).next("input").click();
	});
});


// BUBBLEVIZ - by Scott Kleinman
$(function() {

	// Loop through the token list, already filtered, to create a JavaScript array
	// The safe filter ensures that apostrophes do not appear as &#39;
	var tokens = [];

	$.each($(".words"), function(index, value) {
		// alert($(value).val());
		tokens.push($(value).val());
	});

	// Layout options
	var diameter = 800 + 140,
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

	// I'm confused by the comment on this line. What is this array for?
	var wordList=[]; //each word one entry and contains the total count [ {cnt:30,title_list:[3,5,9],
	var wordCount=[];
	var wordMap={};
	var wordIdList=[];
	var wordTitleMap=[];
	var minVal=10000;
	var maxVal=-230;
	var wordId=0;
	var wordStr="";
	var titleID=0;
	var minWordLength=0; // Change this value to skip words of x number of characters

	// Count the number of words
	var totalWords=tokens.length;

	// Loop through the list of words
	for (var i=0;i<tokens.length; i++) {
	  // Assign the current word to wordStr
	  wordStr=tokens[i];
	  try {
	  {
	    //If the wordStr is defined and >= the minimum word length
		if (typeof(wordStr)!="undefined" && wordStr.length>=minWordLength) {
	   
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

	// Statistics Box
	var wordPercentStr="";
	wordPercentStr+="<table class=\"stats\"><tr><td><b>Number of Tokens:</b> "+totalWords+"</th><td><b>Number of Types:</b> "+wordId+"</td></tr></table>";
	wordPercentStr+="<p class=\"stats\"><b>Gross Density</b> is the word type count divided by the total number of tokens in the text. <b>Good Density</b> is the word type count divided by the total number of words displayed in the visualisation, excluding stop words and words filtered by character count.</p>";
	wordPercentStr+="<table class=\"stats\"><tr><th>Word</th><th>Count</th><th>Good Density (%)</th><th>Gross Density (%)</th></tr>";
	var wi=0;
	var density;
	var grossDensity;
	for (var wp=0; wp<wordIdList.length;wp++) {
	  wi=wordIdList[wp];
	  density=" "+(wordCount[wi]*100/wordId);
	  density=density.substr(0,6);
	  grossDensity=(" "+(wordCount[wi]*100/totalWords)).substr(0,6);
	  wordPercentStr+="<tr>";
	  wordPercentStr+="<td>"+wordList[wi]+"</td><td>"+wordCount[wi]+"</td><td>"+density+"</td><td>"+grossDensity+"</td>";
	  wordPercentStr+="</tr>";
	}
	wordPercentStr+="</table>";
	$("#topwords").html(wordPercentStr);
	$("#countbox").text(wordId);


	minVal=10000;
	maxVal=-100;
	for (var wi=0; wi<wordList.length; wi++) {
		if (minVal>wordCount[wi] ) minVal=wordCount[wi];
		if (maxVal<wordCount[wi] ) maxVal=wordCount[wi];
		
	}
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
			tooltipDivID.css({top:d.y+d3.mouse(this)[1]+170,left:d.x+d3.mouse(this)[0]+330});
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