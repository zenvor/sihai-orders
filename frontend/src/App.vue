<template>
  <a-layout class="app-layout">
    <a-layout-header class="header">
      <div class="header-content">
        <div class="brand">
          <div class="logo-icon">
            <CloudServerOutlined />
          </div>
          <h1>四海订单处理工具</h1>
        </div>
        <a-button type="text" class="settings-btn" @click="showConfigModal = true">
          <template #icon><SettingOutlined /></template>
          设置
        </a-button>
      </div>
    </a-layout-header>

    <a-layout-content class="content">
      <div class="content-wrapper">
        <a-space direction="vertical" size="large" style="width: 100%">

          <!-- 文件上传区域 -->
          <a-card class="glass-card" :bordered="false">
            <template #title>
              <div class="card-title">
                <FileTextOutlined class="title-icon" />
                <span>文件上传</span>
              </div>
            </template>
            <div class="upload-section">
              <OrderInput
                @uploaded="handleOrderInputChanged"
              />
              <FileUploader
                accept=".xlsx"
                title="Excel 模板"
                @uploaded="handleExcelFileUploaded"
              />
            </div>
          </a-card>

          <!-- 操作按钮 -->
          <a-card class="glass-card action-card" :bordered="false">
            <div class="action-buttons">
              <a-button
                type="primary"
                size="large"
                class="main-action-btn"
                :disabled="!canProcess"
                :loading="processing"
                @click="startProcessing"
              >
                <template #icon><PlayCircleOutlined /></template>
                开始处理
              </a-button>

              <div class="secondary-actions">
                <a-button
                  size="large"
                  class="secondary-btn"
                  :disabled="!currentTask || taskStatus !== 'completed'"
                  @click="downloadResult"
                >
                  <template #icon><DownloadOutlined /></template>
                  下载结果
                </a-button>

                <a-button 
                  size="large" 
                  class="secondary-btn danger-hover"
                  @click="reset"
                >
                  <template #icon><ClearOutlined /></template>
                  清空
                </a-button>
              </div>
            </div>
          </a-card>

          <!-- 处理进度 -->
          <transition name="fade">
            <a-card v-if="currentTask" class="glass-card" :bordered="false">
              <template #title>
                <div class="card-title">
                  <SyncOutlined class="title-icon" :spin="taskStatus === 'processing'" />
                  <span>处理进度</span>
                </div>
              </template>
              <ProcessPanel :task-id="currentTask" @status-change="handleStatusChange" />
            </a-card>
          </transition>

        </a-space>
      </div>
    </a-layout-content>

    <!-- 配置弹窗 -->
    <a-modal
      v-model:open="showConfigModal"
      title="配置"
      @ok="saveConfig"
      ok-text="保存"
      cancel-text="取消"
      class="custom-modal"
    >
      <a-form layout="vertical">
        <a-form-item label="Deepseek API Key">
          <a-input-password
            v-model:value="apiKey"
            placeholder="sk-xxxxxxxxxxxxx"
            class="custom-input"
          />
          <template #extra>
            <a-typography-text type="secondary">
              如果不填写，将使用服务端配置的 API Key
            </a-typography-text>
          </template>
        </a-form-item>
      </a-form>
    </a-modal>
  </a-layout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { message } from 'ant-design-vue'
import {
  SettingOutlined,
  PlayCircleOutlined,
  DownloadOutlined,
  ClearOutlined,
  CloudServerOutlined,
  FileTextOutlined,
  SyncOutlined
} from '@ant-design/icons-vue'

import FileUploader from './components/FileUploader.vue'
import OrderInput from './components/OrderInput.vue'
import ProcessPanel from './components/ProcessPanel.vue'
import { startProcess, downloadFile, updateConfig } from './api'

// 状态
const orderFileId = ref(null)
const orderFileName = ref('')
const orderContent = ref(null)
const orderType = ref(null) // 'file' 或 'text'
const excelFileId = ref(null)
const excelFileName = ref('')
const currentTask = ref(null)
const processing = ref(false)
const taskStatus = ref('pending')
const showConfigModal = ref(false)
const apiKey = ref('')

// 计算属性
const canProcess = computed(() => {
  const hasOrder = orderFileId.value || orderContent.value
  return hasOrder && excelFileId.value && !processing.value
})

// 订单输入变化回调
const handleOrderInputChanged = (info) => {
  if (info.cleared) {
    // 清除订单数据
    orderFileId.value = null
    orderFileName.value = ''
    orderContent.value = null
    orderType.value = null
    return
  }

  if (info.type === 'file') {
    // 文件上传模式
    orderFileId.value = info.fileId
    orderFileName.value = info.filename
    orderContent.value = null
    orderType.value = 'file'
    message.success(`订单文件上传成功: ${info.filename}`)
  } else if (info.type === 'text') {
    // 文本输入模式
    orderContent.value = info.content
    orderFileId.value = null
    orderFileName.value = ''
    orderType.value = 'text'
  }
}

const handleExcelFileUploaded = (fileInfo) => {
  excelFileId.value = fileInfo.fileId
  excelFileName.value = fileInfo.filename
  message.success(`Excel 模板上传成功: ${fileInfo.filename}`)
}

// 开始处理
const startProcessing = async () => {
  try {
    processing.value = true

    // 构建请求参数
    const params = {
      excel_file_id: excelFileId.value,
      api_key: apiKey.value || undefined
    }

    // 根据订单类型添加不同的参数
    if (orderType.value === 'file') {
      params.order_file_id = orderFileId.value
    } else if (orderType.value === 'text') {
      params.order_content = orderContent.value
    }

    const res = await startProcess(params)

    currentTask.value = res.taskId
    taskStatus.value = 'pending'
    message.success('任务已启动')
  } catch (error) {
    message.error(error.message || '启动任务失败')
  } finally {
    processing.value = false
  }
}

// 下载结果
const downloadResult = () => {
  if (currentTask.value) {
    downloadFile(currentTask.value)
    message.success('开始下载结果文件')
  }
}

// 重置
const reset = () => {
  orderFileId.value = null
  orderFileName.value = ''
  orderContent.value = null
  orderType.value = null
  excelFileId.value = null
  excelFileName.value = ''
  currentTask.value = null
  taskStatus.value = 'pending'
  message.info('已清空')
}

// 保存配置
const saveConfig = async () => {
  try {
    await updateConfig({ api_key: apiKey.value || undefined })
    message.success('配置保存成功')
    showConfigModal.value = false
  } catch (error) {
    message.error('配置保存失败')
  }
}

// 任务状态变化回调
const handleStatusChange = (status) => {
  taskStatus.value = status
}
</script>

<style scoped>
/* 全局布局优化 */
.app-layout {
  min-height: 100vh;
  /* 柔和的渐变背景 */
  background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* 顶部导航栏 */
.header {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  height: 64px;
  line-height: 64px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 800px;
  margin: 0 auto;
  height: 100%;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 24px;
  color: #1890ff;
  display: flex;
  align-items: center;
}

.header h1 {
  margin: 0;
  color: #2c3e50;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.settings-btn {
  color: #555;
  font-size: 15px;
  border-radius: 6px;
}

.settings-btn:hover {
  color: #1890ff;
  background-color: rgba(24, 144, 255, 0.1);
}

/* 主要内容区域 */
.content {
  padding: 32px 24px;
  width: 100%;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
}

/* 玻璃拟态卡片 */
.glass-card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  overflow: hidden;
  border: 1px solid rgba(0,0,0,0.03);
  transition: all 0.3s ease;
}

.glass-card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.title-icon {
  color: #1890ff;
}

/* 操作按钮区域 */
.action-card :deep(.ant-card-body) {
  padding: 24px;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.secondary-actions {
  display: flex;
  gap: 12px;
}

.main-action-btn {
  height: 48px;
  padding: 0 32px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 24px;
  background: linear-gradient(90deg, #1890ff 0%, #096dd9 100%);
  border: none;
  box-shadow: 0 4px 14px 0 rgba(24, 144, 255, 0.39);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.main-action-btn:hover:not(:disabled) {
  opacity: 0.95;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(24, 144, 255, 0.23);
}

.main-action-btn:disabled {
  background: #f5f5f5;
  color: rgba(0, 0, 0, 0.25);
  box-shadow: none;
}

.secondary-btn {
  height: 44px;
  border-radius: 8px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.secondary-btn:hover:not(:disabled) {
  border-color: #1890ff;
  color: #1890ff;
}

.danger-hover:hover {
  border-color: #ff4d4f;
  color: #ff4d4f;
}

/* 布局辅助 */
/* 上传区域垂直布局 */
.upload-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
}

/* 动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
