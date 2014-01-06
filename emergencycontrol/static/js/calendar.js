function loadLogs(){
    $.get("/calendar/logs")
        .done(function(data){
            $('#calendar_logs').empty();
            var loglist = $("<ul id='loglist'>");
            $.each(data, function(i, log){
                var l = $("<li class='logentry'>");
                l.text(log.text);
                loglist.append(l);
            });
            $('#calendar_logs').append(loglist);
        }
    );
}


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
                $.post("/calendar/swap", {
                    week_from_id : ui.draggable.attr("data-week-id"),
                    week_to_id : $(this).attr("data-week-id")
                }).done(function(){loadLogs();});

            } else if(ui.draggable.attr("data-person-id") != undefined) {
                $(this).text(nameFrom);
                $(this).removeClass("notassigned");

                $.post("/calendar/set", {
                    person_id : ui.draggable.attr("data-person-id"),
                    week_id : $(this).attr("data-week-id")
                }).done(function(){loadLogs();});
            }
        }
    });
}

function loadWeeks(init_date, fetch_type){
    $.get("/calendar/load", {init_date: init_date, fetch_type: fetch_type})
        .done(function(data){
            $('#calendar_weeks').empty();
            $.each(data.weeks, function(i, week_data){
                var w = $("<div class='span3 week'>");
                var head = $("<div class='week_head'>");

                var m = $("<span class='week_month'>");
                m.text(week_data.month);
                head.append(m);

                var h = $("<h4 class='week_head'>");
                h.text("Week " + week_data.week_nr);
                head.append(h);

                w.append(head);

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

            $('#calendar_previous').unbind('click');
            $('#calendar_previous').html("&#9650;");
            $('#calendar_next').html("&#9660;");
            if(data.weeks.length > 0){
                var previous_date=data.prev;
                var next_date=data.next;
                $('#calendar_next').unbind('click');
                $('#calendar_next').bind('click', function(e){
                    loadWeeks(next_date, 'next');
                });
                $('#calendar_previous').bind('click', function(e){
                    loadWeeks(previous_date, 'previous');
                });
            } else {
                $('#calendar_previous').text("");
            }
        }
    );
}

loadWeeks(init_date, 'next');
loadLogs();
