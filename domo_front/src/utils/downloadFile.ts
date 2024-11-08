import { downloadFile } from '@/apis/fileApis'
import type { FileInfo, UserInfo } from '@/interfaces'

const updateProgressBar = (file: FileInfo, percentage: number) => {
  file.downloading = true
  // console.log(`Download progress: ${percentage}%`);
  file.downloadingProgress = percentage
}

export const downloadFileHandler = (file: FileInfo, user: UserInfo | null) => {
  downloadFile(file, user ? user.access : null, updateProgressBar).then((res) => {
    file.downloading = false
    file.downloadingProgress = 100
    file.download_count += 1
  })
}
