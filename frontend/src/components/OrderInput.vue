<template>
  <div class="order-input-container">
    <!-- 切换按钮 -->
    <div class="input-mode-toggle">
      <a-segmented
        v-model:value="inputMode"
        :options="inputModeOptions"
        @change="handleModeChange"
      />
    </div>

    <!-- 文件上传模式 -->
    <div v-show="inputMode === 'file'" class="input-section">
      <FileUploader
        accept=".txt"
        title="订单文件 (order.txt)"
        @uploaded="handleFileUploaded"
      />
    </div>

    <!-- 文本输入模式 -->
    <div v-show="inputMode === 'text'" class="input-section">
      <a-textarea
        v-model:value="orderText"
        placeholder="请输入订单内容，格式如下：&#10;&#10;店铺名称1:&#10;商品名称1:数量1件&#10;商品名称2:数量2件&#10;&#10;店铺名称2:&#10;商品名称3:数量3件"
        :rows="10"
        :maxlength="50000"
        show-count
        class="order-textarea"
        @change="handleTextChange"
      />
      <div class="textarea-actions">
        <a-space>
          <a-button
            type="primary"
            size="small"
            :disabled="!orderText.trim()"
            @click="confirmTextInput"
          >
            <template #icon><CheckOutlined /></template>
            确认
          </a-button>
          <a-button
            size="small"
            @click="clearTextInput"
          >
            <template #icon><ClearOutlined /></template>
            清空
          </a-button>
        </a-space>
      </div>
      <div v-if="textConfirmed" class="text-confirmed-status">
        <check-circle-outlined style="color: #52c41a; margin-right: 8px" />
        <span>订单内容已确认 ({{ orderText.length }} 字符)</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { message } from 'ant-design-vue'
import { CheckOutlined, ClearOutlined, CheckCircleOutlined } from '@ant-design/icons-vue'
import FileUploader from './FileUploader.vue'

const emit = defineEmits(['uploaded'])

// 输入模式：file（文件上传）或 text（文本输入）
const inputMode = ref('file')
const inputModeOptions = [
  { label: '📁 文件上传', value: 'file' },
  { label: '✏️ 文本输入', value: 'text' }
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
    // 从文本模式切换到文件模式，清除文本输入状态
    message.info('已切换到文件上传模式')
    // 发送一个清除事件，让父组件知道需要清除订单数据
    emit('uploaded', { cleared: true })
  } else if (value === 'text' && fileUploaded.value) {
    // 从文件模式切换到文本模式，清除文件上传状态
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
  // 清除文本输入状态
  textConfirmed.value = false
  orderText.value = ''
  // 向上传递文件信息
  emit('uploaded', {
    type: 'file',
    fileId: info.fileId,
    filename: info.filename
  })
}

// 处理文本变化
const handleTextChange = () => {
  // 如果用户修改了文本，取消确认状态
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
  // 清除文件上传状态
  fileUploaded.value = false
  fileInfo.value = null

  // 向上传递文本内容
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
}

.input-mode-toggle {
  display: flex;
  justify-content: center;
  padding: 8px 0;
}

.input-section {
  min-height: 188px;
}

.order-textarea {
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
}

.textarea-actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
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
  font-size: 14px;
}
</style>
