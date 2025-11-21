<template>
  <div class="code-block">
    <div class="code-header">
      <span>{{ language }}</span>
      <el-button size="small" @click="copyCode">
        <el-icon><DocumentCopy /></el-icon>
        复制代码
      </el-button>
    </div>
    <pre><code>{{ code }}</code></pre>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'

const props = defineProps<{
  code: string
  language?: string
}>()

const copyCode = () => {
  navigator.clipboard.writeText(props.code)
  ElMessage.success('代码已复制到剪贴板')
}
</script>

<style lang="scss" scoped>
.code-block {
  margin: 16px 0;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;

  .code-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 16px;
    background: #f5f7fa;
    border-bottom: 1px solid #dcdfe6;

    span {
      font-size: 12px;
      color: #909399;
      font-weight: 600;
    }
  }

  pre {
    margin: 0;
    padding: 16px;
    background: #282c34;
    overflow-x: auto;

    code {
      color: #abb2bf;
      font-family: 'Consolas', 'Monaco', 'Andale Mono', 'Ubuntu Mono', monospace;
      font-size: 14px;
      line-height: 1.5;
    }
  }
}
</style>
