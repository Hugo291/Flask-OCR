$(function () {

    $('.page-element-selection').click(function() {
        searchBox(this);
    });

    searchBox($('.page-element-selection:first'));

});

function startLoad(text) {
    $('#load-process').html(
        "<div class='row'>" +
            "<div class='loader mr-3 ml-3'></div>" +
            "<div>"+text+"</div>" +
        "</div>"
    );
}

function setBackgroundSelect(CurrentSelect) {
    $('.page-element-selection').removeClass("select");
    $(CurrentSelect).addClass('select');
}

function endLoad(text) {
    $('#load-process').html("" +
        "<div class='row '>" +
            "<div class='ml-3'>" +
                text+"" +
            "</div>" +
        "</div>")
}

function setInfoPage(ctx , pdf_id , page_number) {
     //get info of scan page box(word) and text
        $.ajax({url: "/scan/page/"+pdf_id+"/"+page_number, success: function(results){

            //boxs word
            var boxs = results.box;
            last_boxs = boxs;
            //create all box
            for(let index in boxs){
                let box = boxs[index];
                ctx.rect(box.position_left,box.position_top,box.size_width,box.size_height);
                ctx.stroke();
                ctx.lineWidth=1;
                ctx.strokeStyle="#FF0000";
            }

            setTextAreaText(results.text);

            endLoad('The page is loaded');
        }});
}

function setTextAreaText(text) {
    $('#textarea-text-page').val(text);
}

function canvasBox(currentSelect) {
    var src = $(currentSelect).find("img").attr('src');

    //canvas
    var canvas = document.getElementById("canvas-selection"),
    ctx = canvas.getContext("2d");

    //image background convas
    var background = new Image();
    background.src = src;

    //set canvas size
    canvas.width = background.width;
    canvas.height = background.height;

    //set size of
    $('#textarea-text-page').height = background.height;
    $('.scroll-list-image').height = background.height;

    canvas.background= src;

    background.onload = function(){
        ctx.drawImage(background,0,0);
    };

    return ctx;
}

function searchBox(currentSelect) {

    setBackgroundSelect(currentSelect);

    var pdf_id = $(currentSelect).data('pdf_id');
    var page_number = $(currentSelect).data('page_number');

    startLoad("waiting for the page "+(page_number+1));

    let ctx = canvasBox(currentSelect);

    setInfoPage(ctx , pdf_id , page_number);
}

