<template>
    <div>
        <el-container>
            <el-header style="font-family: 'Georgia';font-weight:bold; font-size: x-large;">Voice Recognition (#^.^#)
            </el-header>
            <el-main>
                <el-row :gutter="20" type="flex" justify="center">
                    <el-col :span="7">
                        <el-row>
                            <div style="height: 30px"></div>
                        </el-row>
                        <!--<el-row>-->
                        <!--<el-col :span="17">-->
                        <!--<label class="audio-label"> Blob Content Size: </label>-->
                        <!--<label>{{b64Content}}</label>-->
                        <!--</el-col>-->
                        <!--</el-row>-->
                        <el-row>
                            <el-col :span="17">
                                <label class="audio-label">Recognized as: </label>
                                <el-row>
                                    <div style="height: 30px"></div>
                                </el-row>
                                <el-input
                                        size="large"
                                        placeholder="Waiting to recognize..."
                                        v-model="resultLabel"
                                        :disabled="true">
                                </el-input>
                            </el-col>
                        </el-row>
                        <el-row>
                            <div style="height: 50px"></div>
                        </el-row>
                        <el-row>
                            <el-col :span="4">
                                <el-button :type="recordStyle" @click="startRecord" icon="el-icon-caret-right" round>
                                    Record
                                </el-button>
                            </el-col>
                            <el-col :offset="6" :span="4">
                                <el-button type="success" @click="uploadAudio" icon="el-icon-check" round>
                                    Recognize
                                </el-button>
                            </el-col>
                        </el-row>
                        <el-row>
                            <div style="height: 30px"></div>
                        </el-row>
                        <el-row>
                            <audio :src="audioUrl" ref="audio" controls='controls'>
                            </audio>
                        </el-row>
                        <el-row>
                            <div style="height: 30px"></div>
                            <div><label class="audio-label">Audio recognized: </label><label
                                    class="result-label">{{recIndex}}</label></div>
                        </el-row>
                        <el-row>
                            <a :href="audioUrl" download></a>
                        </el-row>
                        <el-row>
                            <div style="height: 30px"></div>
                        </el-row>
                    </el-col>
                    <el-col :span="10">
                        <el-row>
                            <div style="height: 30px"></div>
                        </el-row>
                        <el-row>
                            <div class="board">
                                <canvas id="analyser" width="1024" height="360"></canvas>
                            </div>
                        </el-row>
                        <el-row>
                            <div style="height: 30px"></div>
                        </el-row>
                        <el-row>
                            <div class="board">
                                <canvas ref="canvas" width="1024" height="360"></canvas>
                            </div>
                        </el-row>
                    </el-col>
                </el-row>
            </el-main>
            <el-footer style="font-family: 'Times New Roman'">
                ©Copyright: JingyuanLiu -- Course Project for Digital Signal Processing(COMP130139.01) @Fudan University 2018.6 Summer
            </el-footer>
        </el-container>
    </div>
</template>

<script>
    import InitRecorder from '../recorderjs/recorder';
    import ElCol from "element-ui/packages/col/src/col";
    import ElRadio from "../../node_modules/element-ui/packages/radio/src/radio.vue";

    let audioContext = new AudioContext();
    let inputPoint = null,
        analyserNode = null;
    let rafID = null;
    let analyserContext = null;
    let canvasWidth, canvasHeight;


    export default {
        components: {
            ElRadio,
            ElCol
        },
        name: 'Recorder',
        data() {
            return {
                'audioRecorder': null,
                'audioUrl': null,
                'waveBuf': null,
                'recIndex': 0,
                'isRecording': false,
                'isAnalysing': false,
                'resultLabel': null,
                'curAudioBlob': null,
                'b64Content': null,
            }
        },

        methods: {
            updateAnalysers(time) {
                // draw the analyser here
                if (!analyserContext) {
                    let canvas = document.getElementById("analyser");
                    canvasWidth = canvas.width;
                    canvasHeight = canvas.height;
                    analyserContext = canvas.getContext('2d');
                }

                // analyzer draw code here
                {
                    let SPACING = 3;
                    let BAR_WIDTH = 1;
                    let numBars = Math.round(canvasWidth / SPACING);
                    let freqByteData = new Uint8Array(analyserNode.frequencyBinCount);

                    analyserNode.getByteFrequencyData(freqByteData);

                    analyserContext.clearRect(0, 0, canvasWidth, canvasHeight);
                    analyserContext.fillStyle = '#F6D565';
                    analyserContext.lineCap = 'round';
                    let multiplier = analyserNode.frequencyBinCount / numBars;

                    // Draw rectangle for each frequency bin.
                    for (let i = 0; i < numBars; ++i) {
                        let magnitude = 0;
                        let offset = Math.floor(i * multiplier);
                        // gotta sum/average the block, or we miss narrow-bandwidth spikes
                        for (let j = 0; j < multiplier; j++)
                            magnitude += freqByteData[offset + j];
                        magnitude = magnitude / multiplier;
                        let magnitude2 = freqByteData[i * multiplier];
                        analyserContext.fillStyle = "hsl( " + Math.round((i * 360) / numBars) + ", 100%, 50%)";
                        analyserContext.fillRect(i * SPACING, canvasHeight, BAR_WIDTH, -magnitude);
                    }
                }

                rafID = window.requestAnimationFrame(this.updateAnalysers);
            },
            drawBuffer(width, height, context, data) {
                let step = Math.ceil(data.length / width);
                let amp = height / 2;
                context.fillStyle = "silver";
                context.clearRect(0, 0, width, height);
                for (let i = 0; i < width; i++) {
                    let min = 1.0;
                    let max = -1.0;
                    for (let j = 0; j < step; j++) {
                        let datum = data[(i * step) + j];
                        if (datum < min)
                            min = datum;
                        if (datum > max)
                            max = datum;
                    }
                    context.fillRect(i, (1 + min) * amp, 1, Math.max(1, (max - min) * amp));
                }
            },

            gotBuffers(buffers) {
                // sync with display board here.
                this.waveBuf = buffers[0];

                let canvas = this.$refs.canvas;
                this.drawBuffer(canvas.width, canvas.height, canvas.getContext('2d'), this.waveBuf);

                // the ONLY time gotBuffers is called is right after a new recording is completed -
                // so here's where we should set up the download.
                // set up upload here
                this.audioRecorder.exportWAV(this.doneEncoding);
            },

            doneEncoding(blob) {
                // deal with blob, upload to server
                this.curAudioBlob = blob;
                this.audioUrl = (window.URL || window.webkitURL).createObjectURL(blob);

                // For test b64 encode

            },

            toggleRecording() {
                if (this.isRecording) {
                    // stop recording
                    console.log('Recording stopped.');
                    this.audioRecorder.stop();

                    // deal with buff, set up callback function
                    this.audioRecorder.getBuffers(this.gotBuffers);
                } else {
                    // start recording
                    console.log('Recording started.');
                    if (!this.audioRecorder)
                        return;
                    // e.classList.add("recording");
                    this.resultLabel = null;
                    this.audioRecorder.clear();
                    this.audioRecorder.record();
                }
                this.isRecording = !this.isRecording;
            },

            gotStream(stream) {
                // GainNode, control volume
                inputPoint = audioContext.createGain();

                audioContext.createMediaStreamSource(stream).connect(inputPoint);

                // create analyser node
                if (!analyserNode) {
                    analyserNode = audioContext.createAnalyser();
                    analyserNode.fftSize = 2048;
                    inputPoint.connect(analyserNode);
                }

                this.audioRecorder = new Recorder(inputPoint);

                let zeroGain = audioContext.createGain();
                zeroGain.gain.value = 0.0;
                inputPoint.connect(zeroGain);
                zeroGain.connect(audioContext.destination);

                // draw analyser here
                this.updateAnalysers();
            },

            startRecord() {
                this.toggleRecording();

                setTimeout(this.toggleRecording, 2002);
            },
            uploadAudio() {
                // check if the first time
                if (!this.curAudioBlob) {
                    this.$notify.error({
                        tile: 'Error',
                        message: 'No audio recorded now.'
                    });
                    return;
                }

                // upload and analyse
                this.isAnalysing = true;

                var reader = new FileReader();
                reader.readAsDataURL(this.curAudioBlob);
                reader.onloadend = () => {
                    this.b64Content = reader.result;

                    //this.$http.post('http://localhost:5000/api', this.b64Content).then(
                    this.$http.post('/api', this.b64Content).then(
                        response => {
                            this.isAnalysing = false;
                            this.resultLabel = response.body['result'];
                            this.recIndex++;
                        },
                        response => {
                            console.log('Analysis failed.');
                            console.log(response.status);
                        }
                    );
                };


//                setTimeout(() => {
//                    this.isAnalysing = false;
//                    this.resultLabel = 'xxx';
//                    this.recIndex++;
//
//                }, 2000);
            }
        },
        computed: {
            recordStyle() {
                return this.isRecording ? 'warning' : 'primary';
            }
        },
        created:

            function () {
                // initRecorder
                InitRecorder(window);

                // initAudio
                if (!navigator.getUserMedia)
                    navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
                if (!navigator.cancelAnimationFrame)
                    navigator.cancelAnimationFrame = navigator.webkitCancelAnimationFrame || navigator.mozCancelAnimationFrame;
                if (!navigator.requestAnimationFrame)
                    navigator.requestAnimationFrame = navigator.webkitRequestAnimationFrame || navigator.mozRequestAnimationFrame;

                navigator.getUserMedia(
                    {
                        "audio": {
                            "mandatory": {
                                "googEchoCancellation": "false",
                                "googAutoGainControl": "false",
                                "googNoiseSuppression": "false",
                                "googHighpassFilter": "false"
                            },
                            "optional": []
                        },
                    }, this.gotStream, function (e) {
                        alert('Error getting audio');
                        console.log(e);
                    });

            }
    }

</script>
<style>


    canvas {
        display: inline-block;
        background: #202020;
        width: 95%;
        height: 45%;
        box-shadow: 0px 0px 10px blue;
    }

    .el-header {
        background-color: #FF9999;
        color: #fff;
        text-align: center;
        line-height: 60px;
    }

    .el-footer {
        width: 98%;
        background-color: #fff;
        color: #848484;
        text-align: center;
        line-height: 60px;
        position: fixed;
        bottom: 20px;
    }

    .audio-label {
        font-size: 18px;
        /*font-style: italic;*/
        font-weight: bold;
        /*text-align: justify;*/
        line-height: 20px;
        color: #155161;
        font-family: Helvetica;
    }

    .result-label {
        font-size: 18px;
        /*font-style: italic;*/
        font-weight: bold;
        /*text-align: justify;*/
        line-height: 20px;
        color: #7DB9CC;
    }

</style>
