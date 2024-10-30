import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { checkAccessApi } from '@/apis/authApis'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/AboutView.vue')
    },
    {
      path: '/articles',
      name: 'articleList',
      component: () => import('@/views/ArticleViews/ArticleList.vue')
    },
    {
      path: '/articles/:id(\\d+)',
      name: 'articleDetail',
      component: () => import('@/views/ArticleViews/ArticleDetail.vue')
    },
    {
      path: '/articles/edit-article/:id(\\d+)',
      name: 'editArticle',
      component: () => import('@/views/ArticleViews/EditArticle.vue')
    },
    {
      path: '/articles/add-article',
      name: 'addArticle',
      component: () => import('@/views/ArticleViews/AddArticle.vue')
    },
    {
      path: '/files',
      name: 'fileList',
      component: () => import('@/views/FileViews/FileList.vue')
    },
    {
      path: '/wallpapers',
      name: 'wallpaper',
      component: () => import('@/views/WallpaperView.vue')
    },
    {
      path: '/tools',
      name: 'tool',
      component: () => import('@/views/ToolView.vue')
    },
    {
      path: '/videos',
      name: 'videoList',
      component: () => import('@/views/VideoViews/VideoList.vue')
    },
    {
      path: '/videos/:id(\\d+)',
      name: 'playVideo',
      component: () => import('@/views/VideoViews/VideoPlay.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/UserLogin.vue')
    },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/views/NotFound.vue') }
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
  if (!user && (to.name === 'videoList' || to.name === 'playVideo' || to.name === 'tool')) {
    return { name: 'home' }
  }
})

export default router
