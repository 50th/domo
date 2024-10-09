import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { checkAccessApi } from '@/apis/authApis'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/About.vue')
    },
    {
      path: '/articles',
      name: 'articleList',
      component: () => import('@/views/Article/ArticleList.vue')
    },
    {
      path: '/articles/:id(\\d+)',
      name: 'articleDetail',
      component: () => import('@/views/Article/ArticleDetail.vue')
    },
    {
      path: '/articles/edit-article/:id(\\d+)',
      name: 'editArticle',
      component: () => import('@/views/Article/EditArticle.vue')
    },
    {
      path: '/articles/add-article',
      name: 'addArticle',
      component: () => import('@/views/Article/AddArticle.vue')
    },
    {
      path: '/files',
      name: 'fileList',
      component: () => import('@/views/File/FileList.vue')
    },
    {
      path: '/videos',
      name: 'videoList',
      component: () => import('@/views/Video/VideoList.vue')
    },
    {
      path: '/videos/:id(\\d+)',
      name: 'playVideo',
      component: () => import('@/views/Video/VideoPlay.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/UserLogin.vue')
    }
  ]
})

router.beforeEach((to, from) => {
  let user = useUserStore().getUser()
  if (user) {
    checkAccessApi(user.access).then((res) => {
      if (res.code == 1005) {
        useUserStore().setUser(null)
        user = null
      }
    })
  }

  if (to.name === 'login' && user) {
    return from
  }
})

export default router
