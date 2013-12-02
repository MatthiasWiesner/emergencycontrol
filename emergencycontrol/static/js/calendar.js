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