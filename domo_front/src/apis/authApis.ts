import axiosInstance from './axiosInstance'

const apiPrefix = '/api-auth'

export async function loginApi(username: string, password: string): Promise<any> {
  return axiosInstance.post(`${apiPrefix}/login/`, { username, password })
}

export async function checkAccessApi(token: string): Promise<any> {
  return axiosInstance.post(`${apiPrefix}/token/verify/`, { token })
}
