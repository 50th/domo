<template>
    <el-row>
        <el-col :span="24" style="text-align: center;">
            <div class="home-box">
                <h1>Domo</h1>
            </div>
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="6" :offset="6">
            <el-card style="margin-right: 25px;">
                <template #header>
                    <div style="text-align: center;">
                        <span>热门文章</span>
                    </div>
                </template>
                <div class="top-box">
                    <ul>
                        <li v-for="item in articleViewTopList" :key="item.id">
                            <span @click="router.push({ name: 'articleDetail', params: { id: item.id } })"
                                style="float: left;cursor: pointer;">
                                {{ item.title }}
                            </span>
                            <span style="float: right;">{{ item.view_count }}</span>
                        </li>
                    </ul>
                </div>
            </el-card>
        </el-col>
        <el-col :span="6">
            <el-card style="margin-left: 25px;">
                <template #header>
                    <div style="text-align: center;">
                        <span>热门下载</span>
                    </div>
                </template>
                <div class="top-box">
                    <ul>
                        <li v-for="item in fileDownloadTopList" :key="item.id">
                            <span style="float: left;">{{ item.filename }}</span>
                            <span style="float: right;">{{ item.download_count }}</span>
                        </li>
                    </ul>
                </div>
            </el-card>
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

import { getArticleViewTopApi } from '@/apis/articleApis';
import { getFileDownloadTopApi } from '@/apis/fileApis';
import type { ArticleInfo, FileInfo } from '@/interfaces';

const router = useRouter();

const articleViewTopList = ref<ArticleInfo[]>([]);

const getArticleViewTopList = async () => {
    const res = await getArticleViewTopApi();
    articleViewTopList.value = res.data.top_view_articles;
}

const fileDownloadTopList = ref<FileInfo[]>([]);

const getFileDownloadTopList = async () => {
    const res = await getFileDownloadTopApi();
    fileDownloadTopList.value = res.data.top_download_files;
}

onMounted(() => {
    getArticleViewTopList();
    getFileDownloadTopList();
})
</script>
<style scoped>
.el-card {
    opacity: 0.8;
}

.home-box {
    h1 {
        font-size: 3rem;
        /* color: rgb(218, 92, 223); */
        letter-spacing: -3px;
        text-shadow: 0px 1px 1px rgba(255, 255, 255, 0.6);
        position: relative;
        z-index: 3;
        margin: 0;
    }

    margin-top: 40px;
    margin-bottom: 80px;
    z-index: 1;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 2rem;
    /* box-shadow: 0px 0px 12px rgba(117, 122, 131, 0.20); */
}

.top-box {
    font-size: 1rem;
    /* font-family: "FangSong"; */

    ul {
        list-style: none;
        margin: 0;
        padding: 0;

        li {
            /* color: #6b531e; */
            min-height: 2rem;
        }
    }

}
</style>
