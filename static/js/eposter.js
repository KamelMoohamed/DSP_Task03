
let micInput = document.querySelector("#record");
micInput.addEventListener("click", (e) => {
  micInput.classList.toggle("mic-input-active");
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
  var constraints = { audio: true, video: false };
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(function (stream) {
      gumStream = stream;
      audioContext = new AudioContext();
      input = audioContext.createMediaStreamSource(stream);
      rec = new Recorder(input, { numChannels: 1 });
      rec.record();
    })
    .catch(function (err) {});
}

function stopRecording() {
  rec.stop();
  gumStream.getAudioTracks()[0].stop();
  rec.exportWAV(sendWAVtoBack);
}

let userName = document.querySelector(".user-name");
let currentStatus = document.querySelector(".current-status");
let progCircles = document.querySelectorAll(".circle");
let formData = new FormData();
function sendWAVtoBack(blob) {
  formData.delete("file");
  // var audio = document.getElementById('audio');
  // var url = URL.createObjectURL(blob);
  // audio.src=url
  // console.log(blob)
  // console.log(audio)
  // audio.play();

  formData.append("file", blob);

  $.ajax({
    type: "POST",
    url: "/predict",
    data: formData,
    contentType: false,
    cache: false,
    processData: false,
    async: true,
    success: function (data) {
      if (data.person != "Others") {
        
        userName.innerHTML = `Welcome ${data.person}`;
        currentStatus.innerHTML = `Right Password`;
        progCircles.forEach((circle) =>
          circle.classList.add("two-right-conds")
        );
        setTimeout(restProgCircles, 2000);
      } else {
        setTimeout(restProgCircles, 2000);
        wrongVoice();
        currentStatus.innerHTML = `Wrong Password`;
        userName.innerHTML = ``;
        progCircles.forEach((circle) =>
          circle.classList.add("two-wrong-conds")
        );
      }
    },
  });
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
  progCircles.forEach((circle) => (circle.className = "circle"));
  // console.log(progCircles)
}

function wrongVoice() {
  micInput.classList.add("wrong-voice");
  setTimeout(restMicBtn, 2000);
}
var trace1 = {
  x: [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004],
  y: [219, 146, 112, 127, 124, 180, 236, 207, 236, 263, 350, 430],
  name: 'Rest of world',
  marker: {color: 'rgba(7, 3, 49, 0.733)'},
  type: 'bar'
};
var trace2 = {
  x: [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004],
  y: [219, 146, 112, 127, 124, 180, 236, 207, 236, 263, 350, 430],
  name: 'Rest of world',
  marker: {color: 'rgba(7, 3, 49, 0.733)'},
  type: 'bar'
};
var data1 = [ trace1 ];
var data2=[ trace2 ];
var layout = {
  // autosize: true,
  useResizeHandler: true,
  responsive:true,
  height: 260,
  margin: {
    l: 24,
    r: 10,
    t: 50,
    b: 30,
    // pad:4
  },
   paper_bgcolor: 'transparent',
  plot_bgcolor: 'transparent',
  // "xaxis": {
  //   "visible": false
  // },
  legend: {
    font: {
      family: "Arial, sans-serif",
    },
  },
};
Plotly.newPlot('bar1_content', data1,layout,{responsive: true});
Plotly.newPlot('bar2_content', data2,layout,{responsive: true});


// let correct = document.querySelector(".correct");
// let wrong = document.querySelector(".test-btn.wrong");
// correct.addEventListener("click", (e) => {
//   openDoor();
// });
// wrong.addEventListener("click", (e) => {
//   wrongVoice();
//   ironDoorClose();
// });
