function initDragDrop(){
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
                $.post("/calendar/swap", {
                    week_from_id : ui.draggable.attr("data-week-id"),
                    week_to_id : $(this).attr("data-week-id")
                });

            } else if(ui.draggable.attr("data-person-id") != undefined) {
                $(this).text(nameFrom);
                $(this).removeClass("notassigned");

                console.log("SET")
                $.post("/calendar/set", {
                    person_id : ui.draggable.attr("data-person-id"),
                    week_id : $(this).attr("data-week-id")
                });
            }
        }
    });
}

function loadWeeks(type){
    $.get("/calendar/load", {type: type})
        .done(function(data){
            console.log(data);
            $('#calendar_weeks').empty();
            $.each(data, function(i, week_data){
                var w = $("<div class='span3 week'>");
                var h = $("<h4>");
                h.text("Week " + week_data.week_nr);
                w.append(h);
                if(week_data.person){
                    var p = $("<div class='draggable droppable' data-week-id='" + week_data.id + "'>");
                    p.text(week_data.person.name);
                } else {
                    var p = $("<div class='draggable droppable notassigned' data-week-id='" + week_data.id + "'>");
                    p.text("No person assigned");
                }
                w.append(p);
                $('#calendar_weeks').append(w);
            });
            initDragDrop();
        }
    );
}


function switchLoad(type){
    var load_switch = $('#calendar_load_switch');
    load_switch.unbind('click');
    if(type == 'previous'){
        load_switch.text("Load previous weeks");
        load_switch.click(function(){
            loadWeeks("previous");
            switchLoad("next");
        });
    } else if(type == 'next'){
        load_switch.text("Load next weeks");
        load_switch.click(function(){
            loadWeeks("next");
            switchLoad("previous");
        });
    }
}

loadWeeks("next");
switchLoad("previous");