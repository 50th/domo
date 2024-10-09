<template>
    <ArticleEditor v-if="articleInfo && articleInfo.content" :is-add="false" :article-info="articleInfo" />
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import ArticleEditor from '@/components/ArticleEditor.vue'
import { getArticleApi } from '@/apis/articleApis'
import type { ArticleInfo } from '@/interfaces';

const articleInfo = ref<ArticleInfo>();

const route = useRoute();
const router = useRouter();

const articleId = route.params.id as string;

function getArticle() {
    getArticleApi(articleId).then(res => {
        if (res.code == 2001) {
            router.push({ name: 'articleList' });
        }
        articleInfo.value = res.data;
    })
}

onMounted(async () => {
    getArticle();
})

</script>
<style></style>
