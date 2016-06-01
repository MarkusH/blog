$(document).ready(function(){
  // Mobile navigation
  $('.button-collapse').sideNav();

  // Masonry layout for index pages
  var $container = $('#posts');
  var layout = function(){
    $container.masonry({
      columnWidth: '.s6, .m3, .l2',
      itemSelector: '.col'
    });
  };
  layout();
  $container.imagesLoaded(layout);
});
