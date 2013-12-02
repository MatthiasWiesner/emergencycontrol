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

$("#accordion").accordion({
    collapsible: true,
    heightStyle: "content"
});

hljs.initHighlightingOnLoad();