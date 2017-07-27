$(function () {
	// Hide unnecessary divs for DTM
  var newLabelsLocation = $('#normalize-options').parent()
  var newNormalizeLocation = $('#temp-label-div').parent()
  var tempNormalize = $('#normalize-options').html()
  var tempLabels = $('#temp-label-div').html()
  $('#normalize-options').remove()
  $('#temp-label-div').remove()
  newLabels = $('<fieldset class="analyze-advanced-options" id="temp-label-div"></fieldset>').append(tempLabels)
  newNormalize = $('<fieldset class="analyze-advanced-options" id="normalize-options"></fieldset>').append(tempNormalize)
  newLabelsLocation.append(newLabels)
  newNormalizeLocation.append(newNormalize)

  $('#normalize-options').hide()
	/* $("#culling-options").hide(); */

//   $("#normalize-options").empty().html($("#temp-label-div").html());
//   $("#temp-label-div").empty().html(tempContent);
	// $("#temp-label-div").css("position","relative").css("left","-10px").css("top","0px");

	// Error handling before submit
  $('#getsims').click(function () {
    if ($('#num_active_files').val() < 2) {
      $('#error-message').text('You must have at least 2 active documents to proceed!')
      $('#error-message').show().fadeOut(3000)
      return false
    } else {
      $('#status-analyze').css({'visibility': 'visible', 'z-index': '400000'})
      return true
    }
  })

	// Display selected document name on screen
  function makeFilenameStr (fileID) {
    var selectedFilename = 'Selected Document: ' + documentLabels[fileID]
    $('#selectedDocument').text(selectedFilename)
  }

  if ($('input[type=radio]').is(':checked')) {
    makeFilenameStr($('input[type=radio]:checked').val())
  }

  function createList () {
    var columnValues = []
    var rows = (docsListScore.length - 1)
    for (i = 0; i < rows; i++) {
      j = i + 1
      columnValues[i] = [j.toString(), docsListName[i], docsListScore[i].toString()]
      valStr = '<tr><td>' + j.toString() + '</td><td>' + docsListName[i] + '</td><td>' + docsListScore[i].toString() + '</td></tr>'
      $('#simtable tbody').append(valStr)
    }
		// $("#status-analyze").css({"visibility":"hidden"});

	    $('#simtable').DataTable({
	        'paging': true,
	        'searching': true,
	        'ordering': true,
	        'info': true,
	        'language': {
          'lengthMenu': 'Display _MENU_ documents per page'
    		}
	    })
  }

  if (docsListScore != '') {
    createList()
  }
})

	// Code to try and make the tokenize box look pretty on simQ page.  Only works in firefox? Makes templabels disappear in chromium
	// var brow, usrAG = navigator.userAgent;		// Catch browser info
	// if (usrAG.indexOf("Firefox") > -1) {        // if 'firefox' in browser name then apply this style stuff
	// 	$("#temp-label-div").css("position","relative").css("top","-126px").css("left","-10px");
	// 	$("#analyze-advanced").css("max-height","150px").css("overflow","hidden");

	// 	$("input[name='tokenType']").click(function(){
	// 		if ($(this).val() == 'word'){
	// 			$("#temp-label-div").css("top","-126px");
	// 		} else {
	// 			$("#temp-label-div").css("top","-161px");
	// 		}
	// 	});
	// }

// Old createList function
/*	function createList() {

		mytable = $('<table></table>').attr({id: "basicTable"});

		// title row
		var titleRow = $('<tr></tr>').appendTo(mytable);
		$('<td></td>').text("Rank").appendTo(titleRow);
		$('<td></td>').text("Filename").appendTo(titleRow);
		$('<td></td>').text("Cosine Similarity").appendTo(titleRow);

		// rankings
		var rows = (docsListScore.length - 1);
		var cols = 3;
		var tr = [];
		for (var i = 0; i < rows; i++) {
			var row = $('<tr></tr>').appendTo(mytable);
			for (var j = 0; j < cols; j++) {

				if (j == 0) {
					$('<td></td>').text(i + 1).appendTo(row);
				} else if (j == 1) {
					$('<td></td>').text(docsListName[i]).appendTo(row);
				} else {
					$('<td></td>').text(docsListScore[i]).appendTo(row);
				}
			}//for
		}//for

		mytable.appendTo("#simstable");
	} */
// End old createList function
