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

  enableResize();
  enableMove();

  function enableResize() {
    var chatBox = document.getElementById("chat-box");
    var resizeIcon = document.getElementById("resize-icon");

    var initialX;
    var initialY;

    function handleResizeStart(e) {

      initialX = e.clientX - chatBox.offsetLeft;
      initialY = e.clientY - chatBox.offsetTop;

      resizeIcon.classList.add("resize-cursor"); 

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

      resizeIcon.classList.remove("resize-cursor");
    }

    resizeIcon.addEventListener("mouseenter", function () {
      chatBox.style.cursor = "nwse-resize";
    });
  
    resizeIcon.addEventListener("mouseleave", function () {
      chatBox.style.cursor = "default";
    });

    resizeIcon.addEventListener("mousedown", handleResizeStart);

    
  }

  function enableMove() {
    var chatBox = document.getElementById("chat-box");
    var moveIcon = document.getElementById("move-icon");
  
    var initialX;
    var initialY;
  
    function handleMoveStart(e) {
      initialX = e.clientX - chatBox.offsetLeft;
      initialY = e.clientY - chatBox.offsetTop;
  
      chatBox.style.cursor = "move";
  
      document.addEventListener("mousemove", handleMove);
      document.addEventListener("mouseup", handleMoveEnd);
    }
  
    function handleMove(e) {
      var newX = e.clientX - initialX;
      var newY = e.clientY - initialY;
  
      chatBox.style.left = newX + "px";
      chatBox.style.top = newY + "px";
    }
  
    function handleMoveEnd() {
      chatBox.style.cursor = "default";
  
      document.removeEventListener("mousemove", handleMove);
      document.removeEventListener("mouseup", handleMoveEnd);
    }
  
    moveIcon.addEventListener("mousedown", handleMoveStart);
    moveIcon.addEventListener("mouseenter", function () {
      chatBox.style.cursor = "move";
    });
  
    moveIcon.addEventListener("mouseleave", function () {
      chatBox.style.cursor = "default";
    });
  }

});
