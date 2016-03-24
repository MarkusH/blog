$(document).ready(function(){
  // Mobile navigation
  $('.button-collapse').sideNav();

  // Masonry layout for index pages
  var $container = $('#posts');
  var layout = function(){
    $container.masonry({
      columnWidth: '.s12, .m6, .l4',
      itemSelector: '.col'
    });
  };
  layout();
  $container.imagesLoaded(layout);
});
