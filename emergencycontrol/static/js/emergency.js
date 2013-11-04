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
ajaxCalls("GET","./testcall?emps="+exchange.id);
}

function ajaxCalls(method,url){
    xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState==4 && xmlhttp.status==200){
           alert("employee : "+xmlhttp.responseText); 
        }
    }
    xmlhttp.open(method,url,true);
    xmlhttp.send();
}
