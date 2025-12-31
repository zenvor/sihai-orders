<template>
  <a-layout class="layout">
    <a-layout-header style="background: #fff; padding: 0 24px; box-shadow: 0 2px 8px #f0f1f2; z-index: 1;">
      <div class="header-content">
        <div class="brand">
          <CloudServerOutlined style="font-size: 24px; color: #1890ff; margin-right: 12px;" />
          <h1 style="margin: 0; font-size: 18px; font-weight: 600;">四海订单处理工具</h1>
        </div>
        <a-button type="text" @click="showConfigModal = true">
          <template #icon><SettingOutlined /></template>
          设置
        </a-button>
      </div>
    </a-layout-header>

    <a-layout-content style="padding: 24px;">
      <div style="max-width: 1200px; margin: 0 auto;">
        <a-space direction="vertical" size="large" style="width: 100%">

          <!-- 输入区域 -->
          <a-row :gutter="24">
            <a-col :xs="24" :md="12">
              <a-card title="订单数据" :bordered="true" style="height: 100%; display: flex; flex-direction: column;">
                <template #extra>
                  <a-segmented
                    v-model:value="orderInputMode"
                    :options="[{ label: '文件', value: 'file' }, { label: '文本', value: 'text' }]"
                  />
                </template>
                <div style="flex: 1;">
                  <OrderInput :mode="orderInputMode" @uploaded="handleOrderInputChanged" />
                </div>
              </a-card>
            </a-col>
            <a-col :xs="24" :md="12" style="margin-top: 0;">
              <a-card title="Excel 模板" :bordered="true" style="height: 100%; display: flex; flex-direction: column;">
                <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
                  <FileUploader
                    accept=".xlsx"
                    title="上传 Excel 模板"
                    @uploaded="handleExcelFileUploaded"
                    @removed="handleExcelFileRemoved"
                  />
                </div>
              </a-card>
            </a-col>
          </a-row>

          <!-- 操作栏 -->
          <a-card :bordered="true">
            <a-row justify="space-between" align="middle">
              <a-col>
                <a-space>
                  <CheckCircleFilled v-if="canProcess" style="color: #52c41a;" />
                  <span v-if="canProcess" style="color: #52c41a;">就绪，可以开始处理</span>
                  <span v-else style="color: rgba(0,0,0,0.45);">请完善上方输入以开始...</span>
                </a-space>
              </a-col>
              <a-col>
                <a-space>
                  <a-button @click="reset">
                    <template #icon><ClearOutlined /></template>
                    重置
                  </a-button>
                  <a-button
                    type="primary"
                    :disabled="!canProcess"
                    :loading="processing"
                    @click="startProcessing"
                  >
                    <template #icon><PlayCircleOutlined /></template>
                    开始处理
                  </a-button>
                  <a-button
                    v-if="currentTask && taskStatus === 'completed'"
                    type="default"
                    @click="downloadResult"
                  >
                    <template #icon><DownloadOutlined /></template>
                    下载结果
                  </a-button>
                </a-space>
              </a-col>
            </a-row>
          </a-card>

          <!-- 处理进度 -->
          <a-card v-if="currentTask" title="处理进度" :bordered="true">
             <template #extra><SyncOutlined :spin="taskStatus === 'processing'" /></template>
             <ProcessPanel :task-id="currentTask" @status-change="handleStatusChange" />
          </a-card>

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
    >
      <a-form layout="vertical">
        <a-form-item label="Deepseek API Key">
          <a-input-password
            v-model:value="apiKey"
            placeholder="sk-xxxxxxxxxxxxx"
          />
          <template #extra>
             如果不填写，将使用服务端配置的 API Key
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
  FileExcelOutlined,
  SyncOutlined,
  CheckCircleFilled
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
const orderInputMode = ref('file') // 订单输入模式
const excelFileId = ref(null)
const excelFileName = ref('')
const currentTask = ref(null)
const processing = ref(false)
const taskStatus = ref('pending')
const showConfigModal = ref(false)
const apiKey = ref('')

// 计算属性
const canProcess = computed(() => {
  const hasOrder = orderFileId.value || (orderContent.value && orderContent.value.trim().length > 0)
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
    // message.success(`订单文件上传成功: ${info.filename}`)
  } else if (info.type === 'text') {
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

// 处理 Excel 文件删除
const handleExcelFileRemoved = () => {
  excelFileId.value = null
  excelFileName.value = ''
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
    // 注意：processing 状态在 handleStatusChange 中根据任务完成状态更新
  } catch (error) {
    message.error(error.message || '启动任务失败')
    processing.value = false  // 只有出错时才立即恢复
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
  message.info('已清空所有输入')
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

const handleStatusChange = (status) => {
  taskStatus.value = status
  // 任务完成或失败时，取消 loading 状态
  if (status === 'completed' || status === 'failed') {
    processing.value = false
  }
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  background: #f0f2f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
}

.brand {
  display: flex;
  align-items: center;
}

/* Ensure cards in grid have same height */
:deep(.ant-card-body) {
  height: 100%;
  padding: 24px;
}
</style>
