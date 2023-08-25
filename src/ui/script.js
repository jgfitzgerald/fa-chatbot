$(function() {

  // initialize by constructing a named function./chat-bubble.
  chatWindow = new Bubbles(
    document.getElementById("chat"), // ./chat-bubble.passing HTML container element./chat-bubble.
    "chatWindow" // ./chat-bubble.and name of the function as a parameter
  );

  chatStarted = false; // prevents first message from sending multiple times
  var chatCircle = document.getElementById("chat-circle");
  chatCircle.addEventListener("click", sendFirstMessage);

  // Event listener for the refresh button
  var refreshButton = document.querySelector(".chat-box-refresh");

  refreshButton.addEventListener("click", function() {
    deleteChat(clientId);
    chatStarted = false;
    document.querySelector(".bubble-wrap").remove();
    chatWindow = new Bubbles(
      document.getElementById("chat"), // ./chat-bubble.passing HTML container element./chat-bubble.
      "chatWindow" // ./chat-bubble.and name of the function as a parameter
    );
    sendFirstMessage();
  });

  // delete the chat if the page is reloaded
  window.onbeforeunload = function(event) {
    chatStarted = false;
    deleteChat(clientId);
  };

  function sendFirstMessage() {
    // Make a POST request to fetch the conversation flow from the API
    if (!chatStarted) {
      fetch("http://localhost:5000/api/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(response => response.json())
        .then(data => {
          // Assign the conversation flow JSON to the convo variable
          var convo = data;
          clientId = convo.id;

          sessionStorage.setItem('clientID', clientId);

          delete convo.id;
          chatStarted = true;

          chatWindow.talk(convo);
        })
        .catch(error => {
          // Handle any errors that occur during the API request
          console.error("Error fetching conversation flow:", error);
        });
    }
  }

  function deleteChat(clientId) {
    fetch(`http://localhost:5000/api/end?id=${clientId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {})
    .catch(error => console.error('Error:', error));
}

  $("#chat-circle").click(function() {
    $("#chat-circle").toggle("scale");
    $(".chat-box").toggle("scale");

    // Scroll to the bottom of the chat container when opened
    var bubbleWrap = document.querySelector(".bubble-wrap");
    bubbleWrap.scrollTop = bubbleWrap.scrollHeight;
  });

  $(".chat-box-toggle").click(function() {
    $("#chat-circle").toggle("scale");
    $(".chat-box").toggle("scale");

    // Scroll to the bottom of the chat container when opened
    var bubbleWrap = document.querySelector(".bubble-wrap");
    bubbleWrap.scrollTop = bubbleWrap.scrollHeight;
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

    resizeIcon.addEventListener("mouseenter", function() {
      chatBox.style.cursor = "nwse-resize";
    });

    resizeIcon.addEventListener("mouseleave", function() {
      chatBox.style.cursor = "default";
    });

    resizeIcon.addEventListener("mousedown", handleResizeStart);
  }
});
