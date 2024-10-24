import { ElMessage } from 'element-plus'
import axios from 'axios'
import type { AxiosResponse } from 'axios'
import axiosInstance from './axiosInstance'
import { baseUrl } from '@/utils/baseUrl'

const apiPrefix = '/api-wallpaper'

export async function downloadWallpaperApi(wallpaper_id: string, token: string | null): Promise<void> {
  try {
    const response: AxiosResponse = await axios({
      url: `${baseUrl}${apiPrefix}/wallpapers/${wallpaper_id}/`,
      method: 'GET',
      responseType: 'blob', // 接收二进制数据
      headers: token ? { Authorization: 'Bearer ' + token } : {}
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
    ElMessage.warning('下载壁纸失败，请稍后再试')
  }
}

export async function getFileDownloadTopApi(): Promise<any> {
  return axiosInstance.get(`${apiPrefix}/download-count-top/`)
}

export async function getWallpaperListApi(params?: any): Promise<any> {
  return axiosInstance.get(`${apiPrefix}/wallpapers/`, { params })
}

export async function delWallpaperApi(id: string): Promise<any> {
  return axiosInstance.delete(`${apiPrefix}/wallpapers/${id}/`)
}
