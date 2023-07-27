const resultAudio = document.querySelector('#result');
const recordButton = document.querySelector('#record');
const stopButton = document.querySelector('#stop');
const submitButton = document.querySelector('#submit');

let recorder;
let audio;


recordButton.addEventListener('click', async () => {
    recordButton.disabled = true;
    stopButton.disabled = false;

    if (!recorder) {
        recorder = await recordAudio();
    }

    recorder.start();
    resultAudio.src = '';
});

stopButton.addEventListener('click', async () => {
    recordButton.disabled = false
    stopButton.disabled = true
    submitButton.disabled = false;
    audio = await recorder.stop();
});

submitButton.addEventListener('click', () => {
    submit();
    submitButton.disabled = true
});

const recordAudio = () => new Promise(async resolve => {
    const stream = await navigator.mediaDevices.getUserMedia(
        {audio: {sampleSize: 16, channelCount: 1, sampleRate: 24000}}
    );
    const mediaRecorder = new MediaRecorder(stream);
    let audioChunks = [];

    mediaRecorder.addEventListener('dataavailable', event => {
        audioChunks.push(event.data);
    });

    const start = () => {
        audioChunks = [];
        mediaRecorder.start();
    };

    const stop = () => new Promise(resolve => {
        mediaRecorder.addEventListener('stop', () => {
            const audioBlob = new Blob(audioChunks, {'type': 'audio/mp3; codecs=opus'});
            const audioUrl = URL.createObjectURL(audioBlob);
            resolve({audioChunks, audioBlob, audioUrl});
            resultAudio.src = audioUrl
        });
        mediaRecorder.stop();
    });

    resolve({start, stop});
});

const submit = () => {
    const reader = new FileReader();
    reader.readAsDataURL(audio.audioBlob);

    reader.onload = () => {
        const base64AudioMessage = reader.result.split(',')[1];

        fetch(endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrf},
            body: JSON.stringify({audio: base64AudioMessage})
        }).then(res => {
            if (res.status === 200) {
                alert('Successfully sent!')
            } else {
                alert('Something went wrong!')
            }
        });
    };
}
