$(function () {

    $('.btn-correction').click(function (e) {

        e.preventDefault();

        var pdf_id = $('.select').data('pdf_id');
         var page_number = $('.select').data('page_number');

         var url = "/scan/correct/"+pdf_id+"/"+page_number;
        $.ajax({
            url: url,
            type:"POST",
            data:{
                'text':$('#textarea-text-page').val()
            },
            success: function(results){
                alert(results);
            }});
    });

});