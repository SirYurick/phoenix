$(document).ready(function() {
  
  // Fancybox Video Galleries
  $(".fancybox-gallery").fancybox({
    
    afterShow: function() {
      // After the show-slide-animation has ended - play the video
      this.content.find('video').trigger('play')
      // Trigger fancybox.next() once the video has ended
      this.content.find('video').on('ended', function() {
        $.fancybox.next();
      });
    }
      
  });
  
  // Fancybox Single Videos
  $(".fancybox-single").fancybox({
    
    afterShow: function() {
      // After the show-slide-animation has ended - play the video
      this.content.find('video').trigger('play')
      // Trigger fancybox.close() once the video has ended
      this.content.find('video').on('ended', function() {
        $.fancybox.close();
      });
    }
      
  });

});