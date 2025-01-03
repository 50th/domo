<template>
    <el-row>
        <el-col style="text-align: center;">
            <el-card style="max-width: 550px; margin: auto;" shadow="hover">
                <template #header>
                    <div class="home-box">
                        <span class="title">Domo</span>
                        <span class="version">{{ sysVersion }}</span>
                    </div>
                </template>
                <img src="@/assets/about.jpg" style="width: 100%" />
                <template #footer>
                    <div class="home-box">
                        <p>{{ hitokoto.hitokoto }} -- {{ hitokoto.from }}</p>
                    </div>
                </template>
            </el-card>
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue';

import { sysInfoApi, getHitokotoApi } from '@/apis/sysApis';
import type { Hitokoto } from '@/interfaces';

const sysVersion = ref<string | null>(null);
const hitokoto = ref<Hitokoto>({ id: '', hitokoto: '人民万岁！', from: '毛泽东', from_who: '毛泽东', uuid: '' });


onMounted(() => {
    sysInfoApi().then(res => {
        if (res.code === 0) {
            sysVersion.value = res.data.version;
        }
    })
    getHitokotoApi().then(({ data }) => {
        hitokoto.value = data;
    }).catch(console.error)
})
</script>
<style scoped>
.home-box {
    position: relative;

    .title {
        font-size: 2.5rem;
        margin: auto;
    }

    .version {
        font-size: 1rem;
        color: #999;
        position: absolute;
        right: 8rem;
        bottom: 0.5rem;
    }

    p {
        margin: 0;
    }
}
</style>
