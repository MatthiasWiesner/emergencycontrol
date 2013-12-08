$(".person_phone").on('dblclick', function(e){
    var _this = $(this);
    var current = _this.text();
    var person_id = _this.attr("data-person-id");
    _this.empty();

    var update = $('<input type="text">');
    if (current.length > 0){
        update.val(current);
    }
    _this.append(update);

    update.change(function(){
        $.post("/person/set", {
            person_id : person_id,
            phone : $(this).val()
        });
        _this.empty();
        _this.text($(this).val());
    });
});

$(".person_picture").on('dblclick', function(e){
    var _this = $(this);
    var current = _this.text();
    var person_id = _this.attr("data-person-id");
    _this.empty();

    var update = $('<input type="text">');
    if (current.length > 0){
        update.val(current);
    }
    _this.append(update);

    update.change(function(){
        $.post("/person/set", {
            person_id : person_id,
            picture : $(this).val()
        });
        _this.empty();
        _this.append($('<image class="person" src="' + $(this).val() + '">'))
    });
});
