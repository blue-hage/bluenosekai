$(function() {


    const keyName = 'visited';
    const keyValue = true;

    if (!sessionStorage.getItem(keyName)) {
        //sessionStorageにキーと値を追加
        sessionStorage.setItem(keyName, keyValue);

        $('.anime img').fadeIn(2000);
        $(".mainSite").css("display", "none");



        setTimeout(function() {
            $('.anime').fadeOut();
            
            }, 3800);
        
        $(".mainSite").css({opacity:'0'});
        setTimeout(function(){
        $(".mainSite").css("display", "block");
        $(".mainSite").stop().animate({opacity:'1'},2000);//1秒かけてコンテンツを表示
        }, 3800);//約4秒後に
        
        $(".mainSite").one(function(){
            $(".mainSite").css("display", "none");
        });


    } else {
        $(".anime").css("display", "none");
        $(".mainSite").css("display", "block");


    }

   



    $('.close').click(function() {
        $('input[type="checkbox"]').prop('checked', false);
    });

   



    $('.no-scroll').addClass('showUp');
    $('.no-scroll').addClass('showUp-text');

    $(window).on('scroll', function() {
        $('.fade-text').each(function(){
            if ($(window).scrollTop() >= $(this).offset().top - $(window).height() + 100) {
                $(this).addClass('showUp');
            }
        });
    });



    $(window).on('scroll', function() {
        $('.container').each(function(){
            if ($(window).scrollTop() >= $(this).offset().top - $(window).height() + 100) {
                $(this).addClass('showUp');
            }
        });
    });

    $('.profile1').click(function(){
        if($('.profile1 img').hasClass('scale')){
            $('.profile1 img').removeClass('scale');
        }else if($('.profile2 img').hasClass('scale')){
            $('.profile2').trigger("click");
            $('.profile2 img').removeClass('scale');
            $('.profile1 img').addClass('scale');
        }else{
            $('.profile1 img').addClass('scale');
        }
    });

    $('.profile2').click(function(){
        if($('.profile2 img').hasClass('scale')){
            $('.profile2 img').removeClass('scale');
        }else if($('.profile1 img').hasClass('scale')){
            $('.profile1').trigger("click");
            $('.profile1 img').removeClass('scale');
            $('.profile2 img').addClass('scale');
        }else{
            $('.profile2 img').addClass('scale');
        }
    });







  

    $(".center").slick({
      infinite: true, 
      centerMode: true,
      slidesToShow: 1,
      adaptiveHeight: true,
      autoplay: true,
      autoplaySpeed: 6000,
    });



    
});