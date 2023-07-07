$(function() {

  // initialize by constructing a named function./chat-bubble.
  chatWindow = new Bubbles(
    document.getElementById("chat"), // ./chat-bubble.passing HTML container element./chat-bubble.
    "chatWindow", // ./chat-bubble.and name of the function as a parameter
  );

  var chatStarted = false; // prevents first message from sending multiple times
  var chatCircle = document.getElementById("chat-circle");
  chatCircle.addEventListener("click", sendFirstMessage);

  function sendFirstMessage() {
    // Make a POST request to fetch the conversation flow from the API
    if (!chatStarted) {
      fetch('http://localhost:5000/app/start', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
      })
      .then(response => response.json())
      .then(data => {
          // Assign the conversation flow JSON to the convo variable
          var convo = data;
          clientId = convo.id;
          delete convo.id;
          chatStarted = true;

          chatWindow.talk(convo);
      })
      .catch(error => {
          // Handle any errors that occur during the API request
          console.error('Error fetching conversation flow:', error);
      });
    }
  }
  
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
});
