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
      if (
        data.graph1 &&
        data.graph2 &&
        data.spectrogram1 &&
        data.spectrogram2
      ) {
        drawBarPlot(
          data.graph1,
          data.graph2,
          data.spectrogram1,
          data.spectrogram2
        );
      }
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

function drawBarPlot(data1, data2, spectrogram1, spectrogram2) {
  let colorScale = [
    ["0.0", "#023a21"],
    ["0.111111111111", "#035934"],
    ["0.222222222222", "#027161"],
    ["0.333333333333", "#02888e"],
    ["0.444444444444", "#01a0bb"],
    ["0.555555555556", "#00b7e8"],
    ["0.666666666667", "#048ac5"],
    ["0.777777777778", "#085da2"],
    ["0.888888888889", "#0f025b"],
    ["1.0", "#0f025b"],
  ];

  let spectrolayout = {
    width: 430,
    height: 260,
    margin: { l: 30, r: 40, b: 25, t: 25, pad: 1 },
    yaxis: { range: [0, Math.max.apply(Math, spectrogram1.f)] },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
  };

  var trace1 = {
    x: data1.x,
    y: data1.y,
    name: "Rest of world",
    marker: { color: "rgba(7, 3, 49, 0.733)" },
    type: "bar",
  };
  var trace2 = {
    x: data2.x,
    y: data2.y,
    name: "Rest of world",
    marker: { color: "rgba(7, 3, 49, 0.733)" },
    type: "bar",
  };

  originalSpectrogram1 = {
    x: spectrogram1.t,
    y: spectrogram1.f,
    z: spectrogram1.Sxx,
    type: "heatmap",
    colorscale: colorScale,
  };
  originalSpectrogram2 = {
    x: spectrogram2.t,
    y: spectrogram2.f,
    z: spectrogram2.Sxx,
    type: "heatmap",
    colorscale: colorScale,
  };

  var data1 = [trace1];
  var data2 = [trace2];

  var layout = {
    title: {
      text:'Model ',
      font: {
        family: 'Courier New, monospace',
        size: 24
      },  
    },
    useResizeHandler: true,
    height: 260,
    margin: {
      l: 50,
      r: 10,
      t: 50,
      b: 40,
    },
    xaxis: {
      title: {
        text: 'labels',
        font: {
          family: 'Arial, sans-serif',
          size: 18,
          color: '#000522e0'
        },
        showticklabels: true,
        tickfont: {
          family: 'Old Standard TT, serif',
          size: 14,
          color: 'white'
        },
      },},
      yaxis: {
        title: {
          text: 'precentage',
          font: {
            family: 'Arial, sans-serif',
            size: 16,
            color: '#000522e0'
          }
        }
      },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    legend: {
      font: {
        family: "Arial, sans-serif",
      },
    },
  };
  Plotly.newPlot("bar1_content", data1, layout, { responsive: true });
  Plotly.newPlot("bar2_content", data2, layout, { responsive: true });
  Plotly.newPlot("spectro1_content", [originalSpectrogram1], spectrolayout);
  Plotly.newPlot("spectro2_content", [originalSpectrogram2], spectrolayout);
}
