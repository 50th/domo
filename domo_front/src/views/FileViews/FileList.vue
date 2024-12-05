<template>
    <el-row>
        <el-col :span="3" :offset="6">
            <el-input v-model="searchVal" placeholder="搜索(文件名)" clearable size="default" @change="refreshFileList" />
        </el-col>
        <el-col :span="2" style="display:flex; align-items:center; justify-content: center;">
            <span>文件总数：{{ fileCount }}</span>
        </el-col>
        <el-col :span="1">
            <el-upload style="display: inline; margin-left: 12px;" v-loading.fullscreen.lock="fullscreenLoading"
                :show-file-list="false" :action="`${baseUrl}/api-file/files/`"
                :headers="userInfo ? { Authorization: `Bearer ${userInfo.access}` } : {}" name="file_path"
                :on-progress="openLoading" :on-success="afterUploadFile" :on-error="fileUploadError">
                <el-button color="#626aef" type="primary" text plain round size="default">上传文件</el-button>
            </el-upload>
        </el-col>
    </el-row>
    <el-row style="margin-top: 15px;">
        <el-col :span="12" :offset="6">
            <el-table :data="fileList" size="default" @sort-change="handleSortChange">
                <el-table-column sortable="custom" prop="filename" label="文件名"></el-table-column>
                <!-- <el-table-column prop="file_type" label="类型" width="170" /> -->
                <el-table-column sortable="custom" prop="file_size" :formatter="parseFileSize" label="文件大小"
                    align="right" width="120" />
                <el-table-column sortable="custom" prop="upload_time" label="上传时间" width="180" align="center" />
                <el-table-column prop="download_count" label="下载次数" align="center" width="90" />
                <el-table-column width="130">
                    <template #default="scope">
                        <div v-show="!scope.row.downloading">
                            <el-button type="success" text plain
                                @click="downloadFileHandler(scope.row, userInfo)">下载</el-button>
                            <el-button type="danger" text plain
                                @click="delFile(scope.row.id, scope.row.filename)">删除</el-button>
                        </div>
                        <div v-show="scope.row.downloading">
                            <el-progress :text-inside="true" :stroke-width="18"
                                :percentage="scope.row.downloadingProgress" />
                        </div>
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <el-row style="margin-top: 20px;">
        <el-col :span="16" :offset="4">
            <el-pagination style="justify-content: center" layout="prev, pager, next" :page-size="pageSize"
                :pager-count="5" :total="fileCount" @current-change="handleCurrentChange" />
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { UploadFile, UploadFiles } from 'element-plus'

import type { FileInfo, UserInfo } from '@/interfaces'
import { getFileListApi, delFileApi } from '@/apis/fileApis'
import { useUserStore } from '@/stores/user'
import { baseUrl } from '@/utils/baseUrl'
import { downloadFileHandler } from '@/utils/downloadFile'

const user = useUserStore();
const userInfo = ref<UserInfo | null>(user.getUser());

const fileList = ref<FileInfo[]>([]);
const fileCount = ref<number>(0);
const fullscreenLoading = ref(false);
let currentPage = 1;
const pageSize = ref<number>(10);
const searchVal = ref<string>();
const ordering = ref<string>();

const refreshFileList = () => {
    // 请求文件列表
    getFileListApi({ page_num: currentPage, page_size: pageSize.value, search: searchVal.value, ordering: ordering.value }).then(res => {
        // console.log(res);
        if (res.code == 0) {
            res.data.results.forEach((file: FileInfo) => {
                file.downloading = false;
                file.downloadingProgress = 0;
            });
            fileList.value = res.data.results;
            fileCount.value = res.data.count;
        }
    });
}

const handleCurrentChange = (val: number) => {
    currentPage = val;
    refreshFileList();
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
    refreshFileList();
}

const openLoading = () => {
    fullscreenLoading.value = true;
}

const afterUploadFile = (response: any, uploadFile: UploadFile, uploadFiles: UploadFiles) => {
    fullscreenLoading.value = false;
    if (response.code == 0) {
        ElMessage.success('上传成功');
        currentPage = 1;
        refreshFileList();
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

const delFile = (fileId: number, filename: string) => {
    delFileApi(fileId).then(res => {
        if (res.code == 0) {
            ElMessage.success(`${filename} 删除成功`);
            refreshFileList();
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
    refreshFileList();
})
</script>
<style></style>