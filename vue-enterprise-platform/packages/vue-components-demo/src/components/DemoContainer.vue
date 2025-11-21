<template>
  <div class="demo-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>{{ title }}</h2>
          <p v-if="description" class="description">{{ description }}</p>
        </div>
      </template>
      <slot></slot>
    </el-card>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description?: string
}>()
</script>

<style lang="scss" scoped>
.demo-container {
  .card-header {
    h2 {
      margin: 0 0 8px 0;
      font-size: 24px;
      color: #303133;
    }

    .description {
      margin: 0;
      color: #909399;
      font-size: 14px;
    }
  }
}
</style>
