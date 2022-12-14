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
      if (data.graph1 && data.graph2 && data.graph3 && data.graph4) {
        drawBarPlot(data.graph1, data.graph2, data.graph3, data.graph4);
      }
      if (data.prediction != "Others") {
        userName.innerHTML = `Welcome ${data.prediction}`;
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

function drawBarPlot(data1, data2, data3, data4) {
  console.log(data3.y);
  var trace1 = {
    x: data1.x,
    y: data1.y,
    name: "Rest of world",
    marker: { color: "#00051e" },
    type: "bar",
  };
  var trace2 = {
    x: data2.x,
    y: data2.y,
    name: "Rest of world",
    marker: { color: "#00051e" },
    type: "bar",
  };
  
  var traceopen={
    x: data3.x.slice(0,40),
    y: data3.y.slice(0,40),
    mode: "markers+text",
    type: "scatter",
    text: Array(40).fill('op'),
    marker: { size: 12, color: "red" },
  }
  var traceother={
    x: data3.x.slice(40,325),
    y: data3.y.slice(40,325),
    mode: "markers+text",
    type: "scatter",
    text: Array(325-40).fill('ot'),
    marker: { size: 12, color: "blue" },
  }
  
  var data1 = [trace1];
  var data2 = [trace2];
  var trace3 = [
    traceopen,traceother
  ];

  var trace4 = [
    {
      x: data4.x,
      y: data4.y,
      mode: "markers",
      type: "scatter",
      // text: ["Kamel", "Abdelrahman", "Sama", "Yousr", ],
      marker: { size: 12, color: data4.color },
    },
  ];

  var layout = {
    title: {
      font: {
        family: "Roboto",
        size: 24,
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
        text: "labels",
        font: {
          family: "Roboto",
          size: 14,
          color: "#000522e0",
        },
        showticklabels: true,
        tickfont: {
          family: "Roboto",
          size: 14,
          color: "white",
        },
      },
    },
    yaxis: {
      range: [0, 100],
      title: {
        text: "percentage",
        font: {
          family: "Arial, sans-serif",
          size: 16,
          color: "#000522e0",
        },
      },
    },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    legend: {
      font: {
        family: "Arial, sans-serif",
      },
    },
  };

  var scatterLayout = {
    title: {
      font: {
        family: "Roboto",
        size: 24,
      },
    },
    width: 550,
    height: 340,
    margin: {
      l: 10,
      r: 10,
      t: 30,
      b: 40,
    },
    xaxis: {
      title: {
        text: "mffc_2",
        font: {
          family: "Roboto",
          size: 14,
          color: "#000522e0",
        },
      },
    },
    yaxis: {
      title: {
        text: "mfcc_1",
        font: {
          family: "Arial, sans-serif",
          size: 16,
          color: "#000522e0",
        },
      },
    },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    
  };

  Plotly.newPlot("bar1_content", data1, layout, { responsive: true });
  Plotly.newPlot("bar2_content", data2, layout, { responsive: true });
  Plotly.newPlot("spectro1_content", trace3, scatterLayout);
  Plotly.newPlot("spectro2_content", trace4, scatterLayout);
}
