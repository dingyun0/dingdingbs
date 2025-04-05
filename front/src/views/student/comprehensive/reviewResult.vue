<template>
  <div class="review-result-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>成绩疑问审核结果</span>
        </div>
      </template>

      <!-- 成绩疑问列表表格 -->
      <el-table :data="reviewList" style="width: 100%" v-loading="loading">
        <el-table-column prop="question_type" label="疑问类型" width="150" />
        <el-table-column prop="content" label="疑问说明" min-width="200" />
        <el-table-column prop="apply_time" label="申请时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.apply_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="审核状态" width="120">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button type="primary" link @click="showReviewDetail(scope.row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 审核详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="审核详情"
      width="50%"
      :close-on-click-modal="false"
      class="review-dialog"
    >
      <div class="review-detail">
        <div class="detail-item">
          <span class="label">疑问类型：</span>
          <span class="value">{{ currentReview.question_type }}</span>
        </div>
        <div class="detail-item">
          <span class="label">申请时间：</span>
          <span class="value">{{ formatDate(currentReview.apply_time) }}</span>
        </div>
        <div class="detail-item">
          <span class="label">审核状态：</span>
          <el-tag
            :type="getStatusType(currentReview.status)"
            class="status-tag"
          >
            {{ getStatusText(currentReview.status) }}
          </el-tag>
        </div>
        <div class="detail-item">
          <span class="label">疑问说明：</span>
          <div>
            {{ currentReview.content }}
          </div>
        </div>
        <div class="detail-item" v-if="currentReview.review_comment">
          <span class="label">审核意见：</span>
          <div class="comment-box">
            {{ currentReview.review_comment }}
          </div>
        </div>
        <div class="detail-item" v-if="currentReview.review_time">
          <span class="label">审核时间：</span>
          <span class="value">{{ formatDate(currentReview.review_time) }}</span>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import dayjs from "dayjs";
import { getScoreReviewResult } from "@/api/score";
import { useUserStore } from "@/store/user";

interface ReviewItem {
  id: number;
  question_type: string;
  content: string;
  apply_time: string;
  status: string;
  review_comment?: string;
  review_time?: string;
}

const userStore = useUserStore();
const reviewList = ref<ReviewItem[]>([]);
const loading = ref(false);
const dialogVisible = ref(false);
const currentReview = ref<ReviewItem>({} as ReviewItem);

// 格式化日期
const formatDate = (date: string) => {
  return dayjs(date).format("YYYY-MM-DD HH:mm:ss");
};

// 获取状态标签类型
const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    approved: "success",
    rejected: "danger",
    pending: "warning",
  };
  return statusMap[status] || "info";
};

// 获取状态显示文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    approved: "已通过",
    rejected: "已驳回",
    pending: "审核中",
  };
  return statusMap[status] || status;
};

// 显示审核详情
const showReviewDetail = (row: ReviewItem) => {
  currentReview.value = row;
  dialogVisible.value = true;
};

// 获取审核结果列表
const getReviewList = async () => {
  try {
    loading.value = true;
    console.log("111111111111111", userStore);

    const res = await getScoreReviewResult(userStore.sno);
    if (res.data.code === 200) {
      reviewList.value = Array.isArray(res.data.data)
        ? res.data.data
        : [res.data.data];
    } else {
      ElMessage.warning(res.data.msg || "获取审核结果失败");
    }
  } catch (error) {
    console.error("获取审核结果失败:", error);
    ElMessage.error("获取审核结果失败");
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  getReviewList();
});
</script>

<style scoped>
.review-result-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 84px);
}

.box-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.review-dialog {
  :deep(.el-dialog__body) {
    padding: 20px 30px;
  }
}

.review-detail {
  .detail-item {
    margin-bottom: 20px;
    display: flex;
    align-items: flex-start;

    .label {
      width: 100px;
      color: #606266;
      font-weight: bold;
    }

    .value {
      flex: 1;
      color: #303133;
    }

    .status-tag {
      margin-left: 10px;
    }

    .content-box,
    .comment-box {
      flex: 1;
      padding: 15px;
      background-color: #f5f7fa;
      border-radius: 4px;
      color: #606266;
      line-height: 1.6;
      min-height: 60px;
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
