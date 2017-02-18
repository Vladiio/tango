$(document).ready( function(){

    $('#add_like').click( function(event){

        var catid = $(this).attr('data-catid');
        $.get('/rango/add_like/', {category_id: catid}, function(data){

            $('#like_count').html(data);

        });
    });


    $('#query').keyup( function(){

        var query_str = $(this).val();
        $.get('/rango/suggestion/', {query: query_str}, function(data){

            $('#suggestion-list').html(data);

        });
    });

    $('.add-page').click( function(event){

        var catid = $(this).attr('data-catid');
        var title = $(this).attr('data-title');
        var url = $(this).attr('data-url');
        var me = $(this)

        $.get('/rango/add/', {category_id: catid, title: title, url: url}, function(data){

            me.hide();
            $('#pages').html(data);
        });
    });
});