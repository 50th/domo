export interface UserInfo {
  id: number
  username: string
  // email: string
  // phone_num: string
  access: string
  refresh: string
  is_superuser: boolean
}

export interface ArticleInfo {
  id: number
  title: string
  abstract?: string
  content: string
  author: number
  author_name: string
  status: number
  create_time?: string
  last_edit_time?: string
  view_count: number
  like_count: number
}

export interface FileInfo {
  id: number
  filename: string
  file_size: number
  file_type: string
  upload_time: string
  upload_user: string
  downloading: boolean
  downloadingProgress: number
  download_count: number
}

export interface VideoInfo {
  id: number
  video_uuid: string
  video_name: string
  video_size: number
  video_duration: number
  video_type: string
  upload_user: number
  upload_username: string
  upload_time: string
}
