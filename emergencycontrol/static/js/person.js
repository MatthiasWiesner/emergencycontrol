$(".person_phone").on('dblclick', function(e){
    var _this = $(this);
    var current = _this.text();
    var person_id = _this.attr("data-person-id");
    _this.empty();

    var update = $('<input type="text">');
    if (current.length > 0){
        update.val(current);
    }
    update.focusout(function(){
        $.post("/person/set", {
            person_id : person_id,
            phone : $(this).val()
        });
        _this.empty();
        _this.text($(this).val());
    });
    _this.append(update);
    update.focus();
});

$(".person_picture").on('dblclick', function(e){
    var _this = $(this);
    var current = $('img', _this).attr('src');

    var person_id = _this.attr("data-person-id");
    _this.empty();

    var update = $('<input type="text">');
    if (current.length > 0){
        update.val(current);
    }
    update.focusout(function(){
        $.post("/person/set", {
            person_id : person_id,
            picture : $(this).val()
        });
        _this.empty();
        _this.append($('<image class="person" src="' + $(this).val() + '">'))
    });
    _this.append(update);
    update.focus();
});

$(".person_is_hero").on('click', function(e){
    var person_id = $(this).attr("data-person-id");
    $.post("/person/set", {
        person_id : person_id,
        is_hero : $(this).prop('checked')
    });
});
