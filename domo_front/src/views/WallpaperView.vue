<template>
    <el-row>
        <el-col :span="4" :offset="5">
            <el-input v-model="searchVal" size="default" placeholder="搜索(文件名)" clearable
                @change="refreshWallpaperList" />
        </el-col>
        <el-col :span="1">
            <el-upload style="display: inline; margin-left: 12px;" v-loading.fullscreen.lock="fullscreenLoading"
                :show-file-list="false" :action="`${baseUrl}/api-wallpaper/upload-wallpaper/`"
                :headers="userInfo ? { Authorization: `Bearer ${userInfo.access}` } : {}" name="wallpaper"
                :on-progress="openLoading" :on-success="afterUploadWallpaper" :on-error="wallpaperUploadError">
                <el-tooltip content="上传壁纸会统一转为 JPG 格式" placement="top" effect="light">
                    <el-button color="#626aef" size="default" type="primary" text plain round>上传壁纸</el-button>
                </el-tooltip>

            </el-upload>
        </el-col>
        <el-col :span="2" style="display:flex; align-items:center; justify-content: center;">
            <span>壁纸总数：{{ wallpaperCount }}</span>
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="24" :offset="0" style="text-align: center;">
            <div class="demo-image">
                <div v-for="wallpaper in wallpaperList" :key="wallpaper.id" class="block">
                    <el-card shadow="hover" body-style="padding: 10px">
                        <!-- <template #header>Yummy hamburger</template> -->
                        <div class="mask">
                            <div style="margin-top: 15%;">
                                <el-button @click="downloadWallpaper(wallpaper.id)">下载</el-button>
                                <el-button
                                    v-if="!wallpaper.upload_user || (userInfo && (userInfo.id == wallpaper.upload_user || userInfo.is_superuser))"
                                    type="danger"
                                    @click="delWallpaper(wallpaper.id, wallpaper.image_name)">删除</el-button>
                            </div>

                            <h3>{{ wallpaper.image_res }}</h3>
                        </div>
                        <el-image :src="`${baseUrl}/api-wallpaper/wallpaper-thumb/${wallpaper.id}/`"
                            style="width: 320px; height: 180px;" />
                    </el-card>

                </div>
            </div>
        </el-col>
    </el-row>
    <el-row style="margin-top: 20px;">
        <el-col :span="14" :offset="5">
            <el-pagination style="justify-content: center" layout="prev, pager, next" :page-size="pageSize"
                :pager-count="5" :total="wallpaperCount" @current-change="handleCurrentChange" />
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { UploadFile, UploadFiles } from 'element-plus'

import { getWallpaperListApi, delWallpaperApi, downloadWallpaperApi } from '@/apis/wallpaperApis'
import { useUserStore } from '@/stores/user'
import { baseUrl } from '@/utils/baseUrl'
import type { WallpaperInfo, UserInfo } from '@/interfaces'

const user = useUserStore();
const userInfo = ref<UserInfo | null>(user.getUser());

const wallpaperList = ref<WallpaperInfo[]>([]);
const wallpaperCount = ref<number>(0);
const fullscreenLoading = ref(false);
let currentPage = 1;
const pageSize = ref<number>(10);
const searchVal = ref<string>();
const ordering = ref<string>();

const refreshWallpaperList = () => {
    // 请求文件列表
    getWallpaperListApi({ page_num: currentPage, page_size: pageSize.value, search: searchVal.value, ordering: ordering.value }).then(res => {
        // console.log(res);
        if (res.code == 0) {
            // res.data.results.forEach((file: WallpaperInfo) => {
            //     file.downloading = false;
            //     file.downloadingProgress = 0;
            // });
            wallpaperList.value = res.data.results;
            wallpaperCount.value = res.data.count;
        }
    });
}

// const updateProgressBar = (file: WallpaperInfo, percentage: number) => {
//     file.downloading = true;
//     // console.log(`Download progress: ${percentage}%`);
//     file.downloadingProgress = percentage;
// }

// const downloadFileHandler = (file: WallpaperInfo) => {
//     downloadFile(file, userInfo.value ? userInfo.value.access : null, updateProgressBar).then(res => {
//         file.downloading = false;
//         file.downloadingProgress = 100;
//         file.download_count += 1;
//     });
// }

const handleCurrentChange = (val: number) => {
    currentPage = val;
    refreshWallpaperList();
}

// const handleSortChange = (data: { column: any, prop: string, order: any }) => {
//     console.log(data);
//     if (data.order == 'ascending') {
//         ordering.value = data.prop;
//     } else if (data.order == 'descending') {
//         ordering.value = '-' + data.prop;
//     } else {
//         ordering.value = '';
//     }
//     refreshFileList();
// }

const openLoading = () => {
    fullscreenLoading.value = true;
}

const afterUploadWallpaper = (response: any, uploadFile: UploadFile, uploadFiles: UploadFiles) => {
    fullscreenLoading.value = false;
    if (response.code == 0) {
        ElMessage.success('上传成功');
        currentPage = 1;
        refreshWallpaperList();
    } else {
        console.log(response)
        ElMessage.warning(response.msg);
    }
    // else if ([1003, 1004, 1005].indexOf(response.code) >= 0) {
    //     user.setUser(null);
    //     router.push({ name: 'login' });
    // }
}

const wallpaperUploadError = () => {
    fullscreenLoading.value = false;
}

const downloadWallpaper = (id: string) => {
    downloadWallpaperApi(id, userInfo.value ? userInfo.value.access : null);
}

const delWallpaper = (id: string, image_name: string) => {
    delWallpaperApi(id).then(res => {
        if (res.code == 0) {
            ElMessage.success(`${image_name} 删除成功`);
            refreshWallpaperList();
        }
    });
}

/**
 * 格式化文件大小
 * @param row 
 * @param column 
 * @param cellValue 单元格值
 * @param index 
 */
const parseFileSize = (row: any, column: any, cellValue: number, index: any) => {
    cellValue /= 1024
    if (cellValue < 1024) {
        return Number(cellValue.toFixed(2)) + ' KB';
    } else {
        cellValue /= 1024;
        if (cellValue < 1024) {
            return Number(cellValue.toFixed(2)) + ' MB';
        } else {
            return Number((cellValue / 1024).toFixed(2)) + ' GB';
        }
    }
}

onMounted(async () => {
    refreshWallpaperList();
})
</script>

<style>
.demo-image {
    .block {
        padding: 30px 0;
        text-align: center;
        margin-right: 5px;
        display: inline-block;
        box-sizing: border-box;
        vertical-align: top;

        .mask {
            position: absolute;
            width: 320px;
            height: 180px;
            background: rgba(101, 101, 101, 0.6);
            color: #ffffff;
            opacity: 0.8;
            z-index: 1;
        }

        .el-image {
            z-index: 2;
        }

        .el-image:hover {
            z-index: 0;
        }

        .mask:hover {
            z-index: 3;
        }
    }

    .block:last-child {
        margin-right: 0px;
    }

    .demonstration {
        display: block;
        color: var(--el-text-color-secondary);
        font-size: 14px;
        margin-bottom: 20px;
    }

}
</style>