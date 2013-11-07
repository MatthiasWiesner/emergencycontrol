$(".draggable").draggable({
	helper : "clone",
	cursor: "move",
	activeClass : "draggable-hover",
});

$(".droppable").droppable({
	hoverClass : "droppable-hover",
	accept : ".draggable",
	drop : function(event, ui) {	
		var nameFrom = ui.draggable.text();
		var nameTo = $(this).text();

		if (ui.draggable.attr("data-week-id") != undefined) {
			$(this).text(nameFrom);
			ui.draggable.text(nameTo);
			console.log("SWAP")
			$.post("./swap", {
				week_from_id : ui.draggable.attr("data-week-id"),
				week_to_id : $(this).attr("data-week-id")
			});

		} else if(ui.draggable.attr("data-person-id") != undefined) {
			$(this).text(nameFrom);
			$(this).removeClass("notassigned");
			
			console.log("SET")
			$.post("/set", {
				person_id : ui.draggable.attr("data-person-id"),
				week_id : $(this).attr("data-week-id")
			});
		} 
	}
});

$("#accordion").accordion({
    collapsible: true
});

$(".editor").editable({
    lineBreaks : false,
    callback: function(data){
        if(data.content){
            var text = data.content
            //text = text.replace(/<br \/>/g, '\n')
            //text = text.replace(/[^\S\n]/g, ' ')
            $.post('/savetext', {
                week_id: data.$el.attr("data-week-id"),
                text: text
            }).done(function(response){
                data.$el.html(response);
                $('pre code').each(function(i, e) {hljs.highlightBlock(e)});
            });
        }
    }
});

$(".editor").on('edit', function(event, $editor){
    $editor.val("..load content");
    $.get('/gettext', {
        week_id: $(this).attr("data-week-id")
    }).done(function(data){
        $editor.val(data);
    });
});

hljs.initHighlightingOnLoad();