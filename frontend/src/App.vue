<template>
  <a-layout class="app-layout">
    <a-layout-header class="header">
      <div class="header-content">
        <h1>四海订单处理工具</h1>
        <a-button type="link" @click="showConfigModal = true">
          <template #icon><SettingOutlined /></template>
          设置
        </a-button>
      </div>
    </a-layout-header>

    <a-layout-content class="content">
      <a-space direction="vertical" size="large" style="width: 100%">

        <!-- 文件上传区域 -->
        <a-card title="文件上传">
          <a-row :gutter="16">
            <a-col :span="12">
              <FileUploader
                accept=".txt"
                title="订单文件 (order.txt)"
                @uploaded="handleOrderFileUploaded"
              />
            </a-col>
            <a-col :span="12">
              <FileUploader
                accept=".xlsx"
                title="Excel 模板"
                @uploaded="handleExcelFileUploaded"
              />
            </a-col>
          </a-row>
        </a-card>

        <!-- 操作按钮 -->
        <a-card>
          <a-space size="middle">
            <a-button
              type="primary"
              size="large"
              :disabled="!canProcess"
              :loading="processing"
              @click="startProcessing"
            >
              <template #icon><PlayCircleOutlined /></template>
              开始处理
            </a-button>

            <a-button
              size="large"
              :disabled="!currentTask || taskStatus !== 'completed'"
              @click="downloadResult"
            >
              <template #icon><DownloadOutlined /></template>
              下载结果
            </a-button>

            <a-button size="large" @click="reset">
              <template #icon><ClearOutlined /></template>
              清空
            </a-button>
          </a-space>
        </a-card>

        <!-- 处理进度 -->
        <a-card v-if="currentTask" title="处理进度">
          <ProcessPanel :task-id="currentTask" @status-change="handleStatusChange" />
        </a-card>

      </a-space>
    </a-layout-content>

    <!-- 配置弹窗 -->
    <a-modal
      v-model:open="showConfigModal"
      title="配置"
      @ok="saveConfig"
      ok-text="保存"
      cancel-text="取消"
    >
      <a-form layout="vertical">
        <a-form-item label="Deepseek API Key">
          <a-input-password
            v-model:value="apiKey"
            placeholder="sk-xxxxxxxxxxxxx"
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
  ClearOutlined
} from '@ant-design/icons-vue'

import FileUploader from './components/FileUploader.vue'
import ProcessPanel from './components/ProcessPanel.vue'
import { startProcess, downloadFile, updateConfig } from './api'

// 状态
const orderFileId = ref(null)
const orderFileName = ref('')
const excelFileId = ref(null)
const excelFileName = ref('')
const currentTask = ref(null)
const processing = ref(false)
const taskStatus = ref('pending')
const showConfigModal = ref(false)
const apiKey = ref('')

// 计算属性
const canProcess = computed(() => {
  return orderFileId.value && excelFileId.value && !processing.value
})

// 文件上传回调
const handleOrderFileUploaded = (fileInfo) => {
  orderFileId.value = fileInfo.fileId
  orderFileName.value = fileInfo.filename
  message.success(`订单文件上传成功: ${fileInfo.filename}`)
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
    const res = await startProcess({
      order_file_id: orderFileId.value,
      excel_file_id: excelFileId.value,
      api_key: apiKey.value || undefined
    })

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
.app-layout {
  min-height: 100vh;
  background: #f0f2f5;
}

.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 0 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.header h1 {
  margin: 0;
  color: #1890ff;
  font-size: 24px;
}

.content {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>
