<template>
    <el-row>
        <el-col :span="24">
            <el-page-header title="返回" @back="router.push({ name: 'videoList' });">
                <template #content v-if="videoInfo">
                    <div>
                        <span style="font-size: 1.3rem;">{{ videoInfo.video_name }}</span>
                    </div>
                    <div style="font-size: 0.8rem; min-width: 600px;">
                        <span>发布时间 {{ videoInfo.upload_time }}</span>
                        <span style="margin-left: 2%;">发布人 {{ videoInfo.upload_username }}</span>
                    </div>
                </template>
                <template #extra>
                    <div class="flex items-center">
                        <el-button
                            v-if="userInfo && videoInfo && (userInfo.is_superuser || userInfo.id == videoInfo.upload_user)"
                            size="default" type="danger" plain text @click="delVideo">
                            删除视频
                        </el-button>
                    </div>
                </template>
            </el-page-header>
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="14" :offset="5">
            <div id="mse" style="min-height: 500px;"></div>
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from 'vue-router';

import { ElMessage, ElMessageBox } from 'element-plus';
import Player from 'xgplayer';
import 'xgplayer/dist/index.min.css';

import { baseUrl } from '@/utils/baseUrl';
import { useUserStore } from '@/stores/user';
import { delVideoApi, getVideoApi } from "@/apis/videoApis";
import type { VideoInfo } from "@/interfaces";

const route = useRoute();
const router = useRouter();
const user = useUserStore();
const userInfo = user.getUser();
const videoId = route.params.id as string;
const videoUrl = `${baseUrl}/api-video/video_serve/${videoId}/`

const videoInfo = ref<VideoInfo>();

const delVideo = () => {
    ElMessageBox.confirm(
        '确认删除此视频？',
        '警告',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        }
    ).then(() => {
        delVideoApi(videoId).then(res => {
            if (res.code == 0) {
                ElMessage.error('删除成功');
                router.push({ name: 'videoList' });
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

onMounted(() => {
    getVideoApi(videoId).then(res => {
        if (res.code == 0) {
            videoInfo.value = res.data;
            const player = new Player({
                id: 'mse',
                url: `${baseUrl}/api-video/video_serve/${videoInfo.value?.video_uuid}/`,
                width: '100%',
                height: '100%',
            });
        }
    })
});
</script>
