import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * 用户状态管理
 */
export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref<any>(null)

  const isLogin = computed(() => !!token.value)

  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUserInfo = (info: any) => {
    userInfo.value = info
  }

  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    userInfo,
    isLogin,
    setToken,
    setUserInfo,
    logout
  }
})

/**
 * 应用状态管理
 */
export const useAppStore = defineStore('app', () => {
  const collapsed = ref(false)
  const loading = ref(false)

  const toggleCollapsed = () => {
    collapsed.value = !collapsed.value
  }

  const setLoading = (status: boolean) => {
    loading.value = status
  }

  return {
    collapsed,
    loading,
    toggleCollapsed,
    setLoading
  }
})
