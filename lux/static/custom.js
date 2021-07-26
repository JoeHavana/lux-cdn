$(()=>{


  /*--------------------------
  preloader
  ---------------------------- */
  $(window).on('load', function() {
    var pre_loader = $('#preloader');
    pre_loader.fadeOut('slow', function() {
      $(this).remove();
    });
  });

  /*----------------------------
   wow js active
  ------------------------------ */
  new WOW().init();


  /*==============================================================
							NAVBAR & NAV2
  ================================================================*/
  // Toggle .header-scrolled class to #navbar when page is scrolled
  $(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
      $('#navbar').addClass('header-scrolled fixed-top');
    } else {
      $('#navbar').removeClass('header-scrolled fixed-top');
    }
  });

  if ($(window).scrollTop() > 100) {
    $('#navbar').addClass('header-scrolled');
  }

  // Update the margin-top to the #nav2 when page is scrolled
  $(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
     $('#nav2').css({'top':'60px'});
    } else {
     $('#nav2').css({'top':'120px'});
    }
  });

  /*if ($(window).scrollTop() > 100) {
    //$('#nav2').addClass({'margin-top':'60px'});
  }*/

  // Smooth scroll for the navigation menu and links with .scrollto classes
  var scrolltoOffset = $('#navbar').outerHeight() - 21;
  if (window.matchMedia("(max-width: 991px)").matches) {
    scrolltoOffset += 20;
  }
  $(document).on('click', '.nav-menu a, .mobile-nav a, .scrollto', function(e) {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      if (target.length) {
        e.preventDefault();

        var scrollto = target.offset().top - scrolltoOffset;

        if ($(this).attr("href") == '#navbar') {
          scrollto = 0;
        }

        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');

        if ($(this).parents('.nav-menu, .mobile-nav').length) {
          $('.nav-menu .active, .mobile-nav .active').removeClass('active');
          $(this).closest('li').addClass('active');
        }

        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('fa-bars');
          $('.mobile-nav-toggle i').toggleClass('fa-times color-red');
          $('.mobile-nav-overly').fadeOut();
        }
        return false;
      }
    }
  });
  

  // Mobile Navigation
  if ($('.nav-menu').length) {
    var $mobile_nav = $('.nav-menu').clone().prop({
      class: 'mobile-nav d-lg-none'
    });
    $('body').append($mobile_nav);
    $('body').prepend('<button type="button" class="mobile-nav-toggle d-lg-none"><i class="fas fa-bars"></i></button>');
    $('body').append('<div class="mobile-nav-overly"></div>');

    $(document).on('click', '.mobile-nav-toggle', function(e) {
      $('body').toggleClass('mobile-nav-active');
      $('.mobile-nav-toggle i').toggleClass('fa-bars text-white');
      $('.mobile-nav-toggle i').toggleClass('fa-times color-red');
      $('.mobile-nav-overly').toggle();
    });

    $(document).on('click', '.mobile-nav .drop-down > a', function(e) {
      e.preventDefault();
      $(this).next().slideToggle(300);
      $(this).parent().toggleClass('active');
    });

    $(document).click(function(e) {
      var container = $(".mobile-nav, .mobile-nav-toggle");
      if (!container.is(e.target) && container.has(e.target).length === 0) {
        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('fa-bars text-white');
          $('.mobile-nav-toggle i').toggleClass('fa-times color-red');
          $('.mobile-nav-overly').fadeOut();
        }
      }
    });
  } else if ($(".mobile-nav, .mobile-nav-toggle").length) {
    $(".mobile-nav, .mobile-nav-toggle").hide();
  }
  /*================	NAVBARS ENDS 	======================*/

  //----------------------------------------
  //        Bootstrap Carousel
  //-----------------------------------------
  $("#myCarousel").carousel({
    interval: 3000
  });

  //---------------------------------------------
  //Nivo slider
  //---------------------------------------------
  $('#bannerNivo').nivoSlider({  /*#ensign-nivoslider*/
    effect: 'random',
    slices: 15,
    boxCols: 12,
    boxRows: 8,
    animSpeed: 500,
    pauseTime: 5000,
    startSlide: 0,
    directionNav: true,
    prevText: '<i class="fas fa-angle-left text-white"></i:',
    nextText: '<i class="fas fa-angle-right text-white"></i:',
    controlNavThumbs: false,
    pauseOnHover: true,
    manualAdvance: false,
  });

  /*----------------------------
   Parallax
  ------------------------------ */
  var well_lax = $('.wellcome-area');
  well_lax.parallax("50%", 0.4);
  var well_text = $('.wellcome-text');
  well_text.parallax("50%", 0.6);

  /*---------------------
   Circular Bars - Knob
--------------------- */
  if (typeof($.fn.knob) != 'undefined') {
    var knob_tex = $('.knob');
    knob_tex.each(function() {
      var $this = $(this),
        knobVal = $this.attr('data-rel');

      $this.knob({
        'draw': function() {
          $(this.i).val(this.cv + '%')
        }
      });

      $this.appear(function() {
        $({
          value: 0
        }).animate({
          value: knobVal
        }, {
          duration: 2000,
          easing: 'swing',
          step: function() {
            $this.val(Math.ceil(this.value)).trigger('change');
          }
        });
      }, {
        accX: 0,
        accY: -150
      });
    });
  }
  
  /*--/ Star Counter /--*/
  $('.counter').counterUp({
    delay: 15,
    time: 2000
  });

  /*--/ Star Scrolling nav /--*/
  var mainNav_height = $('#mainNav').outerHeight() - 22;
  $('a.js-scroll[href*="#"]:not([href="#"])').on("click", function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        var scrollto = target.offset().top - mainNav_height;
        $('html, body').animate({
          scrollTop: scrollto
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  /*--/ Star Typed /--*/
  if ($('.text-slider').length == 1) {
    var typed_strings = $('.text-slider-items').text();
    var typed = new Typed('.text-slider', {
      strings: typed_strings.split(','),
      typeSpeed: 80,
      loop: true,
      backDelay: 1100,
      backSpeed: 30
    });
  }

  // Skills section
  $('.skills-content').waypoint(function() {
    $('.progress .progress-bar').each(function() {
      $(this).css("width", $(this).attr("aria-valuenow") + '%');
    });
    
  }, {
    offset: '80%'
  });


  /*====================================================
					OWL - CAROUSELS
  ======================================================*/
  /*--/ Testimonials owl /--*/
  $('#testimonial-car-light').owlCarousel({
    margin: 20,
    dots: true,
    loop: true,
    autoplay: true,
    autoplayTimeout: 4000,
    autoplayHoverPause: true,
    responsive: {
      0: {
        items: 1,
      },
      768: {
        items: 2
      },
      900: {
        items: 3
      }
    }
  });
  $('#testimonial-car-dark').owlCarousel({
    margin: 20,
    dots: true,
    loop: true,
    autoplay: true,
    autoplayTimeout: 4000,
    autoplayHoverPause: true,
    responsive: {
      0: {
        items: 1,
      },
      768: {
        items: 2
      },
      900: {
        items: 3
      }
    }
  });
  
  $('#items-car-light').owlCarousel({
    margin: 20,
    dots: true,
    loop: true,
    autoplay: true,
    autoplayTimeout: 4000,
    autoplayHoverPause: true,
    responsive: {
      0: {
        items: 1,
      },
      768: {
        items: 2
      },
      900: {
        items: 3
      }
    }
  });
  /*---------------------
   Testimonial carousel
  ---------------------*/
  $(".testimonial-carousel").owlCarousel({
    autoplay: true,
    dots: true,
    loop: true,
    responsive: {
      0: {
        items: 1
      },
      768: {
        items: 1
      },
      900: {
        items: 1
      }
    }
  });


  /*========================================*/
  //			ISOTOPE - LAYOUTS
  /*=========================================*/
  // Porfolio isotope and filter
  $(window).on('load', function() {
    var portfolioIsotope = $('.portfolio-container').isotope({
      itemSelector: '.portfolio-item',
      layoutMode: 'fitRows' // masonry, fitRows, cellsByRow, vertical, packery, masonryHorizontal, fitColums, cellsByColumn, horiz
    });

    $('#portfolio-filters li').on('click', function() {
      $("#portfolio-filters li").removeClass('filter-active');
      $(this).addClass('filter-active');

      portfolioIsotope.isotope({
        filter: $(this).data('filter')
      });
    });

  });
/*
  // Portfolio details carousel
  $(".portfolio-details-carousel").owlCarousel({
    autoplay: true,
    dots: true,
    loop: true,
    items: 1
  });
*/
  // Initiate venobox (lightbox feature used in portofilo)
  $(document).ready(function() {
    $('.venobox').venobox({
      'share': false
    });
  });


});