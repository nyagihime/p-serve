<script setup lang="ts">
import type { LabelImageData } from '@/components/LabelCanvas.vue';
import { ref } from 'vue'
import axios from 'axios'

const itemTitle = ref('')
const itemSummary = ref('')

const imageData = ref<LabelImageData>({
  image: '',
  width: 0,
  height: 0,
})

const printRequest = async () => {
  const res = await axios.post('http://p-serve.local:8080/api/print', {
    size: 62,
    image: imageData.value.image,
  }, {
    headers: {
      'Content-Type': 'multipart/form-data',
    }
  }
  )
  console.log(res)
}
</script>

<template>
    <div class="home-view">
        <h1>labelr-ez</h1>
        <label-canvas
          :title="itemTitle"
          :summary="itemSummary"
          @update:labelImageData="imageData = $event"
        />

        <div class="form">
            <label for="itemTitle">name</label>
            <input
              type="text"
              id="itemTitle"
              v-model="itemTitle"
            >

            <label for="itemSummary">summary</label>
            <textarea
              id="itemSummary"
              cols="30"
              rows="5"
              v-model="itemSummary"
            ></textarea>
            <button @click="printRequest">PRINT</button>
        </div>
    </div>
</template>

<style scoped>
.home-view {
    width: 320px;
    margin: auto;

    h1 {
      font-weight: 100;
      border-bottom: 1px solid var(--color-fg);
    }

    .form {
        padding: 1rem 0;
        display: flex;
        flex-direction: column;
        gap: 1rem;

        input,
        textarea {
          padding: 5px;
          font-size: 1.4rem;
          border: 1px solid var(--color-gray);
          border-radius: 1px;
        }

        button {
          padding: 5px;
          font-size: 1.4rem;
          border: 1px solid  var(--color-gray);
          border-radius: 1px;
          cursor: pointer;
          background-color:  var(--color-blue);
          color: var(--color-fg);
        }
    }
}
</style>
