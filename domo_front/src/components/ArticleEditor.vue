<template>
    <el-row>
        <el-col :span="24">
            <el-page-header title="返回" @back="back">
                <template v-if="title" #content>
                    <div class="article-header">
                        <div class="article-title">
                            <span>{{ title }}</span>
                        </div>
                    </div>
                </template>
                <template #extra>
                    <div class="flex items-center">
                        <el-button style="margin-left: 12px;" size="default" type="success" plain text
                            @click="saveArticle">
                            保存
                        </el-button>
                        <el-button size="default" type="danger" plain text @click="back">
                            退出
                        </el-button>
                    </div>
                </template>
            </el-page-header>
        </el-col>
    </el-row>

    <el-row style="margin-bottom: 10px; margin-top: 10px;">
        <el-col :span="4" :offset="2" style="align-content: center;">
            <el-input v-model="title" size="normal" placeholder="文章标题" />
        </el-col>
        <el-col :span="2" :offset="1" style="align-content: center;">
            <el-switch v-model="status" :active-value="1" :inactive-value="0" active-text="隐藏" />
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="20" :offset="2">
            <div style="border: 1px solid #ccc;">
                <MdEditor style="height: 700px" v-model="content" :showCodeRowNumber="true" :toolbars="toolbars"
                    previewTheme="vuepress" @onUploadImg="onUploadImg" @onSave="saveArticle" />
            </div>
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { MdEditor, type ToolbarNames } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import { ElMessage } from 'element-plus'

import type { ArticleInfo } from '@/interfaces';
import { addArticleApi, updateArticleApi, uploadImgApi } from '@/apis/articleApis';
import { useUserStore } from '@/stores/user';

const toolbars = ref<ToolbarNames[]>([
    'bold',
    'underline',
    'italic',
    '-',
    'title',
    'strikeThrough',
    'sub',
    'sup',
    'quote',
    'unorderedList',
    'orderedList',
    'task',
    '-',
    'codeRow',
    'code',
    'link',
    'image',
    'table',
    'mermaid',
    'katex',
    '-',
    'revoke',
    'next',
    'save',
    '=',
    'pageFullscreen',
    'fullscreen',
    'preview',
    'previewOnly',
    'htmlPreview',
    'catalog',
]);
const props = defineProps<{
    isAdd: boolean
    articleInfo?: ArticleInfo
}>()

const router = useRouter();

const user = useUserStore();

const title = ref<string>('');
const content = ref<string>('');
const status = ref<number>(0);

let articleId: number | null = null;

function saveArticle(value?: string, html?: Promise<string>) {
    if (title.value && content.value) {
        if (!articleId) {
            addArticleApi({ title: title.value, content: content.value, status: status.value }).then(res => {
                if (res.code == 0) {
                    ElMessage.success('保存成功');
                    articleId = res.data.id;
                } else if ([1003, 1004, 1005].indexOf(res.code) >= 0) {
                    user.setUser(null);
                    router.push({ name: 'login' });
                }
            })
        } else {
            updateArticleApi(articleId, { title: title.value, content: content.value, status: status.value }).then(res => {
                if (res.code == 0) {
                    ElMessage.success('保存成功');
                } else if ([1003, 1004, 1005].indexOf(res.code) >= 0) {
                    user.setUser(null);
                    router.push({ name: 'login' });
                }
            })
        }
    } else {
        ElMessage.warning('请填写内容');
    }
}

const onUploadImg = async (files: any[], callback: (arg0: any[]) => void) => {
    const res = await Promise.all(
        files.map((file: string | Blob) => {
            return new Promise((rev, rej) => {
                const form = new FormData();
                form.append('img', file);
                uploadImgApi(form, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }).then((res) => {
                    if (res.code == 0) {
                        rev(res);
                    } else if ([1003, 1004, 1005].indexOf(res.code) >= 0) {
                        user.setUser(null);
                        router.push({ name: 'login' });
                    }
                }).catch((error) => rej(error));
            });
        })
    );

    callback(
        res.map((item: any) => ({
            url: item.data.url,
            alt: item.data.name,
            title: item.data.title,
        }))
    );
};

const back = () => {
    if (props.isAdd || !props.articleInfo) {
        router.push({ name: 'articleList' });
    } else {
        router.push({ name: 'articleDetail', params: { id: props.articleInfo.id } });
    }
}

onMounted(() => {
    if (!props.isAdd && props.articleInfo) {
        articleId = props.articleInfo.id;
        title.value = props.articleInfo.title;
        content.value = props.articleInfo.content;
        status.value = props.articleInfo.status;
    }
})

</script>
