$(document).ready(function(){
  // Mobile navigation
  $('.button-collapse').sideNav();
  $('.search .button').on('click', function(){$('.search input').focus()})


  // Masonry layout for index pages
  var $container = $('#posts');
  $container.imagesLoaded(function(){
    $container.masonry({
        columnWidth: '.s12, .m6, .l4',
        itemSelector: '.col'
    });
  });
});
