$(document).ready( function(){
	var clusterMenu = document.getElementsByClassName("sublist")[3];
	var clusterMenuLi = clusterMenu.getElementsByTagName("li")[1];
	var clusterMenuLiA = clusterMenuLi.getElementsByTagName("a")[0];
	clusterMenuLiA.setAttribute("class", "selected");

	var analyzeMenu = document.getElementsByClassName("headernavitem")[3];
	analyzeMenu.setAttribute("class", "headernavitem selected");
});

window.onload= function(){

	var inconsistentrange= "0 ≤ t ≤ "
	var maxclustRange= "2 ≤ t ≤ "
	var range= " ≤ t ≤ "

	var inconsistentMaxStr= inconsistentMax.toString(); 
	var maxclustMaxStr= maxclustMax.toString();
	var distanceMaxStr= distanceMax.toString();
	var monocritMaxStr= monocritMax.toString();

	var distanceMinStr= distanceMin.toString();
	var monocritMinStr= monocritMin.toString();

	var inconsistentOp= inconsistentrange.concat(inconsistentMaxStr);
	var maxclustOp= maxclustRange.concat(maxclustMaxStr);
	var distanceOp= distanceMinStr.concat(range,distanceMaxStr);
	var monocritOp= monocritMinStr.concat(range,monocritMaxStr);

	var placeholderText = {"Inconsistent":inconsistentOp, "Maxclust": maxclustOp, "Distance": distanceOp, "Monocrit":monocritOp};

	$("#criterion").on("change",function() {
    	var selection = document.getElementById("criterion");
    	var inputBox = document.getElementById("threshold");
    
    	var selectedVal = $('#criterion').find(':selected').text();
    	if (placeholderText[selectedVal] !== undefined) {
        	inputBox.placeholder = placeholderText[selectedVal];
    	}
	});
	
	$("#criterion").on("click",function() {
    	var selection = document.getElementById("criterion");
    	var inputBox = document.getElementById("threshold");
    
    	var selectedVal = $('#criterion').find(':selected').text();
    	if (placeholderText[selectedVal] !== undefined) {
        	inputBox.placeholder = placeholderText[selectedVal];
    	}
	});

};

$(function() {
	$('#getdendro').click( function() {
		var activeFiles = $('#num_active_files').val();
		if (activeFiles < 2) {
			$("#densubmiterrormessage1").show().fadeOut(2500, "swing");
			return false;
		}
		else {
			var pruning =  $('#pruning').val();
			if ((Math.abs(Math.round(pruning)) != pruning) || pruning == 1) {
				$('#densubmiterrormessage3').show().fadeOut(2500, "easeInOutCubic");
				return false;
			}
				
			var thresholdValue = $('#threshold').val();
			var cOption = $('#criterion').val();
			if (cOption == 'inconsistent') {
				if ((thresholdValue >= 0 && thresholdValue <= inconsistentMax)|| (thresholdValue == '')) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
			else if (cOption == 'maxclust') {
				if ((thresholdValue >= 2 && thresholdValue <= maxclustMax)|| (thresholdValue == '')) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
			else if (cOption == 'distance') {
				if ((thresholdValue >= distanceMin && thresholdValue <= distanceMax)|| (thresholdValue == '')) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
			else if (cOption == 'monocrit') {
				if ((thresholdValue >= monocritMin && thresholdValue <= monocritMax )|| (thresholdValue == '')) {
					return true;
				}
				else {
					$("#densubmiterrormessage2").show().fadeOut(2500, "swing");
					return false;
				}	
			}
		}	

	});

	$('#criterion option').each(function() {
		$("#tValue").show();
	});

	$('#threshold').each(function() {
		var default_value = this.value;
		$(this).focus(function(){
			if(this.value == default_value) {
				this.value = '';
			}
		});
	});

	var pdfPage = Number(document.getElementById("pdfPageNumber").innerHTML);
	var pdfHeight = pdfPage * 1491;

	document.getElementById("pdf").height = pdfHeight;
});