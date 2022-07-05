$(window).resize(function(){
    console.log('resize called');
    var width = $(window).width();
    if(width > 960){
        $('div').removeClass('col-4');
        $('div').removeClass('col-8');
    }
 })
 .resize();