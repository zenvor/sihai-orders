<template>
  <div class="order-input-container">
    <!-- 切换按钮 -->
    <div class="input-mode-toggle">
      <a-segmented
        v-model:value="inputMode"
        :options="inputModeOptions"
        @change="handleModeChange"
        block
      />
    </div>

    <!-- 内容区域 -->
    <div class="content-area">
      <transition name="fade-slide" mode="out-in">
        <div v-if="inputMode === 'file'" class="input-section" key="file">
          <FileUploader
            accept=".txt"
            title="订单文件 (order.txt)"
            @uploaded="handleFileUploaded"
          />
        </div>

        <div v-else-if="inputMode === 'text'" class="input-section" key="text">
          <a-textarea
            v-model:value="orderText"
            placeholder="请输入订单内容，格式如下：&#10;&#10;店铺名称1:&#10;商品名称1:数量1件&#10;商品名称2:数量2件&#10;&#10;店铺名称2:&#10;商品名称3:数量3件"
            :rows="8"
            :maxlength="50000"
            show-count
            @change="handleTextChange"
            style="resize: none; font-family: monospace;"
          />
          
          <div class="textarea-actions">
            <a-button
              type="primary"
              :disabled="!orderText.trim()"
              @click="confirmTextInput"
            >
              <template #icon><CheckOutlined /></template>
              确认
            </a-button>
            <a-button
              @click="clearTextInput"
            >
              <template #icon><ClearOutlined /></template>
              清空
            </a-button>
          </div>
          
          <div v-if="textConfirmed" class="text-confirmed-status">
            <check-circle-filled style="color: #52c41a; font-size: 16px;" />
            <span class="confirmed-text">订单内容已确认 ({{ orderText.length }} 字符)</span>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import { CheckOutlined, ClearOutlined, CheckCircleFilled } from '@ant-design/icons-vue'
import FileUploader from './FileUploader.vue'

const emit = defineEmits(['uploaded'])

// 输入模式：file（文件上传）或 text（文本输入）
const inputMode = ref('file')
const inputModeOptions = [
  { label: '文件上传', value: 'file' },
  { label: '文本输入', value: 'text' }
]

// 文本输入模式的状态
const orderText = ref('')
const textConfirmed = ref(false)

// 文件上传模式的状态
const fileUploaded = ref(false)
const fileInfo = ref(null)

// 处理模式切换
const handleModeChange = (value) => {
  if (value === 'file' && textConfirmed.value) {
    message.info('已切换到文件上传模式')
    emit('uploaded', { cleared: true })
  } else if (value === 'text' && fileUploaded.value) {
    message.info('已切换到文本输入模式')
    emit('uploaded', { cleared: true })
    fileUploaded.value = false
    fileInfo.value = null
  }
}

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

.input-mode-toggle {
  margin-bottom: 4px;
}

/* Ensure content area allows child to fill it */
.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.input-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.textarea-actions {
  margin-top: 32px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
}

.text-confirmed-status {
  margin-top: 12px;
  padding: 8px 12px;
  background: #f6ffed;
  border: 1px solid #b7eb8f;
  border-radius: 4px;
  color: #52c41a;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Animations */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.2s ease-in-out;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
