<template>
    <el-row>
        <el-col :span="4" :offset="5">
            <el-input v-model="searchVal" size="default" placeholder="搜索" clearable @change="refreshVideoList" />
        </el-col>
        <el-col :span="1">
            <el-upload style="display: inline; margin-left: 12px;" v-loading.fullscreen.lock="fullscreenLoading"
                :show-file-list="false" :action="`${baseUrl}/api-video/videos/`"
                :headers="userInfo ? { Authorization: `Bearer ${userInfo.access}` } : {}" name="video_path"
                :on-progress="openLoading" :on-success="afterUploadFile" :on-error="fileUploadError">
                <el-button color="#626aef" size="default" type="primary" text plain round>上传视频</el-button>
            </el-upload>
        </el-col>
        <el-col :span="2" style="display:flex; align-items:center; justify-content: center;">
            <span>视频总数：{{ videoCount }}</span>
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="14" :offset="5">
            <el-table :data="videoList" size="default" stripe @sort-change="handleSortChange">
                <el-table-column sortable="custom" prop="video_name" label="视频名称"></el-table-column>
                <el-table-column prop="video_type" label="视频类型" width="300" />
                <el-table-column prop="video_duration" :formatter="parseVideoDuration" label="视频时长" width="100" />
                <el-table-column sortable="custom" prop="upload_time" label="上传时间" width="160" />
                <el-table-column width="130">
                    <template #default="scope">
                        <div v-show="!scope.row.downloading">
                            <el-button type="success" text plain
                                @click="router.push({ name: 'playVideo', params: { id: scope.row.id } })">播放</el-button>
                            <el-button type="danger" text plain
                                @click="delFile(scope.row.id, scope.row.video_name)">删除</el-button>
                        </div>
                        <div v-show="scope.row.downloading">
                            <!-- <el-progress :percentage="scope.row.downloadingProgress" /> -->
                            <el-progress :text-inside="true" :stroke-width="18"
                                :percentage="scope.row.downloadingProgress" />
                        </div>
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <el-row style="margin-top: 20px;">
        <el-col :span="14" :offset="5">
            <el-pagination style="justify-content: center" layout="prev, pager, next" :page-size="pageSize"
                :pager-count="5" :total="videoCount" @current-change="handleCurrentChange" />
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

import { ElMessage } from 'element-plus'
import type { UploadFile, UploadFiles } from 'element-plus'

import { getVideoListApi, delVideoApi } from '@/apis/videoApis'
import { useUserStore } from '@/stores/user'
import { baseUrl } from '@/utils/baseUrl'
import type { VideoInfo, UserInfo } from '@/interfaces'

const router = useRouter()
const user = useUserStore();
const userInfo = ref<UserInfo | null>(user.getUser());

const videoList = ref<VideoInfo[]>([]);
const videoCount = ref<number>(0);
const fullscreenLoading = ref(false);
let currentPage = 1;
const pageSize = ref<number>(10);
const searchVal = ref<string>();
const ordering = ref<string>();

const refreshVideoList = () => {
    // 请求文件列表
    getVideoListApi({ page_num: currentPage, page_size: pageSize.value, search: searchVal.value, ordering: ordering.value }).then(res => {
        // console.log(res);
        if (res.code == 0) {
            videoList.value = res.data.results;
            videoCount.value = res.data.count;
        }
    });
}

const handleCurrentChange = (val: number) => {
    currentPage = val;
    refreshVideoList();
}

const handleSortChange = (data: { column: any, prop: string, order: any }) => {
    console.log(data);
    if (data.order == 'ascending') {
        ordering.value = data.prop;
    } else if (data.order == 'descending') {
        ordering.value = '-' + data.prop;
    } else {
        ordering.value = '';
    }
    refreshVideoList();
}

const openLoading = () => {
    fullscreenLoading.value = true;
}

const afterUploadFile = (response: any, uploadFile: UploadFile, uploadFiles: UploadFiles) => {
    fullscreenLoading.value = false;
    if (response.code == 0) {
        ElMessage.success('上传成功');
        currentPage = 1;
        refreshVideoList();
    } else {
        console.log(response)
        ElMessage.warning(response.msg);
    }
    // else if ([1003, 1004, 1005].indexOf(response.code) >= 0) {
    //     user.setUser(null);
    //     router.push({ name: 'login' });
    // }
}

const fileUploadError = () => {
    fullscreenLoading.value = false;
}

const delFile = (videoId: number, video_name: string) => {
    delVideoApi(videoId).then(res => {
        if (res.code == 0) {
            ElMessage.success(`${video_name} 删除成功`);
            refreshVideoList();
        }
    });
}

/**
 * 格式化视频时长
 * @param row
 * @param column
 * @param cellValue 单元格值
 * @param index
 */
const parseVideoDuration = (row: any, column: any, cellValue: number, index: any) => {
    let seconds = cellValue % 60;
    let minutes = ((cellValue - seconds) / 60) % 60;
    let hours = Math.floor(cellValue / 3600);
    return `${hours}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`
}

onMounted(async () => {
    refreshVideoList();
})
</script>
