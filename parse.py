#!/usr/bin/env python3
from collections import OrderedDict
from datetime import date
from glob import glob
from lxml import html
import json
import sys

title = "Entwicklung ICU-Betten nach Bundesland"
result = OrderedDict()
result["Total"] = {}

for report_nr, filename in enumerate(sorted(glob('report_*.html'))):
    time = filename[7:17]
    tree = html.parse(filename)
    keys = tree.xpath('//table[@id="table"]/thead/tr/th/text()')[:-1]
    states = tree.xpath('//table[@id="table"]/tbody/tr')

    for state in states:
        name = state.xpath('th/text()')[0]
        values = [int(value) for value in state.xpath('td/text()')]
        if report_nr == 0:
            assert(name not in result)
        for key, value in zip(keys, values):
            result.setdefault(name, {}).setdefault(key, []).append({"date": time, "value": value})
            if key not in result["Total"]:
                result["Total"][key] = []
            for entry in result["Total"][key]:
                if entry["date"] == time:
                    entry["value"] += value
                    break
            else:
                result["Total"][key].append({"date": time, "value": value})

print("""<!DOCTYPE html>
<meta charset="utf-8">
<head>
  <script src="d3.js"></script>
  <title>{}</title>
  <!-- Enable responsiveness on mobile devices-->
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1, minimum-scale=1">""".format(title))
print("""  <style>
table {
  padding-right: 100px;
}

td {
  margin: 0;
  padding: 0;
  background: #fff;
  color: #000;
}

tbody td:first-child {
  position: -webkit-sticky;
  position: sticky;
  left: 0;
}

tbody td:first-child {
  left: 0;
  z-index: 1;
}

thead th {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  background: #fff;
  color: #000;
}

thead th:first-child {
  left: 0;
  z-index: 2;
}

.line {
  fill: none;
  stroke: steelblue;
  stroke-width: 2px;
}

.overlay {
  fill: none;
  pointer-events: all;
}

.focus circle {
  fill: steelblue;
}

div.tooltip {
    position: absolute;
    text-align: center;
    padding: 2px;
    background: lightsteelblue;
    border: 0px;
    border-radius: 8px;
    pointer-events: none;
    z-index: 3;
    width: max-content;
}
  </style>
</head>
<body>
<script>
var div = d3.select("body").append("div").attr("class", "tooltip").style("display", "none");
var margin = {top: 0, right: 40, bottom: 0, left: 0}
var width = 200 - margin.left - margin.right;
var height = 50 - margin.top - margin.bottom;

function drawGraph(name, data) {
    var svg = d3.select(name).append("svg").attr("width", width + margin.left + margin.right).attr("height", height + margin.top + margin.bottom).append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    data.forEach(function(d) {
        d.date = d3.timeParse("%Y-%m-%d")(d.date);
    });
    var x = d3.scaleTime().range([10, width - 10]);
    var y = d3.scaleLinear().range([height - 10, 10]);
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) { return d.value; })]);
    var valueline = d3.line().x(function(d) { return x(d.date); }).y(function(d) { return y(d.value); });
    svg.append("path").data([data]).attr("class", "line").attr("d", valueline);
    var maxValue = d3.max(data, function(d) { return d.value; });
    svg.append("g").attr("class", "y axis").attr("transform", "translate(" + width + ",0)").call(d3.axisRight(y).ticks(2).tickValues(d3.range(0, maxValue + 0.1, maxValue)).tickFormat(function(d) { return d == 0 ? "" : d3.format('d')(d) }));
    var focus = svg.append("g").attr("class", "focus").style("display", "none");
    focus.append("circle").attr("r", 5);
    svg.append("rect").attr("class", "overlay").attr("width", width).attr("height", height).on("mouseover", function() { d3.select(this.parentNode).select(".focus").style("display", null); div.style("display", null); }).on("mouseout", function() { d3.select(this.parentNode).select(".focus").style("display", "none"); div.style("display", "none"); }).on("mousemove", function() {
      var focus = d3.select(this.parentNode).select(".focus")
      var x0 = x.invert(d3.mouse(this)[0]),
        i = d3.bisector(function(d) { return d.date; }).left(data, x0, 1),
        d0 = data[i - 1],
        d1 = data[i],
        d = x0 - d0.date > d1.date - x0 ? d1 : d0;
      div.html(d3.timeFormat("%Y-%m-%d")(d.date) + "<br/><b>" + d.value + "</b>").style("left", (d3.event.pageX) + "px").style("top", (d3.event.pageY - 28) + "px");
      focus.attr("transform", "translate(" + x(d.date) + "," + y(d.value) + ")");
    });
}
</script>""")
print("""<h1>{0}</h1>
<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>""".format(title))

for key in keys:
    print('      <th>{}</th>'.format(bytes(key, 'latin1').decode('utf-8')))

print("""    </tr>
  </thead>
  <tbody>""")

i = 0
for key in result:
    print('    <tr>')
    print('      <td>{}</td>'.format(key))
    for keys in result[key]:
        print('      <td id="dv_{0}"></td><script>drawGraph("#dv_{0}", {1});</script>'.format(i, json.dumps(result[key][keys])))
        i += 1
    print("    </tr>")

print("""  </tbody>
</table>
<p><a href="https://github.com/def-/icu-beds">source code</a>, data source: <a href="https://www.divi.de/register/kartenansicht">DIVI Intensivregister</a>, last updated: {}</p>
</body>""".format(date.today().strftime("%Y-%m-%d")))
