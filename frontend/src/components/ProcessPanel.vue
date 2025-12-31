<template>
  <div class="process-panel">
    <!-- 进度条 -->
    <div class="progress-section">
      <a-progress
        :percent="taskInfo.progress"
        :status="progressStatus"
        stroke-color="#1890ff"
        :stroke-width="12"
        :show-info="true"
        class="custom-progress"
      />
    </div>

    <a-divider style="margin: 20px 0;">当前状态</a-divider>

    <!-- 状态显示 -->
    <a-alert
      :type="alertType"
      :message="taskInfo.message"
      show-icon
      class="status-alert"
    />

    <!-- 步骤显示 -->
    <div class="steps-container">
      <a-steps
        :current="currentStep"
        :status="stepStatus"
        size="small"
        direction="vertical"
      >
        <a-step title="读取订单数据" :description="getStepDesc(0)" />
        <a-step title="解析数据" :description="getStepDesc(1)" />
        <a-step title="AI 商品映射" :description="getStepDesc(2)" />
        <a-step title="标准化数据" :description="getStepDesc(3)" />
        <a-step title="写入 Excel" :description="getStepDesc(4)" />
        <a-step title="处理完成" :description="getStepDesc(5)" />
      </a-steps>
    </div>

    <a-divider style="margin: 20px 0;">处理日志</a-divider>

    <!-- 日志显示 -->
    <div class="log-container custom-scrollbar">
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
            <ClockCircleOutlined v-else style="font-size: 14px;" />
          </template>
          <div class="log-item">
            <span class="log-time">{{ log.time }}</span>
            <span class="log-message" :class="{'error-text': log.message.includes('失败') || log.message.includes('❌')}">{{ log.message }}</span>
          </div>
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
  // 如果任务已完成，所有步骤都显示"已完成"
  if (taskInfo.value.status === 'completed') return '已完成'
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
  padding: 8px 0;
}

.progress-section {
  padding: 0 12px;
}

.status-alert {
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.steps-container {
  background: #fafafa;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
}

.log-container {
  max-height: 400px;
  overflow-y: auto;
  padding: 20px;
  background: #1e1e1e; /* Dark terminal-like background for logs is often preferred by devs, or soft gray. Let's do Soft Gray/Code block style */
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e8e8e8;
}

.log-item {
  display: flex;
  flex-direction: column;
}

.log-time {
  color: #999;
  font-size: 12px;
  font-family: 'JetBrains Mono', monospace;
  margin-bottom: 2px;
}

.log-message {
  color: #333;
  font-size: 14px;
  line-height: 1.5;
}

.error-text {
  color: #ff4d4f;
  font-weight: 500;
}

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
</style>
