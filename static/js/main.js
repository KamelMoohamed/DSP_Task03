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

URL = window.URL || window.webkitURL;
var gumStream, rec, input, audioContext; 						
var AudioContext = window.AudioContext || window.webkitAudioContext;

function startRecording() {
  var constraints = {audio: true, video: false};
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
	rec.exportWAV(sendWAVtoBack);
}

let userName = document.querySelector(".user-name")
let currentStatus = document.querySelector(".current-status")
let progCircles = document.querySelectorAll(".circle")
let formData = new FormData();
function sendWAVtoBack(blob) {
  formData.delete('file');
  // var audio = document.getElementById('audio');
  // var url = URL.createObjectURL(blob);
  // audio.src=url
  // console.log(blob)
  // console.log(audio)
  // audio.play();

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
        userName.innerHTML = `Welcome ${data.person}`
        currentStatus.innerHTML = `Right Password`
        progCircles.forEach((circle) => circle.classList.add("two-right-conds"));
        setTimeout(restProgCircles, 2000);
      } else {
        setTimeout(restProgCircles, 2000);
        !door.classList.contains("door-open") ? ironDoorClose() & wrongVoice() : wrongVoice()
        if(data.person == "Others" && data.sentence == "Others"){
           userName.innerHTML = `Who Are You?!`; 
           currentStatus.innerHTML = `Wrong Password`
           progCircles.forEach((circle) => circle.classList.add("two-wrong-conds"));
           console.log(progCircles)
          } else if (data.person != "Others" && data.sentence == "Others"){
              progCircles[0].classList.add("one-cond");
              userName.innerHTML = `${data.person}`;
              currentStatus.innerHTML = `it seems i can't hear you`
            }
            else {
              progCircles[0].classList.add("one-cond");
              userName.innerHTML = `But who Are You?!`;
              currentStatus.innerHTML = `Right Password`
                  }
        
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

function restProgCircles() {
  progCircles.forEach((circle) => circle.className = ("circle"));
  // console.log(progCircles)
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
