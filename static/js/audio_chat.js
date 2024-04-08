const recordButton = document.getElementById('record-button');
const soundWaveCanvas = document.getElementById('sound-wave');
const ctx = soundWaveCanvas.getContext('2d');

let isRecording = false;
let audioStream;
let mediaRecorder;

async function startRecording() {
  if (isRecording) return;
  isRecording = true;

  try {
    // Request audio input stream
    audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // Create MediaRecorder instance
    mediaRecorder = new MediaRecorder(audioStream);

    // Handle data available event (chunks of recorded audio)
    mediaRecorder.addEventListener('dataavailable', (event) => {
      console.log('Recording chunk:', event.data);
      // You can send event.data to your server or handle it as needed
    });

    // Update button text and start recording
    recordButton.textContent = 'Stop Recording';
    mediaRecorder.start();
  } catch (error) {
    console.error('Error starting recording:', error);
    isRecording = false;
  }

  // Start drawing the twisted arc
  drawTwistedArc();
}

function stopRecording() {
  if (!isRecording) return;
  isRecording = false;

  mediaRecorder.stop();
  audioStream.getTracks().forEach(track => track.stop());
  recordButton.textContent = 'Start Recording';

  // Stop drawing the twisted arc
  cancelAnimationFrame(animationId);
}

recordButton.addEventListener('click', () => {
  if (isRecording) {
    stopRecording();
  } else {
    startRecording();
  }
});

let angle = 0;
let animationId;

function drawTwistedArc() {
  const centerX = soundWaveCanvas.width / 2;
  const centerY = soundWaveCanvas.height / 2;
  const radius = 25;
  const amplitude = 30;

  ctx.clearRect(0, 0, soundWaveCanvas.width, soundWaveCanvas.height);

  ctx.beginPath();
  ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);

  for (let i = 0; i < Math.PI * 2; i += 0.01) {
    const x = centerX + Math.cos(i) * radius;
    const y = centerY + Math.sin(i) * radius + Math.sin(angle) * amplitude;
    angle += 0.07;
    ctx.lineTo(x, y);
  }

  ctx.strokeStyle = 'orange';
  ctx.lineWidth = 2;
  ctx.stroke();

  animationId = requestAnimationFrame(drawTwistedArc);
}

startRecording();