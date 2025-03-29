<template>
  <div class="review-message-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>活动审核结果</span>
        </div>
      </template>

      <!-- 活动列表表格 -->
      <el-table :data="reviewList" style="width: 100%" v-loading="loading">
        <el-table-column
          prop="activity_title"
          label="活动名称"
          min-width="200"
        />
        <el-table-column prop="apply_time" label="申请时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.apply_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="审核状态" width="120">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
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

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
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
          <span class="label">活动名称：</span>
          <span class="value">{{ currentReview.activity_title }}</span>
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
            {{ currentReview.status }}
          </el-tag>
        </div>
        <div class="detail-item">
          <span class="label">审核意见：</span>
          <div class="comment-box">
            {{ currentReview.comment || "暂无审核意见" }}
          </div>
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
import { getReviewMessage } from "@/api/activity";
import { useUserStore } from "@/store/user";

interface ReviewItem {
  id: number;
  activity_title: string;
  apply_time: string;
  status: string;
  comment: string;
}

const userStore = useUserStore();
const reviewList = ref<ReviewItem[]>([]);
const loading = ref(false);
const dialogVisible = ref(false);
const currentReview = ref<ReviewItem>({} as ReviewItem);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 格式化日期
const formatDate = (date: string) => {
  return dayjs(date).format("YYYY-MM-DD HH:mm:ss");
};

// 获取状态标签类型
const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    申请通过: "success",
    申请未通过: "danger",
    审核中: "warning",
  };
  return statusMap[status] || "info";
};

// 显示审核详情
const showReviewDetail = (row: ReviewItem) => {
  currentReview.value = row;
  dialogVisible.value = true;
};

// 获取审核消息列表
const getReviewList = async () => {
  try {
    loading.value = true;
    const res = await getReviewMessage(userStore.sno);
    if (res.data.code === 200) {
      reviewList.value = res.data.data;
      total.value = res.data.data.length;
    } else {
      ElMessage.warning(res.data.msg || "获取审核列表失败");
    }
  } catch (error) {
    console.error("获取审核列表失败:", error);
    ElMessage.error("获取审核列表失败");
  } finally {
    loading.value = false;
  }
};

// 分页处理
const handleSizeChange = (val: number) => {
  pageSize.value = val;
  getReviewList();
};

const handleCurrentChange = (val: number) => {
  currentPage.value = val;
  getReviewList();
};

onMounted(() => {
  getReviewList();
});
</script>

<style scoped>
.review-message-container {
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

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
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

    .comment-box {
      flex: 1;
      padding: 15px;
      background-color: #f5f7fa;
      border-radius: 4px;
      color: #606266;
      line-height: 1.6;
      min-height: 80px;
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
