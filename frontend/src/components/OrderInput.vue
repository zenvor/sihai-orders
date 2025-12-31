<template>
  <div class="order-input-container">
    <!-- 内容区域 -->
    <div class="content-area">
      <div v-if="mode === 'file'" class="input-section full-height" key="file">
        <FileUploader
          accept=".txt"
          title="订单文件 (order.txt)"
          @uploaded="handleFileUploaded"
          @removed="handleFileRemoved"
          class="inner-uploader"
        />
      </div>

      <div v-else-if="mode === 'text'" class="input-section full-height" key="text">
        <div class="textarea-wrapper">
           <a-textarea
            v-model:value="orderText"
            placeholder="请输入订单内容，格式如下：&#10;&#10;店铺名称1:&#10;商品名称1:数量1件&#10;商品名称2:数量2件&#10;&#10;店铺名称2:&#10;商品名称3:数量3件"
            :rows="15"
            :maxlength="50000"
            show-count
            @change="handleTextChange"
          />
        </div>
        
        <div class="textarea-actions">
          <span v-if="textConfirmed" class="status-text success">
             <check-circle-filled /> 已确认 ({{ orderText.length }})
          </span>
          <span v-else class="status-text warning" v-show="orderText.length > 0">
             未确认
          </span>

          <div class="buttons">
            <a-button
              size="small"
              @click="clearTextInput"
              v-if="orderText.length > 0"
            >
              <template #icon><ClearOutlined /></template>
              清空
            </a-button>

            <a-button
              type="primary"
              size="small"
              :disabled="!orderText.trim()"
              @click="confirmTextInput"
            >
              <template #icon><CheckOutlined /></template>
              确认输入
            </a-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { message } from 'ant-design-vue'
import { CheckOutlined, ClearOutlined, CheckCircleFilled } from '@ant-design/icons-vue'
import FileUploader from './FileUploader.vue'

const props = defineProps({
  mode: {
    type: String,
    default: 'file'
  }
})

const emit = defineEmits(['uploaded'])

// 文本输入模式的状态
const orderText = ref('')
const textConfirmed = ref(false)

// 文件上传模式的状态
const fileUploaded = ref(false)
const fileInfo = ref(null)

// 监听模式切换，清除状态
watch(() => props.mode, (newMode, oldMode) => {
  if (newMode !== oldMode) {
    if (oldMode === 'text' && textConfirmed.value) {
      emit('uploaded', { cleared: true })
    } else if (oldMode === 'file' && fileUploaded.value) {
      emit('uploaded', { cleared: true })
      fileUploaded.value = false
      fileInfo.value = null
    }
  }
})

// 处理文件上传
const handleFileUploaded = (info) => {
  fileUploaded.value = true
  fileInfo.value = info
  textConfirmed.value = false
  orderText.value = ''
  emit('uploaded', {
    type: 'file',
    fileId: info.fileId,
    filename: info.filename
  })
}

// 处理文件删除
const handleFileRemoved = () => {
  fileUploaded.value = false
  fileInfo.value = null
  emit('uploaded', { cleared: true })
}

// 处理文本变化
const handleTextChange = () => {
  if (textConfirmed.value) {
    textConfirmed.value = false
    emit('uploaded', { cleared: true })
  }
}

// 确认文本输入
const confirmTextInput = () => {
  if (!orderText.value.trim()) {
    message.warning('请输入订单内容')
    return
  }

  textConfirmed.value = true
  fileUploaded.value = false
  fileInfo.value = null

  emit('uploaded', {
    type: 'text',
    content: orderText.value
  })

  message.success('订单内容已确认')
}

// 清空文本输入
const clearTextInput = () => {
  orderText.value = ''
  textConfirmed.value = false
  emit('uploaded', { cleared: true })
  message.info('已清空订单内容')
}
</script>

<style scoped>
.order-input-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
}

.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0; /* Important for nested flex scroll */
}

.input-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.full-height {
  height: 100%;
}

.textarea-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-bottom: 12px;
  min-height: 0;
}

/* 关键修复：强制 Ant Design Textarea 充满高度 */
.custom-textarea {
  height: 100%;
}

:deep(.ant-input-affix-wrapper) {
  height: 100%;
  display: flex;
  flex-direction: column;
}

:deep(.ant-input) {
  flex: 1;
  height: 100% !important;
  resize: none !important;
  font-family: monospace;
}

.inner-uploader {
  height: 100% !important;
}

.textarea-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto; /* Push to bottom if needed, though flex structure handles it */
  padding-top: 8px;
}

.status-text {
  font-size: 14px;
}

.buttons {
  display: flex;
  gap: 8px;
}
</style>
