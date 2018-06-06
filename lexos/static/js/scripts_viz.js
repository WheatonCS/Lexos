$(function () {
  function updateMaxWordsOpt() {
    if ($('#vizmaxwords').is(':checked')) {
      console.log('hi')
      $('#vizmaxwordsopt').show()
    } else {
      $('#vizmaxwordsopt').hide()
    }
  }
  updateMaxWordsOpt()
  $('#vizmaxwords').click(updateMaxWordsOpt)
})

function preprocess(dataset) { // Used to decode utf-8
  wordData = dataset['children']

  for (var i = 0; i < wordData.length; i++) {
    // wordData[i].name = decodeURIComponent(escape(wordData[i].name));
    wordData[i].name = wordData[i].name
  }
}

// Return a flattened hierarchy containing all leaf nodes under the root.
function classes(root) {
  var classes = []

  function recurse(name, node) {
    if (node.children) node.children.forEach(function (child) { recurse(node.name, child) })
    // Note: decodeURIComponent(escape(node.name)) decodes the utf-8 from python/jinja/etc.
    else classes.push({ packageName: name, className: node.name, value: node.size })
  }

  recurse(null, root)
  return { children: classes }
}

$(document).ready(function () {
  // Add tooltip to the DOM
  var tooltip = d3.select('body').append('div')
    .attr('class', 'd3tooltip tooltip right')
    .style('opacity', 0)
  d3.select('.d3tooltip').attr('role', 'tooltip')

  $('#allCheckBoxSelector').click(function () {
    if (this.checked) {
      $('.minifilepreview:not(:checked)').trigger('click')
    } else {
      $('.minifilepreview:checked').trigger('click')
    }
  })

  /*	var prev = -1; //initialize variable
    $("#vizcreateoptions").selectable({
      filter: "label",  //Makes the label tags the elts that are selectable
      selecting: function(e , ui){
        var currnet = $(ui.selecting.tagName, e.target).index(ui.selecting);   //gets index of current taget label
        if (e.shiftKey && prev > -1) {      //if you were holding the shift key and there was a box previously clicked
          //take the slice of labels from index prev to index curr and give them the 'ui-selected' class
          $(ui.selecting.tagName,e.target).slice(Math.min(prev,current)+1, Math.max(prev,current)+1).addClass('ui-selected');
          prev = -1;  //reset prev index
        }else{
          prev = currnet;  //set prev to current if not shift click
        }
      },
      stop: function() {
        //when you stop selecting, all inputs with the class 'ui-selected' get clicked
        $(".ui-selected input").trigger("click");
      }
    }); */
})

// BUBBLEVIZ - by Scott Kleinman
// BubbleViz is based on http://www.infocaptor.com/bubble-my-page.

$(window).on('load', function () {
  // $(function() {
  console.log($('#graphsize'))
  console.log(dataset)
  if (!$.isEmptyObject(dataset)) {
    preprocess(dataset)
    $('#status-prepare').css('visibility', 'hidden')
    $('#save').css('display', 'block')

    // Create the tooltip
    var tooltip = d3.select('body').select('div.d3tooltip')

    // Configure the graph
    var diameter = $('#graphsize').val(),
      format = d3.format(',d'),
      color = d3.scale.category20c()

    var bubble = d3.layout.pack()
      .sort(null)
      .size([diameter, diameter])
      .padding(4)

    // Append the SVG
    var svg = d3.select('#viz').append('svg')
      .attr('width', diameter)
      .attr('height', diameter)
      .attr('class', 'bubble')

    // Append the nodes
    var node = svg.selectAll('.node')
      .data(bubble.nodes(classes(dataset))
        .filter(function (d) { return !d.children }))
      .enter().append('g')
      .attr('class', 'node')
      .attr('transform', function (d) { return 'translate(' + (d.x) + ',' + (d.y) + ')' })

    // Append the bubbles
    node.append('circle')
      .attr('r', function (d) {
        var radius = d.r
        if (radius < 7) {
          radius += 7 - radius
        }
        return radius
      })

      .style('fill', function (d, i) { return color(d.className) }) // Use packageName for clustered data
      .on('mouseover', function (d) {
        d3.select(this.parentNode.childNodes[0]).style('fill', 'gold')
        tooltip.transition()
          .duration(200)
          .style('opacity', 1)
        tooltip.html('<div class="tooltip-arrow"></div><div class="tooltip-inner">' + (d.value) + '</div>')
      })
      .on('mousemove', function (d) {
        return tooltip
          .style('left', (d3.event.pageX + 5) + 'px')
          .style('top', (d3.event.pageY - 20) + 'px')
      })
      .on('mouseout', function (d) {
        tooltip.transition()
          .duration(200)
          .style('opacity', 0)
        d3.select(this).style('fill', function (d, i) { return color(d.className) })
      })

    // Append the labels
    node.append('text')
      .attr('dy', '.3em')
      .style('text-anchor', 'middle')
      .text(function (d) { return d.className.substring(0, d.r / 3) })
      .on('mouseover', function (d) {
        d3.select(this.parentNode.childNodes[0]).style('fill', 'gold')
        tooltip.transition()
          .duration(200)
          .style('opacity', 1)
        tooltip.html('<div class="tooltip-arrow"></div><div class="tooltip-inner">' + (d.value) + '</div>')
      })
      .on('mousemove', function (d) {
        return tooltip
          .style('left', (d3.event.pageX + 5) + 'px')
          .style('top', (d3.event.pageY - 20) + 'px')
      })
      .on('mouseout', function (d) {
        tooltip.transition()
          .duration(200)
          .style('opacity', 0)
        d3.select(this.parentNode.childNodes[0]).style('fill', function (d, i) { return color(d.className) })
      })

    // Set the graph height from the diameter
    d3.select(self.frameElement).style('height', diameter + 'px')
  }

  // Save to PNG
  $('#save').on('click', function () {
    var $container = $('#viz'),
      // Canvg requires trimmed content
      content = $container.html().trim(),
      canvas = document.getElementById('svg-canvas')

    // Draw svg on canvas
    canvg(canvas, content)

    // Change img from SVG representation
    var theImage = canvas.toDataURL('image/png')
    $('#svg-img').attr('src', theImage)

    // Open a new window with the image
    var w = window.open()
    var img = $('#svg-img').clone().css('display', 'block')
    var html = $('<div/>')
    html.append("<h3>Use your browser's Save as function to save the image</h3>")
    html.append(img)
    $(w.document.body).html(html)
    // End Save
  })
})
