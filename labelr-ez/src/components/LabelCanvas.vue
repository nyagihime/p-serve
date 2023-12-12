<script setup lang="ts">
import { ref, onMounted, type PropType } from 'vue'
import dayjs from 'dayjs'

const previewCanvas = ref<HTMLCanvasElement | null>(null)
const labelImgB64 = ref<string | null>(null)

export interface LabelImageData {
  image: string
  width: number
  height: number
}

export interface LabelSizeOverride {
  width: number
  height: number
}

const props = defineProps({
  title: {
    type: String,
    default: '',
  },
  summary: {
    type: String,
    default: '',
  },
  labelSize: {
    type: Object as PropType<LabelSizeOverride>,
    default: () => ({
      width: 696,
      height: 320,
    })
  }
})

const emit = defineEmits([
  'update:labelImageData',
])

const generateLabel = () => {
  const printPadding = 20
  const ctx = previewCanvas.value?.getContext('2d')
  if (previewCanvas.value && ctx) {
    // init
    ctx.rect(0, 0, ctx.canvas.width, ctx.canvas.height)
    ctx.fillStyle = 'white'
    ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height)

    // 座標リセット
    ctx.beginPath()
    // fill の色
    ctx.fillStyle = 'black'

    // タイトル
    const titleSize = ctx.measureText(props.title)
    ctx.font = '400 64px "IBM Plex Sans JP"'
    ctx.fillText(props.title, printPadding, 90 + titleSize.actualBoundingBoxDescent)

    // サマリ
    ctx.font = '400 32px "IBM Plex Sans JP"'
    // 改行コードで分割して描画
    for (let lines = props.summary.split('\n'), len = lines.length, i = 0; i < len; i++) {
      const line = lines[i]
      const lineSize = ctx.measureText(line)

      ctx.fillText(
        line,
        printPadding,
        150 + lineSize.actualBoundingBoxDescent + (i * 30)
      )
    }


    // 印刷日
    ctx.font = '200 24px "IBM Plex Sans JP"'
    const printDate = `PRINTED: ${dayjs().format('YYYY/MM/DD HH:mm:ss')}`
    const printDateSize = ctx.measureText(printDate)
    ctx.fillText(
      printDate,
      ctx.canvas.width - printDateSize.width - printPadding,
      ctx.canvas.height - 10 - printPadding
    )

    // canvas から画像を生成
    labelImgB64.value = previewCanvas.value.toDataURL('image/png')

    // emit
    const imageData: LabelImageData = {
      image: labelImgB64.value,
      width: ctx.canvas.width,
      height: ctx.canvas.height,
    }

    emit('update:labelImageData', imageData)
  }
}

onMounted(() => {
  // webfont ロード終わるまでまつ
  setInterval(() => {
    generateLabel()
  }, 1000)
})

</script>

<template>
    <div class="label-canvas">
        <canvas
          ref="previewCanvas"
          class="workspace"
          :width="labelSize.width"
          :height="labelSize.height"
        />

        <img
          v-if="labelImgB64"
          class="label-image-preview"
          :src="labelImgB64"
          alt="label preview"
        >
</div>
</template>


<style scoped lang="scss">
.label-canvas {
  max-width: 100%;
  .workspace {
    display: none;
  }

  .label-image-preview {
    max-width: 100%;
    max-height: auto;
  }
}
</style>
