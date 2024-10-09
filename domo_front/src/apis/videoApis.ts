import axiosInstance from './axiosInstance'

const apiPrefix = '/api-video'

export async function getVideoListApi(params?: any): Promise<any> {
  return axiosInstance.get(`${apiPrefix}/videos/`, { params })
}

export async function getVideoApi(id: number | string): Promise<any> {
  return axiosInstance.get(`${apiPrefix}/videos/${id}/`)
}

export async function uploadVideoApi(data: any, config: any): Promise<any> {
  return axiosInstance.post(`${apiPrefix}/videos/`, data, config)
}

export async function delVideoApi(id: number | string): Promise<any> {
  return axiosInstance.delete(`${apiPrefix}/videos/${id}/`)
}
