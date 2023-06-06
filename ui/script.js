$(function() {
  $(document).delegate(".chat-btn", "click", function() {
    var value = $(this).attr("chat-value");
    var name = $(this).html();
    $("#chat-input").attr("disabled", false);
    generate_message(name, 'self');
  });
  
  $("#chat-circle").click(function() {    
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  });

  $(".chat-box-toggle").click(function() {
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  });

  enableResize(); // Enable Resizegable functionality initially

  function enableResize() {
    var chatBox = document.getElementById("chat-box");

    var initialX;
    var initialY;

    function handleResizeStart(e) {

      initialX = e.clientX - chatBox.offsetLeft;
      initialY = e.clientY - chatBox.offsetTop;

      chatBoxHeader.classList.add("resize-cursor"); 

      document.addEventListener("mousemove", handleResize);
      document.addEventListener("mouseup", handleResizeEnd);
    }

    function handleResize(e) {

      var newX = e.clientX - initialX;
      var newY = e.clientY - initialY;

      chatBox.style.left = newX + "px";
      chatBox.style.top = newY + "px";
    }

    function handleResizeEnd() {

      document.removeEventListener("mousemove", handleResize);
      document.removeEventListener("mouseup", handleResizeEnd);

      chatBoxHeader.classList.remove("resize-cursor");
    }

    var chatBoxHeader = chatBox.querySelector(".chat-box-header");
    chatBoxHeader.addEventListener("mousedown", handleResizeStart);
  }
});
