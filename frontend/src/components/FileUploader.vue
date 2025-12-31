<template>
  <a-upload-dragger
    :accept="accept"
    :before-upload="beforeUpload"
    :custom-request="customUpload"
    :file-list="[]"
    :show-upload-list="false"
    :max-count="1"
    class="custom-uploader"
  >
    <div class="upload-content">
      <p class="upload-icon-wrapper">
        <inbox-outlined v-if="!uploadedFileName" class="upload-icon" />
        <check-circle-filled v-else class="success-icon" />
      </p>
      <p class="upload-text">
        {{ uploadedFileName ? uploadedFileName : title }}
      </p>
      <p class="upload-hint">
        {{ uploadedFileName ? '点击重新上传' : '点击或拖拽文件到此区域上传' }}
      </p>
    </div>
  </a-upload-dragger>
</template>

<script setup>
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import { InboxOutlined, CheckCircleFilled } from '@ant-design/icons-vue'
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
/* Minimal overrides to ensure height */
.custom-uploader {
  height: 100%;
  min-height: 200px;
  width: 100%;
  background: #fafafa;
  display: flex;
  flex-direction: column;
}

.upload-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  gap: 16px;
  padding: 20px;
}

.upload-icon {
  font-size: 48px;
  color: #1890ff;
}

.success-icon {
  font-size: 48px;
  color: #52c41a;
}

.upload-text {
  font-size: 16px;
  color: #333;
  margin: 0;
  font-weight: 500;
}

.upload-hint {
  font-size: 14px;
  color: #00000073;
  margin: 0;
}
</style>

<style>
/* Override Ant Design styles specifically for this uploader */
.custom-uploader .ant-upload-drag {
  border-radius: 12px !important;
  border: 2px dashed #d9d9d9 !important;
  background: #fafafa !important;
  transition: border-color 0.3s, background 0.3s !important;
}

.custom-uploader .ant-upload-drag:hover {
  border-color: #1890ff !important;
  background: #f0f5ff !important;
}

.custom-uploader .ant-upload-btn {
  padding: 0 !important;
  height: 100% !important;
  display: block !important;
}
</style>
