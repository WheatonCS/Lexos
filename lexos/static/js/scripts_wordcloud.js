$(document).ready(function () {
  // Add tooltip to the DOM
  var tooltip = d3.select('body').append('div')
    .attr('class', 'd3tooltip tooltip right')
    .style('opacity', 0)
  d3.select('.d3tooltip').attr('role', 'tooltip')

  // Spinner Functionality
  $('#minlength').spinner({
    step: 1,
    min: 0
  })
  $('#graphsize').spinner({
    step: 10,
    min: 100,
    max: 3000
  })

  // Toggle file selection when 'Toggle All' is clicked
  $('#allCheckBoxSelector').click(function () {
    if (this.checked) {
      $('.minifilepreview:not(:checked)').trigger('click')
    } else {
      $('.minifilepreview:checked').trigger('click')
    }
  })

  var prev = -1 // initialize variable
  $('#vizcreateoptions').selectable({
    filter: 'label',  // Makes the label tags the elts that are selectable
    selecting: function (e, ui) {
      var currnet = $(ui.selecting.tagName, e.target).index(ui.selecting)   // gets index of current taget label
      if (e.shiftKey && prev > -1) {      // if you were holding the shift key and there was a box previously clicked
        // take the slice of labels from index prev to index curr and give them the 'ui-selected' class
        $(ui.selecting.tagName, e.target).slice(Math.min(prev, currnet) + 1, Math.max(prev, currnet) + 1).addClass('ui-selected')
        prev = -1  // reset prev index
      } else {
        prev = currnet  // set prev to current if not shift click
      }
    },
    stop: function () {
      // when you stop selecting, all inputs with the class 'ui-selected' get clicked
      $('.ui-selected input').trigger('click')
    }
  })
})

/*
Copyright (c) 2013, Jason Davies.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

  * The name Jason Davies may not be used to endorse or promote products
    derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL JASON DAVIES BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

// Word Cloud - by Scott Kleinman
// Word Cloud is based on https://github.com/jasondavies/d3-cloud/blob/master/examples/simple.html.

function preprocess (dataset) { // Used to decode utf-8
  wordData = dataset['children']
  for (var i = 0; i < wordData.length; i++) {
    // wordData[i].name = decodeURIComponent(escape(wordData[i].name));
    wordData[i].name = wordData[i].name
  }
}

$(function () {
  if (!$.isEmptyObject(dataset)) {
    preprocess(dataset)

    var wordCounts = {}

    var fill = d3.scale.category20b()

    var w = 860,
      h = 500

    var words = {},
      max,
      scale = 1,
      complete = 0,
      keyword = '',
      tags,
      fontSize,
      maxLength = 30,
      statusText = d3.select('#status')

    function flatten (o, k) {
      if (typeof o === 'string') return o
      var text = []
      for (k in o) {
        var v = flatten(o[k], k)
        if (v) text.push(v)
      }
      return text.join(' ')
    }

    function parseJSON (jsonObject) {
      cloud = jsonObject['children']
      tags = {}
      var cases = {}
      for (var i = 0; i < cloud.length; i++) {
        word = cloud[i].name.substr(0, maxLength)
        cases[word] = word
        count = cloud[i].size
        tags[word] = count
      }

      wordCounts = tags
      tags = d3.entries(tags).sort(function (a, b) { return b.value - a.value })
      tags.forEach(function (d) { d.key = cases[d.key] })
      // The line above doesn't seem to do anything.
      // console.log(tags); //Tags are correct here
      generate()
    }

    function generate () {
      layout
        .font(d3.select('#font').property('value'))
        .spiral(d3.select('input[name=spiral]:checked').property('value'))
      fontSize = d3.scale[d3.select('input[name=scale]:checked').property('value')]().range([10, 100])
      if (tags.length) fontSize.domain([+tags[tags.length - 1].value || 1, +tags[0].value])
      complete = 0
      statusText.style('display', null)
      words = []
      layout.stop().words(tags.slice(0, max = Math.min(tags.length, +d3.select('#maxwords').property('value')))).start()
    }

    function progress (d) {
      statusText.text('Loading words ' + ++complete + '/' + max)
    }

    function draw (data, bounds) {
      // console.log(data); // At this stage the text is missing government.
      var tooltip = d3.select('body').select('div.d3tooltip')
      statusText.style('display', 'none')
      scale = bounds ? Math.min(
        w / Math.abs(bounds[1].x - w / 2),
        w / Math.abs(bounds[0].x - w / 2),
        h / Math.abs(bounds[1].y - h / 2),
        h / Math.abs(bounds[0].y - h / 2)) / 2 : 1
      words = data

      var text = vis.selectAll('text')
        .data(words, function (d) { return d.text.toLowerCase() })

      text.transition()
        .duration(1000)
        .attr('transform', function (d) { return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')' })
        .style('font-size', function (d) { return d.size + 'px' })
      text.enter().append('text')
        .attr('text-anchor', 'middle')
        .attr('transform', function (d) { return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')' })
        .attr('id', function (d) { return wordCounts[d.text] })
        .style('font-size', function (d) { return d.size + 'px' })
        .on('click', function (d) {
          load(d.name)
          tooltip.transition()
            .duration(200)
            .style('opacity', 0)
        })
        .style('opacity', 1e-6)
        .transition()
        .duration(1000)
        .style('opacity', 1)
      text.style('font-family', function (d) { return d.font })
        .style('fill', function (d) { return fill(d.text.toLowerCase()) })
        .text(function (d) { return d.text })
        .style('cursor', 'pointer')
        .on('mouseover', function () {
          tooltip.transition()
            .duration(200)
            .style('opacity', 1)
          tooltip.html('<div class="tooltip-arrow"></div><div class="tooltip-inner">' + (this.id) + '</div>')
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
        })

      var exitGroup = background.append('g')
        .attr('transform', vis.attr('transform'))
      var exitGroupNode = exitGroup.node()
      text.exit().each(function () {
        exitGroupNode.appendChild(this)
      })
      exitGroup.transition()
        .duration(1000)
        .style('opacity', 1e-6)
        .remove()
      vis.transition()
        .delay(1000)
        .duration(750)
        .attr('transform', 'translate(' + [w >> 1, h >> 1] + ')scale(' + scale + ')')
    }

    // Converts a given word cloud to image/png.
    function downloadPNG () {
      var canvas = document.createElement('canvas'),
        c = canvas.getContext('2d')
      canvas.width = w
      canvas.height = h
      c.translate(w >> 1, h >> 1)
      c.scale(scale, scale)
      words.forEach(function (word, i) {
        c.save()
        c.translate(word.x, word.y)
        c.rotate(word.rotate * Math.PI / 180)
        c.textAlign = 'center'
        c.fillStyle = fill(word.name.toLowerCase())
        c.font = word.size + 'px ' + word.font
        c.fillText(word.name, 0, 0)
        c.restore()
      })
      d3.select(this).attr('href', canvas.toDataURL('image/png'))
    }

    // Save to PNG
    $('#download-png').on('click', function () {
      var $container = $('#vis'),
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
      html.append("<h2 style='margin-left: 30px'>Instructions for Saving Image</h2>")
      html.append("<h3 style='font-size: 16px; margin-left: 30px'><strong>For Mozilla Firefox:</strong></h3><ol>")
      html.append("<h3 style='font-size: 14px; margin-left: 30px'><li>PNG: Right click on the image and choose \"Save Image As...\".</li>")
      html.append("<h3 style='font-size: 14px; margin-left: 30px'><li>PDF: Right click and view image, then select your browser's print operation and choose print to PDF.</li></ol>")
      html.append("<h3 style='font-size: 16px; margin-left: 30px'><strong>For Chrome:</strong></h3>")
      html.append("<h3 style='font-size: 14px; margin-left: 30px'><li>Right click on the image and choose to \"Open image in new tab\".</li>")
      html.append("<h3 style='font-size: 14px; margin-left: 30px'><li>PNG: Right click on the image and choose to \"Save image as...\".</li>")
      html.append("<h3 style='font-size: 14px; margin-left: 30px'><li>PDF: Select your browser's print operation and choose print to PDF.</li></ol>")
      html.append(img)

      $(w.document.body).html(html)
      // End Save
    })

    function downloadSVG () {
      d3.select(this).attr('href', 'data:image/svg+xml;charset=utf-8;base64,' + btoa(unescape(encodeURIComponent(
        svg.attr('version', '1.1')
          .attr('xmlns', 'http://www.w3.org/2000/svg')
          .node().parentNode.innerHTML))))
    }

    function hashchange () {
      var h = location.hash
      if (h && h.length > 1) {
        h = h.substr(1).split(/@|=/, 2).map(decodeURIComponent)
        if (h.length > 1 && h[1] !== keyword || h[0] !== dataset) load(h[1], h[0])
        if (h.length && h[0].length) return
      }
      load('cloud')
    }

    function load (d, f) {
      f = f || dataset
      dataset = f
      if (dataset) parseJSON(dataset)
    }

    function updateTabs () {
      tabs.classed('active', function () {
        return decodeURIComponent(d3.select(this).attr('href').substr(1)) === dataset && dataset !== ''
      })
      var custom = d3.selectAll('.active').empty()
      d3.select('#custom').classed('active', custom)
      d3.select('#custom-area').style('display', custom ? null : 'none')
    }

    var layout = d3.layout.cloud()
      .timeInterval(10)
      .size([w, h])
      .fontSize(function (d) { return fontSize(+d.value) })
      .text(function (d) { return d.key })
      .on('word', progress)
      .on('end', draw)

    var svg = d3.select('#vis').append('svg')
      .attr('width', w)
      .attr('height', h)
    svg.append('rect')
      .attr('width', '100%')
      .attr('height', '100%')
      .attr('fill', 'white')
    var background = svg.append('g'),
      vis = svg.append('g')
        .attr('transform', 'translate(' + [w >> 1, h >> 1] + ')')

    d3.select('#download-svg').on('click', downloadSVG)
    d3.select('#download-png').on('click', downloadPNG)

    var tabs = d3.select('#presets').selectAll('a')
      .data([
        { dataset: '', name: 'Custom', id: 'custom' }
      ])
      .enter().append('a')
      .classed('first', function (d, i) { return !i })
      .attr('id', function (d) { return d.id })
      .attr('href', function (d) { return '#' + encodeURIComponent(d.dataset) })
      .text(function (d) { return d.name })
      .on('click', function (d) {
        var f = decodeURIComponent(d3.select(this).attr('href').substr(1)),
          that = this
        if (f !== '') {
          load(keyword, dataset = f)
        }
        tabs.classed('active', function () { return this === that })
        d3.select('#custom-area').style('display', d.id ? null : 'none')
        d3.event.preventDefault()
      })
    d3.select(window).on('hashchange', hashchange)
    d3.select(window)
      .on('load', hashchange)
      .on('load.tab', updateTabs)

    var form = d3.select('#wordcloud')
      .on('submit', function () {
        load(d3.select('#keyword').property('value'),
          d3.select('#text').property('value'))
        d3.event.preventDefault()
      })
    form.selectAll('input[type=number]')
      .on('click.refresh', function () {
        if (this.value === this.defaultValue) return
        generate()
        body.select('.d3tooltip').remove()
        this.defaultValue = this.value
      })
    form.selectAll('input[type=radio], #font')
      .on('change', generate)

    d3.select('#random-palette').on('click', function () {
      paletteJSON('http://www.colourlovers.com/api/palettes/random', {}, function (d) {
        fill.range(d[0].colors)
        vis.selectAll('text')
          .style('fill', function (d) { return fill(d.name.toLowerCase()) })
      })
      d3.event.preventDefault()
    });

    (function () {
      var r = 40.5,
        px = 35,
        py = 20

      var angles = d3.select('#angles').append('svg')
        .attr('width', 2 * (r + px))
        .attr('height', r + 1.5 * py)
        .append('g')
        .attr('transform', 'translate(' + [r + px, r + py] + ')')

      angles.append('path')
        .style('fill', 'none')
        .attr('d', ['M', -r, 0, 'A', r, r, 0, 0, 1, r, 0].join(' '))

      angles.append('line')
        .attr('x1', -r - 7)
        .attr('x2', r + 7)

      angles.append('line')
        .attr('y2', -r - 7)

      angles.selectAll('text')
        .data([-90, 0, 90])
        .enter().append('text')
        .attr('dy', function (d, i) { return i === 1 ? null : '.3em' })
        .attr('text-anchor', function (d, i) { return ['end', 'middle', 'start'][i] })
        .attr('transform', function (d) {
          d += 90
          return 'rotate(' + d + ')translate(' + -(r + 10) + ')rotate(' + -d + ')translate(2)'
        })
        .text(function (d) { return d + '°' })

      var radians = Math.PI / 180,
        from,
        to,
        count,
        scale = d3.scale.linear(),
        arc = d3.svg.arc()
          .innerRadius(0)
          .outerRadius(r)

      d3.selectAll('#angle-count, #angle-from, #angle-to')
        .on('change', getAngles)
        .on('mouseup', getAngles)

      getAngles()

      function getAngles () {
        count = +d3.select('#angle-count').property('value')
        from = Math.max(-90, Math.min(90, +d3.select('#angle-from').property('value')))
        to = Math.max(-90, Math.min(90, +d3.select('#angle-to').property('value')))
        update()
      }

      function update () {
        scale.domain([0, count - 1]).range([from, to])
        var step = (to - from) / count

        var path = angles.selectAll('path.angle')
          .data([{ startAngle: from * radians, endAngle: to * radians }])
        path.enter().insert('path', 'circle')
          .attr('class', 'angle')
          .style('fill', '#fc0')
        path.attr('d', arc)

        var line = angles.selectAll('line.angle')
          .data(d3.range(count).map(scale))
        line.enter().append('line')
          .attr('class', 'angle')
        line.exit().remove()
        line.attr('transform', function (d) { return 'rotate(' + (90 + d) + ')' })
          .attr('x2', function (d, i) { return !i || i === count - 1 ? -r - 5 : -r })

        var drag = angles.selectAll('path.drag')
          .data([from, to])
        drag.enter().append('path')
          .attr('class', 'drag')
          .attr('d', 'M-9.5,0L-3,3.5L-3,-3.5Z')
          .call(d3.behavior.drag()
            .on('drag', function (d, i) {
              d = (i ? to : from) + 90
              var start = [-r * Math.cos(d * radians), -r * Math.sin(d * radians)],
                m = [d3.event.x, d3.event.y],
                delta = ~~(Math.atan2(cross(start, m), dot(start, m)) / radians)
              d = Math.max(-90, Math.min(90, d + delta - 90)) // remove this for 360Â°
              delta = to - from
              if (i) {
                to = d
                if (delta > 360) from += delta - 360
                else if (delta < 0) from = to
              } else {
                from = d
                if (delta > 360) to += 360 - delta
                else if (delta < 0) to = from
              }
              update()
            })
            .on('dragend', generate))
        drag.attr('transform', function (d) { return 'rotate(' + (d + 90) + ')translate(-' + r + ')' })
        layout.rotate(function () {
          return scale(~~(Math.random() * count))
        })
        d3.select('#angle-count').property('value', count)
        d3.select('#angle-from').property('value', from)
        d3.select('#angle-to').property('value', to)
      }

      function cross (a, b) { return a[0] * b[1] - a[1] * b[0] }
      function dot (a, b) { return a[0] * b[0] + a[1] * b[1] }
    })()
  }
})
