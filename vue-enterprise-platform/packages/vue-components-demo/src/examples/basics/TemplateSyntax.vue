<template>
  <DemoContainer
    title="模板语法"
    description="Vue模板语法 - 插值、指令、事件处理"
  >
    <el-space direction="vertical" :size="20" style="width: 100%">
      <!-- 文本插值 -->
      <el-card header="文本插值 - {{ }}">
        <p>消息: {{ message }}</p>
        <p>HTML内容: <span v-html="rawHtml"></span></p>
        <el-input v-model="message" placeholder="修改消息" />
      </el-card>

      <!-- 指令 -->
      <el-card header="指令 - v-bind, v-on">
        <p>动态属性绑定:</p>
        <el-button :type="buttonType" @click="changeButtonType">
          {{ buttonType }} 按钮
        </el-button>
        <p style="margin-top: 16px">点击次数: {{ clickCount }}</p>
      </el-card>

      <!-- 表达式 -->
      <el-card header="JavaScript表达式">
        <p>数字: {{ number }}</p>
        <p>数字 + 1 = {{ number + 1 }}</p>
        <p>三元表达式: {{ isOk ? 'YES' : 'NO' }}</p>
        <p>方法调用: {{ reverseMessage() }}</p>
        <el-button @click="number++">增加数字</el-button>
        <el-button @click="isOk = !isOk">切换状态</el-button>
      </el-card>

      <!-- 事件处理 -->
      <el-card header="事件处理">
        <el-space>
          <el-button @click="handleClick">普通点击</el-button>
          <el-button @click="handleClickWithArg('参数')">带参数点击</el-button>
          <el-button @click.prevent="handlePrevent">阻止默认行为</el-button>
          <el-button @click.stop="handleStop">阻止冒泡</el-button>
        </el-space>
        <p style="margin-top: 16px">事件信息: {{ eventInfo }}</p>
      </el-card>
    </el-space>
  </DemoContainer>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import DemoContainer from '@/components/DemoContainer.vue'

const message = ref('Hello Vue 3!')
const rawHtml = ref('<span style="color: red">红色文本</span>')
const buttonType = ref<any>('primary')
const clickCount = ref(0)
const number = ref(10)
const isOk = ref(true)
const eventInfo = ref('')

const changeButtonType = () => {
  const types = ['primary', 'success', 'warning', 'danger', 'info']
  const currentIndex = types.indexOf(buttonType.value)
  buttonType.value = types[(currentIndex + 1) % types.length]
  clickCount.value++
}

const reverseMessage = () => {
  return message.value.split('').reverse().join('')
}

const handleClick = () => {
  eventInfo.value = '普通点击事件触发'
}

const handleClickWithArg = (arg: string) => {
  eventInfo.value = `带参数点击: ${arg}`
}

const handlePrevent = (event: Event) => {
  eventInfo.value = '阻止了默认行为'
}

const handleStop = (event: Event) => {
  eventInfo.value = '阻止了事件冒泡'
}
</script>
