$(document).ready(function() {
  $('.like-btn').click(function() {
      var button = $(this);
      var postId = button.data('course-id');

      $.ajax({
          url: '../courses/' + postId + '/like',
          method: 'POST',
          success: function(data) {
              if (data.result === 'liked') {
                  button.html(
                    '<i class="fa-regular fa-heart"></i><span>'+data.likes+'</span>');
              } else if (data.result === "unliked") {
                  button.html(
                    '<i class="fa-regular fa-heart"></i><span>'+data.likes+'</span>');
              } else {
                  button.html(
                  '<i class="fa-regular fa-heart"></i><span>'+data.likes+'</span>');
              }
              window.location.reload();
          }
      });
  });
});