import type { AxiosResponse } from 'axios'

export function downloadFile(res: AxiosResponse) {
  let filename = ''
  const disposition = res.headers['content-disposition']
  const matches = disposition.match(/filename\*=([^;]+);*/)
  if (matches != null && matches[1]) {
    filename = decodeURIComponent(matches[1].split("'")[2])
  } else {
    const matches = disposition.match(/filename=([^;]+);*/)
    if (matches != null && matches[1]) {
      filename = matches[1].replace(/^"/, '').replace(/"$/, '')
    }
  }
  const url = window.URL.createObjectURL(new Blob([res.data]))
  const link = document.createElement('a')
  link.style.display = 'none'
  link.href = url
  link.download = filename // 指定下载后的文件名，防跳转
  document.body.appendChild(link)
  link.click()
  URL.revokeObjectURL(url)
}
