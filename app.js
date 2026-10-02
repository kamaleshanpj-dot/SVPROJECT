const form=document.getElementById("commandForm");
const input=document.getElementById("commandInput");
const responseBox=document.getElementById("response");
const statusBox=document.getElementById("status");
const micButton=document.getElementById("micButton");
const backendStatus=document.getElementById("backendStatus");

fetch("/api/health").then(r=>{if(!r.ok)throw Error();return r.json()})
 .then(()=>backendStatus.textContent="Backend online")
 .catch(()=>backendStatus.textContent="Backend unavailable");

function speak(text){
 if(!("speechSynthesis" in window))return;
 window.speechSynthesis.cancel();
 const utterance=new SpeechSynthesisUtterance(text);
 utterance.rate=1;
 window.speechSynthesis.speak(utterance);
}
async function sendCommand(command){
 const value=command.trim();
 if(!value)return;
 statusBox.textContent="Processing your command…";
 responseBox.textContent="Please wait…";
 try{
  const res=await fetch("/api/command",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({command:value})});
  const data=await res.json();
  if(!res.ok)throw Error(data.response||"Request failed.");
  responseBox.textContent=data.response||"No response received.";
  statusBox.textContent=data.status==="error"?"Please try again":"Response ready";
  if(data.status!=="error")speak(data.response||"");
  if(data.action==="redirect"&&["https://www.youtube.com","https://www.google.com"].includes(data.url))window.open(data.url,"_blank","noopener");
  if(data.assistant_name)document.title=data.assistant_name+" | Voice & Text Assistant";
 }catch(error){
  responseBox.textContent=error.message||"Unable to contact the backend.";
  statusBox.textContent="Connection error";
 }
}
form.addEventListener("submit",event=>{event.preventDefault();sendCommand(input.value);input.value="";});
document.querySelectorAll("[data-command]").forEach(button=>button.addEventListener("click",()=>sendCommand(button.dataset.command)));
micButton.addEventListener("click",()=>{
 const Recognition=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!Recognition){statusBox.textContent="Speech recognition is not supported in this browser.";return;}
 const recognition=new Recognition();
 recognition.lang="en-IN";recognition.interimResults=false;
 recognition.onstart=()=>statusBox.textContent="Listening…";
 recognition.onresult=event=>{const transcript=event.results[0][0].transcript;input.value=transcript;sendCommand(transcript);};
 recognition.onerror=event=>statusBox.textContent="Microphone: "+event.error;
 recognition.onend=()=>{if(statusBox.textContent==="Listening…")statusBox.textContent="Ready when you are";};
 recognition.start();
});
