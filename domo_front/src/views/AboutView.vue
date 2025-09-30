<template>
    <el-row>
        <el-col style="text-align: center;">
            <el-card style="" shadow="hover" class="home-box">
                <template #header>
                    <div>
                        <p class="title">Domo</p>
                        <p class="version">{{ sysVersion }}</p>
                    </div>
                </template>
                <img src="@/assets/about.jpg" style="width: 100%" />
                <template #footer>
                    <div>
                        <p v-if="hitokoto.hitokoto">{{ hitokoto.hitokoto }} -- {{ hitokoto.from }}</p>
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
const hitokoto = ref<Hitokoto>({ id: '', hitokoto: '', from: '', from_who: '', uuid: '' });


onMounted(() => {
    sysInfoApi().then(res => {
        if (res.code === 0) {
            sysVersion.value = res.data.version;
        }
    })
    getHitokotoApi().then(data => {
        hitokoto.value = data;
    }).catch(
        err => {
            console.error('获取一言失败', err);
            hitokoto.value = { id: '', hitokoto: '人民万岁！', from: '毛泽东', from_who: '毛泽东', uuid: '' };
        }
    )
})
</script>
<style scoped>
.home-box {
    max-width: 550px;
    margin: auto;

    .title {
        font-size: 2.5rem;
        margin: auto;
    }

    .version {
        font-size: 1rem;
        color: #999;
        text-align: right;
    }

    p {
        margin: 0;
    }
}
</style>
