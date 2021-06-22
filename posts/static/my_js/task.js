$(document).ready(function(){

    $('#createBut').click(function(){
        var serializer = $('#createTask').serialize();
        console.log(serializer)
        $.ajax({
            url: $('#createTask').data('url'),
            data: serializer,
            type: 'post',
            success: function(resp){
                $('#taskList').append(
                    '<div class="card"><div class="card-body">' + resp.mes.title + '</div></div><br>'
                )
            }
        })
        $('#createTask  ').trigger('reset');
    });
});