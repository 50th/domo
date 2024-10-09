import axiosInstance from './axiosInstance'

const apiPrefix = '/api-article'

export async function getArticleViewTopApi(): Promise<any> {
  return axiosInstance.get(`${apiPrefix}/view-count-top/`)
}

export async function getArticleListApi(params?: any): Promise<any> {
  return axiosInstance.get(`${apiPrefix}/articles/`, { params })
}

export async function getArticleApi(id: number | string): Promise<any> {
  return axiosInstance.get(`${apiPrefix}/articles/${id}/`)
}

export async function addArticleApi(data: any): Promise<any> {
  return axiosInstance.post(`${apiPrefix}/articles/`, data)
}

export async function updateArticleApi(id: number | string, data: any): Promise<any> {
  return axiosInstance.put(`${apiPrefix}/articles/${id}/`, data)
}

export async function delArticleApi(id: number | string): Promise<any> {
  return axiosInstance.delete(`${apiPrefix}/articles/${id}/`)
}

export async function uploadImgApi(data: any, config: any): Promise<any> {
  return axiosInstance.post(`${apiPrefix}/article-img/`, data, config)
}
