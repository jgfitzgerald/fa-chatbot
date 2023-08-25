// core function
function Bubbles(container, self, options) {
  // options
  clientId = null;
  chatHistoryEnabled = true;
  options = {
    responseCallbackFn: function(content) {
      requestBody = {
        "id": clientId,
        "input": content
      };

      fetch('http://localhost:5000/api/chat', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
      })
      .then(response => response.json())
      .then(data => {
          chatWindow.talk(data);
      })
      .catch(error => {
          // Handle any errors that occur during the API request
          console.error('Error fetching conversation flow:', error);
      });
    } 
    // Uncomment this to install an input field (chat box)
    // ,
    // inputCallbackFn: function(content) {
    //   requestBody = {
    //     "id": clientId,
    //     "input": content.input
    //   };

    //   fetch('http://localhost:5000/api/chat', {
    //   method: 'POST',
    //   headers: {
    //       'Content-Type': 'application/json'
    //   },
    //   body: JSON.stringify(requestBody)
    //   })
    //   .then(response => response.json())
    //   .then(data => {
    //       chatWindow.talk(data);
    //   })
    //   .catch(error => {
    //       // Handle any errors that occur during the API request
    //       console.error('Error fetching conversation flow:', error);
    //   });
    // }
  }
  animationTime = options.animationTime || 200 // how long it takes to animate chat bubble, also set in CSS
  typeSpeed = options.typeSpeed || 5 // delay per character, to simulate the machine "typing"
  widerBy = options.widerBy || 2 // add a little extra width to bubbles to make sure they don't break
  sidePadding = options.sidePadding || 6 // padding on both sides of chat bubbles
  inputCallbackFn = options.inputCallbackFn || false // should we display an input field?
  responseCallbackFn =  options.responseCallbackFn || false // is there a callback function for when a user clicks on a bubble button
  // this function is called after the user sends a message

  var _convo = {} // local memory for conversation JSON object
  //--> NOTE that this object is only assigned once, per session and does not change for this
  // 		constructor name during open session.

  // set up the stage
  container.classList.add("bubble-container")
  var bubbleWrap = document.createElement("div")
  bubbleWrap.className = "bubble-wrap"
  container.appendChild(bubbleWrap)

  // install user input textfield
  this.typeInput = function(callbackFn) {
    var inputWrap = document.createElement("div")
    inputWrap.className = "input-wrap"
    var inputText = document.createElement("textarea")
    inputText.setAttribute("placeholder", "Ask me anything...")
    inputWrap.appendChild(inputText)
    inputText.addEventListener("keypress", function(e) {
      // register user input
      if (e.key == "Enter") {
        e.preventDefault()
        typeof bubbleQueue !== false ? clearTimeout(bubbleQueue) : false // allow user to interrupt the bot
        var lastBubble = document.querySelectorAll(".bubble.say")
        lastBubble = lastBubble[lastBubble.length - 1]
        lastBubble.classList.contains("reply") &&
        !lastBubble.classList.contains("reply-freeform")
          ? lastBubble.classList.add("bubble-hidden")
          : false
        addBubble(
          '<span class="bubble-button bubble-pick">' + this.value + "</span>",
          function() {},
          "reply reply-freeform"
        )
        // callback
        typeof callbackFn === "function"
          ? callbackFn({
              input: this.value,
              convo: _convo,
            })
          : false
        this.value = ""
      }
    })
    container.appendChild(inputWrap)
    bubbleWrap.style.paddingBottom = "100px"
    inputText.focus()
  }
  inputCallbackFn ? this.typeInput(inputCallbackFn) : false

  // init typing bubble
  var bubbleTyping = document.createElement("div")
  bubbleTyping.className = "bubble-typing imagine"
  for (dots = 0; dots < 3; dots++) {
    var dot = document.createElement("div")
    dot.className = "dot_" + dots + " dot"
    bubbleTyping.appendChild(dot)
  }
  bubbleWrap.appendChild(bubbleTyping)

  // accept JSON & create bubbles
  this.talk = function(convo) {
    _convo = convo // POLYFILL REQUIRED FOR OLDER BROWSERS
    here = Object.keys(_convo)[0];
    this.reply(_convo[here])
  }

  var iceBreaker = false // this variable holds answer to whether this is the initative bot interaction or not
  this.reply = function(turn) {
    iceBreaker = typeof turn === "undefined"
    turn = !iceBreaker ? turn : _convo[Object.keys(turn)[0]]
    questionsHTML = ""
    if (!turn) return
    if (turn.reply !== undefined) {
      turn.reply.reverse()
      for (var i = 0; i < turn.reply.length; i++) {
        ;(function(el, count) {
          var escapedAnswer = el.answer.replace(/'/g, "\\'");
          var escapedQuestion = el.question.replace(/'/g, "\\'");
          questionsHTML +=
            '<span class="bubble-button" style="animation-delay: ' +
            (animationTime / 2) * count +
            'ms" onClick="' +
            self +
            ".answer('" +
            escapedAnswer + "', '" +
            escapedQuestion + "');this.classList.add('bubble-pick')\">" +
            el.question +
            '</span>';
        })(turn.reply[i], i);
      }
    }


    orderBubbles(turn.says, function() {
      bubbleTyping.classList.remove("imagine")
      questionsHTML !== ""
        ? addBubble(questionsHTML, function() {}, "reply")
        : bubbleTyping.classList.add("imagine")
    })
  }
  // navigate "answers"
  this.answer = function(key, content) {
    var func = function(key, content) {
      typeof window[key] === "function" ? window[key](content) : false;
    };
    _convo[key] !== undefined
      ? this.reply(_convo[key])
      : typeof responseCallbackFn === 'function' ? responseCallbackFn(content) : func(key, content);
  };

  // api for typing bubble
  this.think = function() {
    bubbleTyping.classList.remove("imagine")
    this.stop = function() {
      bubbleTyping.classList.add("imagine")
    }
  }

  // "type" each message within the group
  var orderBubbles = function(q, callback) {
    var start = function() {
      setTimeout(function() {
        callback()
      }, animationTime)
    }
    var position = 0
    for (
      var nextCallback = position + q.length - 1;
      nextCallback >= position;
      nextCallback--
    ) {
      ;(function(callback, index) {
        start = function() {
          addBubble(q[index], callback)
        }
      })(start, nextCallback)
    }
    start()
  }

  // create a bubble
var bubbleQueue = false;
var isFirstMessage = true;
var addBubble = function(say, posted, reply, live) {
  reply = typeof reply !== "undefined" ? reply : "";
  live = typeof live !== "undefined" ? live : true; // bubbles that are not "live" are not animated and displayed differently
  var animationTime = live ? this.animationTime : 0;
  var typeSpeed = live ? this.typeSpeed : 0;

  var messageSource = (reply === "reply" || reply === "reply reply-freeform") ? "user" : "bot";

  // create bubble element
  var msgContainer = document.createElement("div")

  var bubble = document.createElement("div");
  var avatar = document.createElement("div");

  var bubbleContent = document.createElement("span");

  msgContainer.className = "msg-container";
  bubble.className = "bubble imagine " + (!live ? " history " : "") + reply;
  avatar.className = "avatar";
  bubbleContent.className = "bubble-content";
  bubbleContent.innerHTML = say;

  bubble.appendChild(bubbleContent);

  if (messageSource == "user") {
    if (reply === "reply reply-freeform") { // TEXT INPUT IS HANDLED HERE
      msgContainer = bubbleWrap.childNodes[bubbleWrap.childNodes.length - 2]
      msgContainer.insertBefore(bubble, msgContainer.lastChild)
      avatar.style.marginRight = 0;
    } else {
    msgContainer.id = "user-message";
    msgContainer.appendChild(bubble);
    msgContainer.appendChild(avatar);
    avatar.style.marginRight = 0;
    }
  } else {
    msgContainer.id = "bot-message";
    msgContainer.appendChild(avatar);
    msgContainer.appendChild(bubble);
    avatar.style.marginLeft = 0;
    if (isFirstMessage) {
      isFirstMessage = false;
    } else {
      avatar.style.backgroundImage = "none";
      avatar.style.backgroundColor = "transparent";
      avatar.style.border = "none";
    }
  }

  avatar.style.visibility = "hidden";

  bubbleWrap.insertBefore(msgContainer, bubbleTyping);

  // answer picker styles
  if (reply !== "") {
    var bubbleButtons = bubbleContent.querySelectorAll(".bubble-button");
    bubble.addEventListener("click", function(e) {
      if (e.target.classList.contains("bubble-button")) {
        for (var i = 0; i < bubbleButtons.length; i++) {
          (function(el) {
            // el.style.width = 0 + "px"
            if (!el.classList.contains("bubble-pick")) {
              el.style.display = "none";
            }
            el.classList.contains("bubble-pick") ? (el.style.width = "") : false;
            el.removeAttribute("onclick");
          })(bubbleButtons[i]);
        }

        this.classList.add("bubble-picked");
      }
    });
    isFirstMessage = true;
  }

  // time, size & animate
  wait = live ? animationTime * 2 : 0;
  minTypingWait = live ? animationTime * 6 : 0;
  if (say.length * typeSpeed > animationTime && reply == "") {
    wait += typeSpeed * say.length;
    wait < minTypingWait ? (wait = minTypingWait) : false;
    setTimeout(function() {
      bubbleTyping.classList.remove("imagine");
    }, animationTime);
  }

  live &&
    setTimeout(function() {
      bubbleTyping.classList.add("imagine");
    }, wait - animationTime * 2);

  bubbleQueue = setTimeout(function() {
    bubble.classList.remove("imagine");
    avatar.style.visibility = "visible";
    bubble.style.width = say.includes("<img src=") ? "50%" : bubble.style.width;
    bubble.classList.add("say");
    posted();

    // animate scrolling
    containerHeight = container.offsetHeight;
    scrollDifference = bubbleWrap.scrollHeight - bubbleWrap.scrollTop;
    scrollHop = scrollDifference / 200;
    var scrollBubbles = function() {
      for (var i = 1; i <= scrollDifference / scrollHop; i++) {
        (function() {
          setTimeout(function() {
            bubbleWrap.scrollHeight - bubbleWrap.scrollTop > containerHeight
              ? (bubbleWrap.scrollTop = bubbleWrap.scrollTop + scrollHop)
              : false;
          }, i * 5);
        })();
      }
    };
    setTimeout(scrollBubbles, animationTime / 2);
  }, wait + animationTime * 2);
};

// below functions are specifically for WebPack-type project that work with import()

// this function automatically adds all HTML and CSS necessary for chat-bubble to function
function prepHTML(options) {
  // options
  var options = typeof options !== "undefined" ? options : {}
  var container = options.container || "chat" // id of the container HTML element
  var relative_path = options.relative_path || "./node_modules/chat-bubble/"

  // make HTML container element
  window[container] = document.createElement("div")
  window[container].setAttribute("id", container)
  document.body.appendChild(window[container])

  // style everything
  var appendCSS = function(file) {
    var link = document.createElement("link")
    link.href = file
    link.type = "text/css"
    link.rel = "stylesheet"
    link.media = "screen,print"
    document.getElementsByTagName("head")[0].appendChild(link)
  }
  appendCSS(relative_path + "component/styles/input.css")
  appendCSS(relative_path + "component/styles/reply.css")
  appendCSS(relative_path + "component/styles/says.css")
  appendCSS(relative_path + "component/styles/setup.css")
  appendCSS(relative_path + "component/styles/typing.css")
}

// exports for es6
if (typeof exports !== "undefined") {
  exports.Bubbles = Bubbles
  exports.prepHTML = prepHTML
}
}