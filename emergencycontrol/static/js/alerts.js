$(".mail").on('click', function(e){
    $(".payload", $(this)).toggle();
});

$("#accordion").accordion({
    collapsible: true,
    heightStyle: "content"
});
