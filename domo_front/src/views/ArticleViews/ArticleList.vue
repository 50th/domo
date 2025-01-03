<template>
    <el-row>
        <el-col :span="3" :offset="6">
            <el-input v-model="searchVal" size="default" placeholder="搜索(标题和正文)" clearable
                @change="refreshArticleList" />
        </el-col>
        <el-col v-if="userInfo && userInfo.is_superuser" :span="3" :offset="1">
            <el-button size="default" type="primary" plain round text @click="router.push({ name: 'addArticle' })">
                添加文章
            </el-button>
            <el-upload v-if="userInfo.is_superuser" style="display: inline; margin-left: 12px;" :show-file-list="false"
                :action="`${baseUrl}/api-article/article-file/`"
                :headers="userInfo ? { Authorization: `Bearer ${userInfo.access}` } : {}" name="article_file"
                accept=".md" :on-success="afterUploadArticle">
                <el-button size="default" type="primary" text plain round>上传文章</el-button>
            </el-upload>
        </el-col>
    </el-row>

    <el-row v-for="article in articleList" :key="article.id">
        <el-col :span="12" :offset="6">
            <el-card shadow="never" style="border-style: none;" body-class="article-card"
                @click="goArticleDetail(article.id)">
                <span class="article-title">{{ article.title }}</span>
                <!-- <span>{{ article.view_count }}</span> -->
                <span class="article-time">{{ article.last_edit_time }}</span>
            </el-card>
        </el-col>
    </el-row>

    <el-row v-if="articleList.length > 0" style="margin-top: 15px;">
        <el-col :span="10" :offset="7">
            <el-pagination style="justify-content: center;" layout="prev, pager, next" :page-size="pageSize"
                :pager-count="5" :total="articleCount" @current-change="handleCurrentChange" />
        </el-col>
    </el-row>
    <el-row v-else>
        <el-empty description="没有文章" />
    </el-row>


</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { UploadFile, UploadFiles } from 'element-plus'

import { baseUrl } from '@/utils/baseUrl'
import { useUserStore } from '@/stores/user';
import { getArticleListApi } from '@/apis/articleApis';
import type { ArticleInfo, UserInfo } from '@/interfaces';

const router = useRouter();

const user = useUserStore();
const userInfo = ref<UserInfo | null>(user.getUser());

const articleList = ref<ArticleInfo[]>([]);
const articleCount = ref<number>(0);
const searchVal = ref<string>('');

let currentPage = 1;
const pageSize = 10;

const afterUploadArticle = (response: any, uploadFile: UploadFile, uploadFiles: UploadFiles) => {
    if (response.code == 0) {
        ElMessage.success('上传成功');
        currentPage = 1;
        refreshArticleList();
    } else {
        ElMessage.error('上传失败：' + response.msg);
        if ([1003, 1004, 1005].indexOf(response.code) >= 0) {
            user.setUser(null);
        }
    }
}

/**
 * 请求文章列表
 */
const refreshArticleList = () => {
    getArticleListApi({ page_num: currentPage, page_size: pageSize, search: searchVal.value }).then(res => {
        if (res.code == 0) {
            articleList.value = res.data.results;
            articleCount.value = res.data.count;
        }
    });
}

const handleCurrentChange = (val: number) => {
    currentPage = val;
    refreshArticleList()
}

const goArticleDetail = (articleId: number) => {
    // console.log('跳转文章详情：', articleId);
    router.push({
        name: 'articleDetail',
        params: { id: articleId },
    })
}

onMounted(async () => {
    refreshArticleList();
})
</script>

<style>
.el-card {
    --el-card-padding: 17px;
}

.article-card {
    align-content: center;

    .article-title {
        font-size: 1.2rem;
        cursor: pointer;
    }

    .article-time {
        float: right;
        display: flex;
        align-items: center;
        font-size: 1.1rem;
    }
}
</style>
