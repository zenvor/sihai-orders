<template>
  <a-upload-dragger
    :accept="accept"
    :before-upload="beforeUpload"
    :custom-request="customUpload"
    :file-list="fileList"
    @remove="handleRemove"
    :max-count="1"
  >
    <p class="ant-upload-drag-icon">
      <inbox-outlined></inbox-outlined>
    </p>
    <p class="ant-upload-text">{{ title }}</p>
    <p class="ant-upload-hint">点击或拖拽文件到此区域上传</p>
  </a-upload-dragger>
</template>

<script setup>
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import { InboxOutlined } from '@ant-design/icons-vue'
import { uploadFile } from '../api'

const props = defineProps({
  accept: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['uploaded'])

const fileList = ref([])
const uploading = ref(false)

const beforeUpload = (file) => {
  const extension = props.accept.replace('.', '')
  const isValid = file.name.toLowerCase().endsWith(extension)

  if (!isValid) {
    message.error(`只能上传 ${props.accept} 文件`)
  }

  const isLt50M = file.size / 1024 / 1024 < 50
  if (!isLt50M) {
    message.error('文件大小不能超过 50MB')
    return false
  }

  return isValid
}

const customUpload = async ({ file, onSuccess, onError, onProgress }) => {
  try {
    uploading.value = true

    const res = await uploadFile(file)

    fileList.value = [{
      uid: res.fileId,
      name: res.filename,
      status: 'done',
      size: res.size
    }]

    emit('uploaded', res)
    onSuccess(res)
  } catch (error) {
    message.error(error.message || '上传失败')
    onError(error)
  } finally {
    uploading.value = false
  }
}

const handleRemove = () => {
  fileList.value = []
  return true
}
</script>

<style scoped>
.ant-upload-drag-icon {
  font-size: 48px;
  color: #1890ff;
}
</style>
