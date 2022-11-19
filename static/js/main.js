let doorHandle = document.querySelector(".door-handle")
let windowHandle = document.querySelector(".window-handle")
let doorIsOpened = false
doorHandle.addEventListener("click", (e)=>{
    document.querySelector(".door").classList.toggle("door-open")
    doorIsOpened = true
})
let eyes = document.querySelector(".eyes")
let eyelid = document.querySelectorAll(".eyelid")

function closeEyelid() {
    eyelid.forEach((oneEyelid)=>oneEyelid.classList.add("eyelid-close"))
    setTimeout(openEyelid, 150)
  }
function openEyelid() {
    eyelid.forEach((oneEyelid)=>oneEyelid.classList.remove("eyelid-close"))
  }

setInterval(closeEyelid, 3000);

function eyesBreathInhalation(){
    eyes.classList.add("eyes-breath")
    setTimeout(eyesBreathExhalation, 1500)
} 
function eyesBreathExhalation(){
    eyes.classList.remove("eyes-breath")
} 
setInterval(eyesBreathInhalation, 4000);
// const recorder = document.getElementById('recorder');
// const player = document.getElementById('player');
// let pause= document.getElementById('pause');
var recorder;
window.onload = function() {

    recordButton = document.getElementById('record');
    stopButton = document.getElementById('stop');
    // get audio stream from user's mic
    navigator.mediaDevices.getUserMedia({
            audio: true
        })
        .then(function(stream) {
            recordButton.disabled = false;
            stopButton.disabled = true;
            recordButton.addEventListener('click', startRecording);
            stopButton.addEventListener('click', stopRecording);
            var options = {
                mimeType: 'audio/webm'
            }
            recorder = new MediaRecorder(stream, options);
            recorder.addEventListener('dataavailable', onRecordingReady);
        }, function() {
            recordButton.disabled = true;
            stopButton.disabled = true;         
            $("#audioMediaNotAvailable").show();
        }); // if microphone is not connected
};
function startRecording() {
    recordButton.disabled = true;
    stopButton.disabled = false;
    document.querySelector(".door-window").classList.toggle("door-window-open")
    document.querySelector(".window-handle").classList.toggle("window-handle-open")
    recorder.start();
}
function stopRecording() {
    recordButton.disabled = false;
    stopButton.disabled = true;
    document.querySelector(".door-window").classList.toggle("door-window-open")
    document.querySelector(".window-handle").classList.toggle("window-handle-open")
    recorder.stop();
    $("#recording").hide();
    $("#processing").show();
}
var audioFile;
function onRecordingReady(e) {
    var audio = document.getElementById('audio');
    audioFile = e.data;
    //  var file = new File(e.data,"hello.wav");
    audio.src = URL.createObjectURL(e.data);
    audio.play();
}

// let micInput = document.querySelector(".mic-input")

// micInput.addEventListener("click", (e)=>{
//     micInput.classList.toggle("mic-input-active")
//     document.querySelector(".door-window").classList.toggle("door-window-open")
//     document.querySelector(".window-handle").classList.toggle("window-handle-open")
// })
// // pause.addEventListener("click", (e)=>{
// //     micInput.classList.toggle("mic-input-active")
// //     pause.classList.toggle("pause-input-active")
// //     micInput.pause()
// //     document.querySelector(".door-window").classList.toggle("door-window-open")
// //     document.querySelector(".window-handle").classList.toggle("window-handle-open")
// // })