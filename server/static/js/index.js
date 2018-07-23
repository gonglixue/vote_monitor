
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

window.onload = function()
{
    console.log('onload')
    request_last_minutes(60, '吴宣仪');
}