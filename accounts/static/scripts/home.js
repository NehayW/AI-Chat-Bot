$(document).ready(function() {

    
    // check_if_media_requested(input.innerHTML)
    $('#myForm').submit(function(event) {
      /*Takes input from user, creates a user message card and appends it in chatbox.
      Sends the input to django view through ajax and appends the response to bot message card in chatbox. */
     
      event.preventDefault();
      input = document.getElementById("clear_input")
      // console.log("Input Value", )
      // // debugger;
      // value = check_if_media_requested(input.value)
      
      var user = input.dataset.user
      console.log("Input Data", input, "User,", user)
      add_user_input = document.querySelector(".chat-window")
      add_user_input.innerHTML +=` <div class="user-dialog-box row justify-content-end align-items-center">
      <div class="col-md-7 user-text text-end"><p>${input.value}</p></div>
      <div class="col-md-2 d-md-block d-none">
        <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-5.webp" alt="avatar"
        class="p-0 m-auto rounded-circle d-flex align-self-end shadow-1-strong" width="60">
        <p class="text-center">${user}</p>
      </div></div>`
      chatbox.scrollTop(chatbox.prop("scrollHeight"));
    
      $.ajax({
      type: 'POST',
      url: '',
      data: $(this).serialize(),
      // data: input.value,
      success: function(response) {
          document.getElementById("chat-window").innerHTML +=` <div class="ai-dialog-box row justify-content-start align-items-center">
          <div class="col-md-2 d-md-block d-none">
            <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-5.webp" alt="avatar"
            class="p-0 m-auto rounded-circle d-flex align-self-end shadow-1-strong" width="60">
            <p class="text-center">${response.name}</p>
          </div>
          <div class="col-md-7 bot-text text-start">
            <p>${response.response}</p>
            <a class=" dispaly-inline text-white" id="speak-button">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-volume-up" viewBox="0 0 16 16">
                <path d="M11.536 14.01A8.473 8.473 0 0 0 14.026 8a8.473 8.473 0 0 0-2.49-6.01l-.708.707A7.476 7.476 0 0 1 13.025 8c0 2.071-.84 3.946-2.197 5.303l.708.707z"/>
                <path d="M10.121 12.596A6.48 6.48 0 0 0 12.025 8a6.48 6.48 0 0 0-1.904-4.596l-.707.707A5.483 5.483 0 0 1 11.025 8a5.483 5.483 0 0 1-1.61 3.89l.706.706z"/>
                <path d="M10.025 8a4.486 4.486 0 0 1-1.318 3.182L8 10.475A3.489 3.489 0 0 0 9.025 8c0-.966-.392-1.841-1.025-2.475l.707-.707A4.486 4.486 0 0 1 10.025 8zM7 4a.5.5 0 0 0-.812-.39L3.825 5.5H1.5A.5.5 0 0 0 1 6v4a.5.5 0 0 0 .5.5h2.325l2.363 1.89A.5.5 0 0 0 7 12V4zM4.312 6.39 6 5.04v5.92L4.312 9.61A.5.5 0 0 0 4 9.5H2v-3h2a.5.5 0 0 0 .312-.11z"/>
              </svg>
            </a>
          </div>
        </div>`
        chatbox.scrollTop(chatbox.prop("scrollHeight"));
        input.value=''
      },
      error: function(response) {
          // Handle the error
          alert('Error occurred while submitting the form');
          }
      }); 
    });
});

// To keep the scrollbar at bottom at all times. This showed animation.
// $(".chatbox").animate({ scrollTop: $(".chatbox").get(0).scrollHeight }, "fast");

//This keeps the scrollbar down without animation.
var chatbox = $(".chat-window");
chatbox.scrollTop(chatbox.prop("scrollHeight"));    


//To convert speech to text
runSpeechRecog = () => {
  console.log("Speech recognition working")
  let recognization = new webkitSpeechRecognition();
  recognization.onstart = () => {
      document.getElementById("clear_input").value = "Listening.......";
    }
  recognization.onresult = (e) => {
    var transcript = e.results[0][0].transcript;
    console.log(transcript)
    document.getElementById("clear_input").value = transcript;
    }
  recognization.start();
}


//To convert text to speech
let speakButton = document.getElementById("speak-button");
speakButton.addEventListener("click", function() {
  console.log("Speak button clicked")
  var parentCard = $(this).closest('.card');
  var botReplyElement = parentCard.find('.card-body #bot_reply');
  var botReplyText = botReplyElement.text();

  let utterance = new SpeechSynthesisUtterance();

  utterance.text = botReplyText;
  utterance.voice = window.speechSynthesis.getVoices()[0];

  window.speechSynthesis.speak(utterance);
});


function check_if_media_requested(input){
  input_arr = input.split(/(\s+)/) // Splits string into words
  console.log("Input Arr", input_arr)
  list_arr = ['image', 'img', 'pic', 'picture', 'send pic', 'send img']
  result = list_arr.some(value => input_arr.includes(value));
  console.log("result:::", result)
  return result
}

