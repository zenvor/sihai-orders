<template>
  <div class="process-panel">
    <!-- 进度条 -->
    <a-progress
      :percent="taskInfo.progress"
      :status="progressStatus"
      stroke-color="#1890ff"
      :show-info="true"
    />

    <a-divider>当前状态</a-divider>

    <!-- 状态显示 -->
    <a-alert
      :type="alertType"
      :message="taskInfo.message"
      show-icon
      style="margin-bottom: 16px"
    />

    <!-- 步骤显示 -->
    <a-steps
      :current="currentStep"
      :status="stepStatus"
      size="small"
      direction="vertical"
      style="margin-top: 24px"
    >
      <a-step title="读取订单数据" :description="getStepDesc(0)" />
      <a-step title="解析数据" :description="getStepDesc(1)" />
      <a-step title="AI 商品映射" :description="getStepDesc(2)" />
      <a-step title="标准化数据" :description="getStepDesc(3)" />
      <a-step title="写入 Excel" :description="getStepDesc(4)" />
      <a-step title="处理完成" :description="getStepDesc(5)" />
    </a-steps>

    <a-divider>处理日志</a-divider>

    <!-- 日志显示 -->
    <div class="log-container">
      <a-timeline mode="left">
        <a-timeline-item
          v-for="(log, index) in taskInfo.logs"
          :key="index"
          :color="getLogColor(log.message)"
        >
          <template #dot>
            <span v-if="log.message.includes('✅')">✅</span>
            <span v-else-if="log.message.includes('❌')">❌</span>
            <span v-else-if="log.message.includes('🔄')">🔄</span>
            <ClockCircleOutlined v-else />
          </template>
          <span class="log-time">{{ log.time }}</span>
          <span class="log-message">{{ log.message }}</span>
        </a-timeline-item>
      </a-timeline>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { ClockCircleOutlined } from '@ant-design/icons-vue'
import { getTaskStatus } from '../api'

const props = defineProps({
  taskId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['status-change'])

const taskInfo = ref({
  status: 'pending',
  progress: 0,
  message: '等待处理...',
  logs: []
})

const progressStatus = computed(() => {
  if (taskInfo.value.status === 'completed') return 'success'
  if (taskInfo.value.status === 'failed') return 'exception'
  return 'active'
})

const alertType = computed(() => {
  if (taskInfo.value.status === 'completed') return 'success'
  if (taskInfo.value.status === 'failed') return 'error'
  if (taskInfo.value.status === 'processing') return 'info'
  return 'warning'
})

const currentStep = computed(() => {
  const p = taskInfo.value.progress
  if (p < 10) return 0
  if (p < 30) return 1
  if (p < 55) return 2
  if (p < 75) return 3
  if (p < 100) return 4
  return 5
})

const stepStatus = computed(() => {
  if (taskInfo.value.status === 'failed') return 'error'
  if (taskInfo.value.status === 'completed') return 'finish'
  return 'process'
})

const getStepDesc = (step) => {
  const current = currentStep.value
  if (current > step) return '已完成'
  if (current === step) return '进行中...'
  return '等待中'
}

const getLogColor = (message) => {
  if (message.includes('✅') || message.includes('完成')) return 'green'
  if (message.includes('❌') || message.includes('失败')) return 'red'
  if (message.includes('🔄') || message.includes('正在')) return 'blue'
  return 'gray'
}

// 轮询任务状态
let pollInterval = null

const pollTaskStatus = async () => {
  try {
    const res = await getTaskStatus(props.taskId)
    taskInfo.value = res

    // 发送状态变化事件
    emit('status-change', res.status)

    // 如果任务完成或失败，停止轮询
    if (res.status === 'completed' || res.status === 'failed') {
      if (pollInterval) {
        clearInterval(pollInterval)
        pollInterval = null
      }
    }
  } catch (error) {
    console.error('获取任务状态失败:', error)
  }
}

onMounted(() => {
  pollTaskStatus()
  pollInterval = setInterval(pollTaskStatus, 1000)  // 每秒轮询一次
})

onUnmounted(() => {
  if (pollInterval) {
    clearInterval(pollInterval)
  }
})

// 监听 taskId 变化，重新开始轮询
watch(() => props.taskId, () => {
  if (pollInterval) {
    clearInterval(pollInterval)
  }
  pollTaskStatus()
  pollInterval = setInterval(pollTaskStatus, 1000)
})
</script>

<style scoped>
.process-panel {
  padding: 16px 0;
}

.log-container {
  max-height: 400px;
  overflow-y: auto;
  padding: 16px;
  background: #fafafa;
  border-radius: 4px;
}

.log-time {
  color: #999;
  margin-right: 12px;
  font-family: monospace;
}

.log-message {
  color: #333;
}
</style>
