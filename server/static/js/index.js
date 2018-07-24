

wuxuanyi_sequence = {"ok": 1, "data": [["2018-07-24 20:02:42", 2157492, -1], ["2018-07-24 20:03:47", 2157732, 240], ["2018-07-24 20:04:51", 2158016, 284], ["2018-07-24 20:05:57", 2158244, 228], ["2018-07-24 20:07:00", 2158494, 250], ["2018-07-24 20:08:05", 2158722, 228], ["2018-07-24 20:09:11", 2158990, 268], ["2018-07-24 20:10:14", 2159230, 240], ["2018-07-24 20:11:21", 2159449, 219], ["2018-07-24 20:12:28", 2159708, 259], ["2018-07-24 20:13:32", 2159959, 251], ["2018-07-24 20:14:36", 2160205, 246], ["2018-07-24 20:15:44", 2160425, 220], ["2018-07-24 20:16:47", 2160710, 285], ["2018-07-24 20:17:55", 2160933, 223], ["2018-07-24 20:19:03", 2161243, 310], ["2018-07-24 20:20:06", 2161464, 221], ["2018-07-24 20:21:09", 2161690, 226], ["2018-07-24 20:22:13", 2161921, 231], ["2018-07-24 20:24:20", 2162479, 558], ["2018-07-24 20:25:30", 2162853, 374], ["2018-07-24 20:26:33", 2163113, 260], ["2018-07-24 20:27:38", 2163372, 259], ["2018-07-24 20:28:45", 2163699, 327], ["2018-07-24 20:29:56", 2163956, 257], ["2018-07-24 20:31:01", 2164291, 335], ["2018-07-24 20:32:05", 2164652, 361], ["2018-07-24 20:33:08", 2165021, 369], ["2018-07-24 20:34:13", 2165351, 330], ["2018-07-24 20:35:16", 2165778, 427], ["2018-07-24 20:36:19", 2166088, 310], ["2018-07-24 20:37:22", 2166470, 382], ["2018-07-24 20:38:27", 2166816, 346], ["2018-07-24 20:39:30", 2167198, 382], ["2018-07-24 20:40:34", 2167568, 370], ["2018-07-24 20:41:37", 2167909, 341], ["2018-07-24 20:42:41", 2168282, 373], ["2018-07-24 20:43:44", 2168659, 377], ["2018-07-24 20:44:48", 2169048, 389], ["2018-07-24 20:45:56", 2169364, 316], ["2018-07-24 20:47:01", 2169742, 378], ["2018-07-24 20:48:07", 2170132, 390], ["2018-07-24 20:49:12", 2170518, 386], ["2018-07-24 20:50:15", 2170889, 371], ["2018-07-24 20:51:19", 2171214, 325], ["2018-07-24 20:52:23", 2171570, 356], ["2018-07-24 20:53:26", 2171948, 378], ["2018-07-24 20:54:30", 2172297, 349]], "message": "ok"}

function request_last_minutes(minutes, singer)
{
    var ajax = null;
    if(window.XMLHttpRequest)
        ajax = new XMLHttpRequest()
    else
        ajax = new ActiveXObject("Microsoft.XMLHTTP");

    url = '/last_minutes'
    url = url + '?' + 'singer=' + singer + '&minutes=' + minutes
    ajax.open('GET', url)
    ajax.send()

    ajax.onreadystatechange = function(){
        if(ajax.readyState == 4 && ajax.status == 200){
            response_json = JSON.parse(ajax.responseText)
            if(response_json["ok"] > 0 && response_json.data.length > 0)
            {
                console.log('request success')
                render_vote_data(response_json.data)
            }
        }
    }
}

function render_vote_data(list_data)
{
    container = document.getElementById("vote-container")
    for(var i=0; i<list_data.length; i++)
    {
        item_p = document.createElement("p")
        list_item = list_data[i]
        item_p.innerText = list_item[0] + " " + list_item[1] + " " + list_item[2]
        container.appendChild(item_p)
    }
}

function build_inc_chart(data_list)
{
    var svg = d3.select("#inc-chart"),
        margin = {top:20, right:80, bottom:30, left:50},
        width = svg.attr("width") - margin.left - margin.right,
        height = svg.attr("height") - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")")

    var x = d3.scaleTime().range([0, width]),
        y = d3.scaleLinear().range([height, 0]),
        z = d3.scaleOrdinal(d3.schemeCategory10);

    var line = d3.line()
        .curve(d3.curveBasis)
        .x(function(d){ return x(parseTime(d[0])); })
        .y(function(d){ return y(d[2]); });

    var parseTime = d3.timeParse("%Y-%m-%d %H:%M:%S")
    x.domain(d3.extent(data_list, function(d) { return d[0]; }));   // d3.extent: return the min/max using natural order
    console.log(d3.extent(data_list, function(d) { return d[0]; }))
    y.domain([
        d3.min(data_list, function(item) { return item[2]; }),  // min increment
        d3.max(data_list, function(item) { return item[2]; })
    ])
    console.log(d3.min(data_list, function(item) { return item[2]; }))
    console.log(d3.max(data_list, function(item) { return item[2]; }))


    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));
    g.append("g")
        .attr("class", "axis axis--y")
        .call(d3.axisLeft(y))
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", "0.71em")
        .attr("fill", "#000")
        .text("涨幅/min")

    g.append("path")
        .attr("class", "line")
        .attr("d", line(data_list))
        .attr('stroke', z(0))

}

window.onload = function()
{
    console.log('onload')
    request_last_minutes(60, '吴宣仪');
    build_inc_chart(wuxuanyi_sequence["data"].slice(1));
}