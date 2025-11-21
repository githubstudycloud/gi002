<template>
  <DemoContainer
    title="响应式基础"
    description="探究Vue 3的响应式系统 - ref, reactive, computed, watch"
  >
    <el-space direction="vertical" :size="20" style="width: 100%">
      <!-- ref示例 -->
      <el-card header="ref - 基本类型响应式">
        <p>计数器: {{ count }}</p>
        <el-button @click="count++">增加</el-button>
        <el-button @click="count--">减少</el-button>
        <el-button @click="count = 0">重置</el-button>

        <CodeBlock
          :code="`const count = ref(0)\n// 使用: count.value++\n// 模板中自动解包: {{ count }}`"
          language="TypeScript"
        />
      </el-card>

      <!-- reactive示例 -->
      <el-card header="reactive - 对象响应式">
        <p>用户信息:</p>
        <ul>
          <li>姓名: {{ user.name }}</li>
          <li>年龄: {{ user.age }}</li>
          <li>邮箱: {{ user.email }}</li>
        </ul>
        <el-button @click="user.age++">增加年龄</el-button>
        <el-button @click="updateUser">更新信息</el-button>

        <CodeBlock
          :code="`const user = reactive({\n  name: '张三',\n  age: 25,\n  email: 'zhang@example.com'\n})\n// 使用: user.age++`"
          language="TypeScript"
        />
      </el-card>

      <!-- computed示例 -->
      <el-card header="computed - 计算属性">
        <p>原价: ¥{{ price }}</p>
        <p>折扣: {{ discount }}%</p>
        <p>最终价格: ¥{{ finalPrice }}</p>
        <el-slider v-model="discount" :min="0" :max="100" />

        <CodeBlock
          :code="`const finalPrice = computed(() => {\n  return (price.value * (100 - discount.value) / 100).toFixed(2)\n})`"
          language="TypeScript"
        />
      </el-card>

      <!-- watch示例 -->
      <el-card header="watch - 侦听器">
        <p>输入内容: {{ input }}</p>
        <el-input v-model="input" placeholder="输入内容，触发watch" />
        <p>变化次数: {{ changeCount }}</p>
        <p>上次变化时间: {{ lastChangeTime }}</p>

        <CodeBlock
          :code="`watch(input, (newVal, oldVal) => {\n  console.log(\`从 \${oldVal} 变为 \${newVal}\`)\n  changeCount.value++\n  lastChangeTime.value = new Date().toLocaleTimeString()\n})`"
          language="TypeScript"
        />
      </el-card>

      <!-- watchEffect示例 -->
      <el-card header="watchEffect - 自动追踪依赖">
        <p>名字: <el-input v-model="firstName" style="width: 150px" /></p>
        <p>姓氏: <el-input v-model="lastName" style="width: 150px" /></p>
        <p>完整姓名: {{ fullName }}</p>

        <CodeBlock
          :code="`watchEffect(() => {\n  fullName.value = \`\${firstName.value} \${lastName.value}\`\n  console.log('姓名更新:', fullName.value)\n})`"
          language="TypeScript"
        />
      </el-card>
    </el-space>
  </DemoContainer>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, watchEffect } from 'vue'
import DemoContainer from '@/components/DemoContainer.vue'
import CodeBlock from '@/components/CodeBlock.vue'

// ref示例
const count = ref(0)

// reactive示例
const user = reactive({
  name: '张三',
  age: 25,
  email: 'zhang@example.com'
})

const updateUser = () => {
  user.name = '李四'
  user.age = 30
  user.email = 'li@example.com'
}

// computed示例
const price = ref(100)
const discount = ref(20)
const finalPrice = computed(() => {
  return (price.value * (100 - discount.value) / 100).toFixed(2)
})

// watch示例
const input = ref('')
const changeCount = ref(0)
const lastChangeTime = ref('')

watch(input, (newVal, oldVal) => {
  console.log(`从 ${oldVal} 变为 ${newVal}`)
  changeCount.value++
  lastChangeTime.value = new Date().toLocaleTimeString()
})

// watchEffect示例
const firstName = ref('三')
const lastName = ref('张')
const fullName = ref('')

watchEffect(() => {
  fullName.value = `${lastName.value}${firstName.value}`
  console.log('姓名更新:', fullName.value)
})
</script>

<style lang="scss" scoped>
ul {
  list-style: none;
  padding: 0;

  li {
    padding: 4px 0;
  }
}
</style>
