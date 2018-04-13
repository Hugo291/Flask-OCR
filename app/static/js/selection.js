$(function () {

    var lest_boxs = null;

    $('.page-element-selection').click(function() {

        var folder = $(this).data('folder');
        var file = $(this).data('file');

        var src = $(this).find("img").attr('src');

        var canvas = document.getElementById("canvas-selection"),
        ctx = canvas.getContext("2d");

        var background = new Image();
        background.src = src;

        canvas.width = background.width;
        canvas.height = background.height;

        $('#textarea-text-page').height = background.height;
        $('.scroll-list-image').height = background.height;


        canvas.background= src;

        background.onload = function(){
            ctx.drawImage(background,0,0);
        };

        $.ajax({url: "/scan/page/"+folder+"/"+file, success: function(results){

            //boxs word
            var boxs = results.box;

            lest_boxs = boxs;

            for(let index in boxs){

                var box = boxs[index];

                //create all box
                ctx.rect(box.position_left,box.position_top,box.size_width,box.size_height);
                ctx.stroke();
                ctx.lineWidth=1;
                ctx.strokeStyle="#FF0000";


            }

            //text page
            var text = results.text;
            console.log('text',text);

            $('#textarea-text-page').val(text);

        }});

    });


});