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

function getBarLayout(yIndex) {
  return {
    useResizeHandler: true,
    height: 260,
    margin: {
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
    shapes: [
      {
        type: "line",
        x0: -1,
        y0: yIndex,
        x1: 3,
        y1: yIndex,
        line: {
          color: "rgb(55, 128, 191)",
          width: 1,
        },
      },
    ],
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    legend: {
      font: {
        family: "Arial, sans-serif",
      },
    },
  };
}

function drawBarPlot(data1, data2, data3, data4) {
  var traceModel1 = {
    x: data1.x,
    y: data1.y,
    marker: { color: "#00051e" },
    type: "bar",
  };
  var traceModel2 = {
    x: data2.x,
    y: data2.y,
    marker: { color: "#00051e" },
    type: "bar",
  };

  var traceOpen = {
    x: data3.x.slice(0, 76),
    y: data3.y.slice(0, 76),
    mode: "markers",
    type: "scatter",
    name: "Open",
    marker: { size: 12, color: "red" },
  };
  var traceOther = {
    x: data3.x.slice(76, 324),
    y: data3.y.slice(76, 324),
    mode: "markers",
    type: "scatter",
    name: "other",
    marker: { size: 12, color: "blue" },
  };
  var tracePoint = {
    x: data3.x[325],
    y: data3.y[325],
    mode: "markers",
    type: "scatter",
    name: "prediction point",
    marker: { size: 20, color: "green", Symbol: "x" },
  };

  var traceKamel = {
    x: data4.x.slice(0, 23),
    y: data4.y.slice(0, 23),
    mode: "markers",
    type: "scatter",
    name: "Sama",
    marker: { size: 12, color: "red" },
  };
  var traceSama = {
    x: data4.x.slice(45, 78),
    y: data4.y.slice(45, 78),
    mode: "markers",
    type: "scatter",
    name: "Kamel",
    marker: { size: 12, color: "blue" },
  };

  var traceYousr = {
    x: data4.x.slice(78, 102),
    y: data4.y.slice(78, 102),
    mode: "markers",
    type: "scatter",
    name: "yousr",
    marker: { size: 12, color: "gray" },
  };
  var traceAbdelrhaman = {
    x: data4.x.slice(23, 45),
    y: data4.y.slice(23, 45),
    mode: "markers",
    type: "scatter",
    name: "Abdelrhaman",
    marker: { size: 12, color: "orange" },
  };
  var tracePoint2 = {
    x: data4.x[103],
    y: data4.y[103],
    mode: "markers",
    type: "scatter",
    name: "Prediction Point",
    marker: { size: 20, color: "green", Symbol: "x" },
  };
  var barMode1 = [traceModel1];
  var barModel2 = [traceModel2];
  var scatterModel1 = [traceOpen, traceOther, tracePoint];
  var scatterModel2 = [
    traceKamel,
    traceSama,
    traceYousr,
    traceAbdelrhaman,
    tracePoint2,
  ];

  var scatterLayout = {
    width: 520,
    height: 320,
    margin: {
      t: 30,
    },
    xaxis: {
      title: {
        text: "mffc_1",
        font: {
          family: "Roboto",
          size: 14,
          color: "#000522e0",
        },
      },
    },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
  };
  var scatterModel1_update = {
    yaxis: {
      title: {
        text: "mffc_2",
        font: {
          family: "Roboto",
          size: 14,
          color: "#000522e0",
        },
      },
    },
  };
  var scatterModel2_update = {
    yaxis: {
      title: {
        text: "mffc_2",
        font: {
          family: "Roboto",
          size: 14,
          color: "#000522e0",
        },
      },
    },
  };
  Plotly.newPlot("bar1_content", barMode1, getBarLayout(data1.lineIndex), {
    responsive: true,
  });
  Plotly.newPlot("bar2_content", barModel2, getBarLayout(data2.lineIndex), {
    responsive: true,
  });
  Plotly.newPlot("scatter1_content", scatterModel1, scatterLayout);
  Plotly.update("scatter1_content", scatterModel1, scatterModel1_update);
  Plotly.newPlot("scatter2_content", scatterModel2, scatterLayout);
  Plotly.update("scatter2_content", scatterModel2, scatterModel2_update);
}
