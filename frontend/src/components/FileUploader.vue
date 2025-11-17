<template>
  <a-upload-dragger
    :accept="accept"
    :before-upload="beforeUpload"
    :custom-request="customUpload"
    :file-list="[]"
    :show-upload-list="false"
    :max-count="1"
    class="fixed-height-uploader"
  >
    <p class="ant-upload-drag-icon">
      <inbox-outlined v-if="!uploadedFileName"></inbox-outlined>
      <check-circle-outlined v-else style="color: #52c41a"></check-circle-outlined>
    </p>
    <p class="ant-upload-text">
      {{ uploadedFileName ? uploadedFileName : title }}
    </p>
    <p class="ant-upload-hint">
      {{ uploadedFileName ? '点击重新上传' : '点击或拖拽文件到此区域上传' }}
    </p>
  </a-upload-dragger>
</template>

<script setup>
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import { InboxOutlined, CheckCircleOutlined } from '@ant-design/icons-vue'
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

const uploadedFileName = ref('')
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

const customUpload = async ({ file, onSuccess, onError }) => {
  try {
    uploading.value = true

    const res = await uploadFile(file)

    // 保存上传的文件名
    uploadedFileName.value = res.filename

    emit('uploaded', res)
    onSuccess(res)
  } catch (error) {
    message.error(error.message || '上传失败')
    onError(error)
  } finally {
    uploading.value = false
  }
}
</script>

<style scoped>
.fixed-height-uploader {
  height: 188px;
}
</style>

<style>
/* 确保上传区域固定高度 */
.fixed-height-uploader .ant-upload {
  height: 188px !important;
  display: flex !important;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.ant-upload-drag-icon {
  font-size: 48px;
  color: #1890ff;
  margin-bottom: 8px;
}

.ant-upload-text {
  font-size: 16px;
  color: rgba(0, 0, 0, 0.85);
  margin: 0 0 4px 0;
  padding: 0 20px;
  word-break: break-all;
}

.ant-upload-hint {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.45);
}
</style>
