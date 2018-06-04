<template>
  <div>
    <recorder>
    </recorder>
  </div>
</template>

<script>
  import ElCol from "element-ui/packages/col/src/col";
  import Recorder from './Recorder.vue'


  export default {
    components: {
      ElCol,
      Recorder
    },
    name: 'MainApp',
    data() {
      return {
        "status": "init",
//        "isPlaying": false,
        'isRecording': false,
        'isAnalysing': false,
        // init, recording, complete

      }
    },
  }
</script>
