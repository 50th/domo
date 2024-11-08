<template>
    <el-row>
        <el-col :span="24">
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
                                style="float: left; cursor: pointer;">
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
                            <span style="float: left; cursor: pointer;" @click="downloadFileHandler(item, userInfo)">
                                {{ item.filename }}
                            </span>
                            <span style="float: right;">{{ item.download_count }}</span>
                            <el-progress v-show="item.downloading" style="padding: 4px;" :text-inside="true"
                                :stroke-width="15" :percentage="item.downloadingProgress" />
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

import type { ArticleInfo, FileInfo, UserInfo } from '@/interfaces';
import { getArticleViewTopApi } from '@/apis/articleApis';
import { getFileDownloadTopApi } from '@/apis/fileApis';
import { downloadFileHandler } from '@/utils/downloadFile';
import { useUserStore } from '@/stores/user';

const router = useRouter();
const user = useUserStore();
const userInfo = ref<UserInfo | null>(user.getUser());
const articleViewTopList = ref<ArticleInfo[]>([]);
const fileDownloadTopList = ref<FileInfo[]>([]);

const getArticleViewTopList = async () => {
    const res = await getArticleViewTopApi();
    articleViewTopList.value = res.data.top_view_articles;
}

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
    text-align: center;
    text-shadow: 0px 1px 1px rgba(255, 255, 255, 0.6);

    h1 {
        margin-top: 10px;
        font-size: 3rem;
        color: #7795f0;
    }
}

.top-box {
    font-size: 1rem;

    ul {
        list-style: none;
        margin: 0;
        padding: 0;

        li {
            min-height: 2rem;
        }
    }

}
</style>
