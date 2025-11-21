<template>
  <div id="micro-app-container" class="micro-app-container"></div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

onMounted(() => {
  console.log('微应用容器已挂载')
})
</script>

<style lang="scss" scoped>
.micro-app-container {
  width: 100%;
  min-height: 500px;
}
</style>
