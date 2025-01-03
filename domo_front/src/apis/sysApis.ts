import axiosInstance from './axiosInstance'

const apiPrefix = '/api-sys'

export async function sysInfoApi(): Promise<any> {
  return axiosInstance.get(`${apiPrefix}/sys-info/`)
}

export async function getHitokotoApi(): Promise<any> {
  return axiosInstance.get('https://v1.hitokoto.cn/')
}
