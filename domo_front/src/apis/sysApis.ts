import axiosInstance from './axiosInstance'

const apiPrefix = '/api-sys'

export async function sysInfoApi(): Promise<any> {
  return axiosInstance.get(`${apiPrefix}/sys-info/`)
}
