$(".draggable").draggable({
	helper : "clone",
	cursor: "move"
});

$(".droppable").droppable({
	activeClass : "ui-state-default",
	hoverClass : "ui-state-hover",
	accept : ".droppable",
	drop : function(event, ui) {
		var nameFrom = ui.draggable.text();
		var nameTo = $(this).text();
		
		$(this).text(nameFrom);
		ui.draggable.text(nameTo);
		
		$.post("./swap", {
			week_from_id : ui.draggable.attr("data-week-id"),
			week_to_id : $(this).attr("data-week-id")
		});
	}
});
