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

const recorder = document.getElementById('recorder');
const player = document.getElementById('player');





let micInput = document.querySelector(".mic-input")
micInput.addEventListener("click", (e)=>{
    micInput.classList.toggle("mic-input-active")
    document.querySelector(".door-window").classList.toggle("door-window-open")
    document.querySelector(".window-handle").classList.toggle("window-handle-open")
})