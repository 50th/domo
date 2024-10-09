import { defineStore } from 'pinia'
import type { UserInfo } from '@/interfaces'

export const useUserStore = defineStore('user', {
  state: () => ({ userInfo: null as UserInfo | null }),
  actions: {
    setUser(userInfo: UserInfo | null) {
      this.userInfo = userInfo
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
    },
    getUser() {
      if (!this.userInfo) {
        const userInfo = localStorage.getItem('userInfo')
        if (userInfo) {
          this.userInfo = JSON.parse(userInfo)
        }
      }
      return this.userInfo
    },
    delUser() {
      this.userInfo = null
      localStorage.removeItem('userInfo')
    }
  }
})
