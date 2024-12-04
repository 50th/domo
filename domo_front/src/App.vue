<template>
  <el-container>
    <el-header>
      <el-menu :ellipsis="false" mode="horizontal" @select="handleSelect">
        <el-menu-item index="home">
          <span style="font-weight: bold; color: #d95f5f">Domo</span>
        </el-menu-item>
        <el-menu-item index="articleList">
          <span>文章</span>
        </el-menu-item>
        <el-menu-item index="fileList">
          <span>文件</span>
        </el-menu-item>
        <el-menu-item index="wallpaperList">
          <span>壁纸</span>
        </el-menu-item>
        <el-menu-item v-if="userInfo && userInfo.is_superuser" index="videoList">
          <span>视频</span>
        </el-menu-item>
        <el-menu-item v-if="userInfo && userInfo.is_superuser" index="tool">
          <span>工具</span>
        </el-menu-item>
        <el-menu-item index="about">
          <span>关于</span>
        </el-menu-item>
        <div class="flex-grow" />
        <!-- 第三方访问计数 -->
        <!-- <el-menu-item>
          <img src="https://count.getloli.com/@domo-app?theme=sketch-2" alt="domo-app" />
        </el-menu-item> -->
        <el-menu-item v-if="!userInfo" index="login">登录</el-menu-item>
        <el-menu-item v-else>
          <el-popconfirm title="确认登出吗？" confirm-button-text="确认" cancel-button-text="取消" @confirm="logout">
            <template #reference>
              <el-button text>{{ userInfo.username }}</el-button>
            </template>
          </el-popconfirm>
        </el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <RouterView />
    </el-main>
  </el-container>
  <el-backtop :right="100" :bottom="100" />
</template>
<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { RouterView, useRouter } from 'vue-router';
import { useUserStore } from './stores/user';
import type { UserInfo } from '@/interfaces';

const router = useRouter();
const user = useUserStore();
const userInfo = ref<UserInfo | null>(user.getUser());

const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
  console.log(userInfo);
  router.push({ name: key });
}

const logout = (e: MouseEvent) => {
  console.log('logout');
  if (userInfo.value) {
    user.delUser();
    userInfo.value = null;
    // router.push({name: 'index'});
    window.location.reload();
  }
}

watch(user, async (newValue, oldValue) => {
  userInfo.value = user.getUser();
})

onMounted(() => { })

</script>
<style>
@font-face {
  font-family: 'Harmony_Light';
  src: url('https://cdn.jsdelivr.net/gh/50th/resources/HarmonyOS_Sans_SC_Light.woff2') format('woff2'),
    url('@/assets/fonts/HarmonyOS_Sans_SC_Light.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
}

* {
  font-family: 'Harmony_Light', sans-serif;
}

body {
  margin: 0;
  /* 加载背景图 */
  /* background-image: url(./assets/background_img.jpg); */
  /* 背景图垂直、水平均居中 */
  /* background-position: center center; */
  /* 背景图不平铺 */
  /* background-repeat: no-repeat; */
  /* 当内容高度大于图片高度时，背景图像的位置相对于viewport固定 */
  /* background-attachment: fixed; */
  /* 让背景图基于容器大小伸缩 */
  /* background-size: cover; */
  /* 设置背景颜色，背景图加载过程中会显示背景色 */
  /* background-color: rgb(235, 243, 241); */
}

.el-header {
  padding: 0;
  width: 50%;
  margin: auto;

  .el-menu {
    /* --el-menu-text-color: #57d786; */
    /* --el-menu-bg-color: #dff1ec94; */
    /* --el-menu-hover-text-color: #44bd70; */
    --el-menu-hover-bg-color: None;
    /* --el-menu-active-color: #44bd70; */
    /* padding: 0px !important; */
    border-bottom: none;

    .flex-grow {
      flex-grow: 1;
    }
  }
}

</style>
