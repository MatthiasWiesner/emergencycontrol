function allowDrop(ev)
{
    ev.preventDefault();
}

function drag(ev)
{
    ev.dataTransfer.setData("Text",ev.target.id);
}

function drop(ev)
{
    ev.preventDefault();
    var data=ev.dataTransfer.getData("Text");
    var initdiv = document.getElementById(data).parentNode;
    var exchange = ev.target;
    exchange.parentNode.appendChild(document.getElementById(data));
    initdiv.appendChild(exchange);

    $.post( "./swap", { week_from_id: exchange.id, week_to_id: data }); 
}
