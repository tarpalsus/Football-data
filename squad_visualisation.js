
d3.json("file", function(data) {
        index = -1;
        update_data(true);
        function update_data(forward) {
        if (forward) {
            if (index == data.length - 1) {
                index = index
    
            } else {
                index = index + 1
            }
        } else {
            if (index == 0) {
                index = index
    
            } else {
                index = index - 1
            }
        }
    
        d3.select("svg").remove()
    
        var players = data[index].Players
        var svg = d3.select("body")
        .append('svg')
        .attr("width", 1000)
        .attr("height", 1000);
    
        var matchData = svg
        .append("text")
        .style("text-anchor", "middle")
        .attr("x",500)
        .attr("y",100)
        .text("Match against " + data[index].Rival + ', ' + data[index].date)
        .attr("font-family", "sans-serif")
        .attr("font-size", "20px");
    
        var pitch_image = svg
        .append("svg:image")
        .attr("xlink:href", "file"
        .attr("height", '1000')
        .attr('x',0)
        .attr('y',0)
    
        var imgContainers = svg.selectAll("body")
        .data(players)
        .enter()
        .append("image");
    
        var textContainers = svg.selectAll("body")
        .data(players)
        .enter()
        .append("text")
    
        var playersImgs = imgContainers
        .attr("xlink:href", "file")
        .attr("x", function(d){return 100 * d[1] -50 ;})
        .attr("y", function(d){return 70 * d[2]; })
        .attr("width",100)
        .attr("height",100)
    
        var playersNames = textContainers
        .style("text-anchor", "middle")
        .attr("x", function(d){return 100 * d[1]; })
        .attr("y", function(d){return 70 * d[2] + 120; })
        .text(function(d){return d[0]; })
        .attr("font-family", "sans-serif")
        .attr("font-size", "20px");
      
        var clickable = svg.append("text")
            .text('Next')
            .attr("x", 800)
            .attr("y", 100)
            .on('click', function() { update_data(true) })
            .attr("font-family", "sans-serif")
            .attr("font-size", "30px");
      
        var clickable = svg.append("text")
            .text('Previous')
            .attr("x", 100)
            .attr("y", 100)
            .on('click', function() { update_data(false) })
            .attr("font-family", "sans-serif")
            .attr("font-size", "30px");
      
    }
});
