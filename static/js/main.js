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
    document
      .querySelector(".window-handle")
      .classList.toggle("window-handle-open");
  }
});

var recorder;
window.onload = function () {
  recordButton = document.getElementById("record");
  navigator.mediaDevices.getUserMedia({ audio: true }).then(
    function (stream) {
      recordButton.addEventListener("click", (e) => {
        if (!e.target.classList.contains("mic-input-active")) {
          stopRecording();
        } else {
          startRecording();
        }
      });
      var options = { mimeType: "audio/webm" };
      recorder = new MediaRecorder(stream, options);
      recorder.addEventListener("dataavailable", (record) => {
        onRecordingReady(record);
      });
    },
    function () {
      document.querySelector("#audioMediaNotAvailable").show;
    }
  );
};

function readURL(file) {
  var reader = new FileReader();
  reader.readAsDataURL(file);
  return reader;
}

function startRecording() {
  recorder.start();
}
function stopRecording() {
  recorder.stop();
}
var audioFile;
function onRecordingReady(record) {
  var audio = document.getElementById("audio");
  audioFile = record.data;

  // reader = readURL(audioFile);
  let formData = new FormData();
  formData.append("file", audioFile)

  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/predict",
    data: formData,
    contentType: false,
    cache: false,
    processData: false,
    async: true,
    success: function (data) {
      console.log("TESTTTTTTTTTTTTT");
    },
  });

  audio.src = URL.createObjectURL(audioFile);
  audio.play();
}

let ironDoor = document.querySelector(".iron-door");
function correctVoice() {
  door.classList.toggle("door-open");
  micInput.classList.add("correct-voice");
  setTimeout(restMicBtn, 2000);
}

function wrongVoice() {
  micInput.classList.toggle("wrong-voice");
  ironDoor.classList.toggle("iron-door-close");
  setTimeout(restMicBtn, 2000);
}

function restMicBtn() {
  micInput.classList.remove("correct-voice");
  // micInput.classList.remove("wrong-voice")
}

let correct = document.querySelector(".correct");
let wrong = document.querySelector(".test-btn.wrong");
correct.addEventListener("click", (e) => {
  correctVoice();
});
wrong.addEventListener("click", (e) => {
  wrongVoice();
});
