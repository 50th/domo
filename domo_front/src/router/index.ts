import { createRouter, createWebHistory, type RouteRecordName } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { checkAccessApi } from '@/apis/authApis'

const NeedLoginRoutes: RouteRecordName[] = [
  'editArticle',
  'addArticle',
  'tool',
  'videoList',
  'playVideo'
]

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
      name: 'wallpaperList',
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

router.beforeEach(async (to, from) => {
  let user = useUserStore().getUser()
  if (user) {
    await checkAccessApi(user.access)
      .then((res) => {
        if (res.code === 1003 || res.code === 1005) {
          useUserStore().setUser(null)
          user = null
        }
      })
      .catch((err) => {
        useUserStore().setUser(null)
        user = null
      })
  }

  if (to.name === 'login' && user) {
    return { name: 'home' }
  }

  if (!user && to.name && NeedLoginRoutes.includes(to.name as RouteRecordName)) {
    return { name: 'home' }
  }
})

export default router
