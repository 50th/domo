import { ElMessage } from 'element-plus'
import axios from 'axios'
import type { AxiosResponse, AxiosProgressEvent } from 'axios'
import axiosInstance from './axiosInstance'
import { baseUrl } from '@/utils/baseUrl'
import type { FileInfo } from '@/interfaces'

const apiPrefix = '/api-file'

type ProgressCallback = (file: FileInfo, progress: number) => void

// 防抖函数
function debounce<ProgressCallback extends (...args: any) => any>(
  func: ProgressCallback,
  wait: number
): ProgressCallback {
  let startTime = Date.now()
  return function (this: any, ...args: Parameters<ProgressCallback>) {
    if (Date.now() - wait >= startTime) {
      func.apply(this, args)
      startTime = Date.now()
    }
  } as ProgressCallback
}

export async function downloadFile(
  file: FileInfo,
  token: string | null,
  updateProgressBar: ProgressCallback
): Promise<void> {
  try {
    const updateProgress = debounce(updateProgressBar, 200) // 200ms 防抖间隔时间

    const response: AxiosResponse = await axios({
      url: `${baseUrl}${apiPrefix}/files/${file.id}/`,
      method: 'GET',
      responseType: 'blob', // 接收二进制数据
      headers: token ? { Authorization: 'Bearer ' + token } : {},
      onDownloadProgress: (progressEvent: AxiosProgressEvent) => {
        const total = progressEvent.total
        const current = progressEvent.loaded
        if (total) {
          const percentage = Math.floor((current / total) * 100)
          updateProgress(file, percentage)
        }
      }
    })
    if (response.headers['content-type'].startsWith('application/json')) {
      const resCode = response.data.code
      if (resCode != 0) {
        ElMessage.warning(response.data.msg)
      }
    } else {
      // 处理文件名，从响应头的 content-disposition 中获取
      let filename = ''
      const disposition = response.headers['content-disposition']
      if (disposition) {
        const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/
        const matches = filenameRegex.exec(disposition)
        if (matches && matches[1]) {
          filename = decodeURIComponent(matches[1].replace(/['"]/g, '')) // 去除引号
        }
      }
      // 处理下载的文件
      const urlBlob = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.style.display = 'none'
      link.href = urlBlob
      link.download = filename // 指定下载后的文件名，防跳转
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(urlBlob)
    }
  } catch (error) {
    console.error('Error downloading the file:', error)
    ElMessage.warning('下载文件失败，请稍后再试')
  }
}

export async function getFileDownloadTopApi(): Promise<any> {
  return axiosInstance.get(`${apiPrefix}/download-count-top/`)
}

export async function getFileListApi(params?: any): Promise<any> {
  return axiosInstance.get(`${apiPrefix}/files/`, { params })
}

export async function delFileApi(id: number | string): Promise<any> {
  return axiosInstance.delete(`${apiPrefix}/files/${id}/`)
}
