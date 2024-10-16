<template>
    <el-row v-if="articleInfo">
        <el-col :span="24">
            <el-page-header title="返回" @back="router.push({ name: 'articleList' });">
                <template #content>
                    <!-- <div class="article-header">
                        <span class="article-title">{{ articleInfo.title }}</span>
                        <span class="article-time">发布时间 {{ articleInfo.create_time }}</span>
                        <span class="article-time">编辑时间 {{ articleInfo.last_edit_time }}</span>
                        <span class="article-time">作者 {{ articleInfo.author_name }}</span>
                    </div> -->

                    <div>
                        <span style="font-size: 1.3rem;">{{ articleInfo.title }}</span>
                    </div>
                    <div style="font-size: 0.8rem; min-width: 600px;">
                        <span>发布时间 {{ articleInfo.create_time }}</span>
                        <span style="margin-left: 2%;">编辑时间 {{ articleInfo.last_edit_time }}</span>
                        <span style="margin-left: 2%;">作者 {{ articleInfo.author_name }}</span>
                    </div>
                </template>
                <template #extra>
                    <div class="flex items-center">
                        <el-button
                            v-if="userInfo && (userInfo.id == articleInfo.author || (!articleInfo.author && userInfo.is_superuser))"
                            style="margin-left: 12px;" size="default" type="success" plain text
                            @click="router.push({ name: 'editArticle', params: { id: articleId } })">
                            编辑文章
                        </el-button>
                        <el-button v-if="userInfo && (userInfo.is_superuser || userInfo.id == articleInfo.author)"
                            size="default" type="danger" plain text @click="delArticle">
                            删除文章
                        </el-button>
                    </div>
                </template>
            </el-page-header>
        </el-col>
    </el-row>

    <el-row v-if="articleInfo">
        <el-col :span="12" :offset="6">
            <el-card style="width: 100%; border-style: none;" shadow="never">
                <MdPreview previewTheme="default" :codeStyleReverse="true" :editorId="mdPreviewID"
                    :modelValue="articleInfo.content" :showCodeRowNumber="true" />
                <template #footer>
                    <div class="article-footer">
                        <span>发布时间 {{ articleInfo.create_time }}</span>
                        <span style="margin-left: 2%;">编辑时间 {{ articleInfo.last_edit_time }}</span>
                        <span style="margin-left: 2%;">作者 {{ articleInfo.author_name }}</span>
                    </div>
                </template>
            </el-card>
        </el-col>
        <!-- <el-col :span="4" class="affix-container">
            <el-affix target=".affix-container" :offset="150">
                <MdCatalog style="background-color: white;" :editorId="mdPreviewID" :scrollElement="scrollElement" />
            </el-affix>
        </el-col> -->
    </el-row>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MdPreview } from 'md-editor-v3';
import 'md-editor-v3/lib/preview.css';
import { ElMessage, ElMessageBox } from 'element-plus';

import { useUserStore } from '@/stores/user'
import { getArticleApi, delArticleApi } from '@/apis/articleApis'
import type { ArticleInfo } from '@/interfaces';

const route = useRoute();
const router = useRouter();
const user = useUserStore();
const userInfo = user.getUser();

const articleId = ref<string>(route.params.id as string);
const articleInfo = ref<ArticleInfo>();

const mdPreviewID = 'preview-article-content';
const scrollElement = document.documentElement;

function getArticle() {
    getArticleApi(articleId.value).then(res => {
        if (res.code == 2001) {
            router.push({ name: 'articleList' });
        }
        articleInfo.value = res.data;
    })
}

const delArticle = () => {
    ElMessageBox.confirm(
        '确认删除此文章？',
        '警告',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        }
    ).then(() => {
        delArticleApi(articleId.value).then(res => {
            if (res.code == 0) {
                ElMessage.error('删除成功');
                router.push({ name: 'articleList' });
            } else if ([1003, 1004, 1005].indexOf(res.code) >= 0) {
                user.setUser(null);
                router.push({ name: 'login' });
            }
        })
    }).catch(() => {
        ElMessage({
            type: 'info',
            message: '取消删除',
        })
    })
}

onMounted(async () => {
    getArticle();
})

</script>
<style>
.md-editor-preview {
    font-size: 1.2rem;

    .code-block {
        /* font-family: source-code-pro, Menlo, Monaco, Consolas, "Courier New", monospace; */
        /* font: initial; */
        /* font-size: 1rem; */
    }

}

.article-header {
    min-width: 800px;

    .article-title {
        font-size: 1.3rem;
    }

    .article-time {
        margin-left: 2%;
        font-size: 0.8rem;
    }
}

.article-footer {
    /* align-content: center; */
    /* float: inline-end; */
    font-size: 0.9rem;
    /* margin-top: 15px; */
}

.affix-container {
    margin-left: 5px;
}
</style>
