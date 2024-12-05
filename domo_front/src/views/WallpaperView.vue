<template>
    <el-row>
        <el-col :span="3" :offset="6">
            <el-input v-model="searchVal" placeholder="搜索(文件名)" size="default" clearable @change="refreshWallpaperList" />
        </el-col>
        <el-col :span="2" style="display:flex; align-items:center; justify-content: center;">
            <span>壁纸总数：{{ wallpaperCount }}</span>
        </el-col>
        <el-col :span="1" v-if="userInfo">
            <el-upload style="display: inline; margin-left: 12px;" v-loading.fullscreen.lock="fullscreenLoading"
                :show-file-list="false" :action="`${baseUrl}/api-wallpaper/upload-wallpaper/`"
                :headers="userInfo ? { Authorization: `Bearer ${userInfo.access}` } : {}" name="wallpaper"
                :on-progress="openLoading" :on-success="afterUploadWallpaper" :on-error="wallpaperUploadError">
                <el-tooltip content="上传壁纸会统一转为 JPEG 格式" placement="top" effect="light">
                    <el-button color="#626aef" type="primary" size="default" text plain round>上传壁纸</el-button>
                </el-tooltip>
            </el-upload>
        </el-col>
    </el-row>
    <el-row style="margin-top: 15px;">
        <el-col :span="4" v-for="(wallpaper, index) in wallpaperList" :key="wallpaper.id" style="text-align: center;">
            <div class="demo-image">
                <div class="block">
                    <el-card shadow="hover" body-style="padding: 5px">
                        <div class="mask">
                            <div style="margin-top: 10%;">
                                <el-button @click="previewWallpaper(index)">预览</el-button>
                                <el-button @click="downloadWallpaper(wallpaper.id)">下载</el-button>
                                <el-button v-if="userInfo && userInfo.is_superuser" type="danger"
                                    @click="delWallpaper(wallpaper.id, wallpaper.image_name)">删除</el-button>
                            </div>
                            <h3>{{ wallpaper.image_res }}</h3>
                            <p>{{ parseSize(wallpaper.image_size) }}</p>
                        </div>
                        <el-image fit="scale-down" :src="`${baseUrl}/api-wallpaper/wallpaper-thumb/${wallpaper.id}/`" />
                        <el-image-viewer v-if="showViewerList[index]" @close="() => { showViewerList[index] = false }"
                            :hide-on-click-modal="true"
                            :url-list="[`${baseUrl}/api-wallpaper/wallpapers/${wallpaper.id}/`]" />
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
const pageSize = ref<number>(18);
const searchVal = ref<string>();
const ordering = ref<string>();
const showViewerList = ref<boolean[]>([]);

const refreshWallpaperList = () => {
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

const previewWallpaper = (index: number) => {
    console.log("preview");
    showViewerList.value[index] = true;
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
 * @param img_size 图片大小字节数
 */
const parseSize = (img_size: number) => {
    img_size /= 1024
    if (img_size < 1024) {
        return Number(img_size.toFixed(2)) + ' KB';
    } else {
        img_size /= 1024;
        if (img_size < 1024) {
            return Number(img_size.toFixed(2)) + ' MB';
        } else {
            return Number((img_size / 1024).toFixed(2)) + ' GB';
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
        padding: 10px 0;
        text-align: center;
        display: inline-block;
        box-sizing: border-box;
        vertical-align: top;

        .mask {
            position: absolute;
            width: 288px;
            height: 162px;
            color: #ffffff;
            z-index: 1;
            opacity: 0;
        }

        .el-image {
            width: 288px;
            height: 162px;
            z-index: 2;

            img {
                z-index: 1;
            }

            img:hover {
                z-index: 0;
            }
        }

        .el-image:hover {
            z-index: 0;
        }

        .mask:hover {
            z-index: 3;
            background: rgba(148, 144, 144, 0.6);
            display: block;
            opacity: 1;
        }
    }
}
</style>