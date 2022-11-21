//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						
var rec; 							
var input; 	
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext 
var constraints = { audio: true, video:false }


// import ajax from 'ajax'
let doorHandle = document.querySelector(".door-handle");
let windowHandle = document.querySelector(".window-handle");
let door = document.querySelector(".door");
let doorIsOpened = false;
doorHandle.addEventListener("click", (e) => {
  micInput.click();
});

let eyes = document.querySelector(".eyes");
let eyelid = document.querySelectorAll(".eyelid");

function closeEyelid() {
  eyelid.forEach((oneEyelid) => oneEyelid.classList.add("eyelid-close"));
  setTimeout(openEyelid, 150);
}
function openEyelid() {
  eyelid.forEach((oneEyelid) => oneEyelid.classList.remove("eyelid-close"));
}

setInterval(closeEyelid, 3000);

function eyesBreathInhalation() {
  eyes.classList.add("eyes-breath");
  setTimeout(eyesBreathExhalation, 1500);
}
function eyesBreathExhalation() {
  eyes.classList.remove("eyes-breath");
}

setInterval(eyesBreathInhalation, 4000);

let micInput = document.querySelector("#record");
micInput.addEventListener("click", (e) => {
  ironDoor.classList.remove("iron-door-close");
  micInput.classList.toggle("mic-input-active");
  if (!door.classList.contains("door-open")) {
    document.querySelector(".door-window").classList.toggle("door-window-open");
    document.querySelector(".window-handle").classList.toggle("window-handle-open");
  }
});


recordButton = document.getElementById("record");
recordButton.addEventListener("click", (e) => {
  if (!e.target.classList.contains("mic-input-active")) {
    stopRecording();
  } else {
    startRecording();
  }
});


function readURL(file) {
  var reader = new FileReader();
  reader.readAsDataURL(file);
  return reader;
}

function startRecording() {
  var constraints = {
    audio: true,
    video: false,
  };
  navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
      gumStream=stream
      audioContext = new AudioContext();
      input = audioContext.createMediaStreamSource(stream);
      rec = new Recorder(input, {numChannels: 1,});
      rec.record();
    })
    .catch(function (err) {});
    }

function stopRecording() {
  rec.stop();
	gumStream.getAudioTracks()[0].stop();
	rec.exportWAV(createDownloadLink);
}

var audioFile;
function createDownloadLink(blob) {
  var audio = document.getElementById('audio');
  var url = URL.createObjectURL(blob);
  audio.src=url
  console.log(audio.src)
  audio.play();

  // reader = readURL(audioFile);
  let formData = new FormData();
  formData.append("file", blob)

  $.ajax({
    type: "POST",
    url: "/predict",
    data: formData,
    contentType: false,
    cache: false,
    processData: false,
    async: true,
    success: function (data) {
      console.log(data)
      if(data.person != "Others" && data.sentence != "Others"){
        data.sentence == "Open" ? openDoor() : closeDoor()
      } else {
        !door.classList.contains("door-open") ? ironDoorClose() & wrongVoice() : wrongVoice()
      }
    },
  });
}

let ironDoor = document.querySelector(".iron-door");
function openDoor() {
  door.classList.add("door-open");
  micInputCorrect()
}

function closeDoor() {
  door.classList.remove("door-open");
  micInputCorrect()
}

function micInputCorrect() {
  micInput.classList.add("correct-voice");
  setTimeout(restMicBtn, 2000);
}

function micInputWrong() {
  micInput.classList.add("wrong-voice");
  setTimeout(restMicBtn, 2000);
}

function restMicBtn() {
  micInput.classList.remove("correct-voice");
  micInput.classList.remove("wrong-voice");
}

function wrongVoice() {
  micInput.classList.add("wrong-voice");
  setTimeout(restMicBtn, 2000);
}

function ironDoorClose() {
  ironDoor.classList.toggle("iron-door-close");
}


let correct = document.querySelector(".correct");
let wrong = document.querySelector(".test-btn.wrong");
correct.addEventListener("click", (e) => {
  openDoor();
});
wrong.addEventListener("click", (e) => {
  wrongVoice();
  ironDoorClose()
});
