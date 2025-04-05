<template>
  <div class="review-container">
    <el-card class="review-card">
      <template #header>
        <div class="card-header">
          <span class="title">成绩疑问审核</span>
        </div>
      </template>

      <!-- 审核列表 -->
      <el-table
        v-if="reviewList.length > 0"
        :data="reviewList"
        border
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="student_sno" label="学号" width="120" />
        <el-table-column prop="student_name" label="学生姓名" width="120" />
        <el-table-column prop="question_type" label="疑问类型" width="120">
          <template #default="scope">
            {{ formatQuestionType(scope.row.question_type) }}
          </template>
        </el-table-column>
        <el-table-column
          prop="content"
          label="疑问说明"
          min-width="200"
          show-overflow-tooltip
        />
        <el-table-column prop="apply_time" label="申请时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.apply_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ formatStatus(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="120">
          <template #default="scope">
            <el-button
              v-if="scope.row.status === 'pending'"
              type="primary"
              link
              @click="handleReview(scope.row)"
            >
              审核
            </el-button>
            <el-button
              v-else
              type="info"
              link
              @click="viewReviewDetail(scope.row)"
            >
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-else description="暂无待审核的成绩疑问" />

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

    <!-- 审核对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isView ? '查看详情' : '成绩疑问审核'"
      width="600px"
      :close-on-click-modal="false"
      class="review-dialog"
    >
      <el-form
        ref="reviewFormRef"
        :model="reviewForm"
        :rules="rules"
        label-width="100px"
        class="review-form"
      >
        <div class="info-section">
          <el-form-item label="学生学号">
            <span>{{ currentReview?.student_sno }}</span>
          </el-form-item>
          <el-form-item label="学生姓名">
            <span>{{ currentReview?.student_name }}</span>
          </el-form-item>
          <el-form-item label="疑问类型">
            <span>{{
              formatQuestionType(currentReview?.question_type || "")
            }}</span>
          </el-form-item>
          <el-form-item label="申请时间">
            <span>{{ formatDate(currentReview?.apply_time || "") }}</span>
          </el-form-item>
        </div>

        <el-form-item label="疑问说明" class="content-item">
          <div>{{ currentReview?.content }}</div>
        </el-form-item>

        <template v-if="!isView">
          <el-form-item label="审核结果" prop="status" class="review-result">
            <el-radio-group v-model="reviewForm.status">
              <el-radio label="approved">通过</el-radio>
              <el-radio label="rejected">不通过</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="审核意见" prop="comment">
            <el-input
              v-model="reviewForm.comment"
              type="textarea"
              :rows="4"
              placeholder="请输入审核意见..."
            />
          </el-form-item>
        </template>
        <template v-else>
          <el-form-item label="审核结果">
            <el-tag :type="getStatusType(currentReview?.status || '')">
              {{ formatStatus(currentReview?.status || "") }}
            </el-tag>
          </el-form-item>
          <el-form-item label="审核意见">
            <div class="content-box">{{ currentReview?.review_comment }}</div>
          </el-form-item>
        </template>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">
            {{ isView ? "关闭" : "取消" }}
          </el-button>
          <el-button v-if="!isView" type="primary" @click="submitReview">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import dayjs from "dayjs";
import { getScoreReviewList, submitScoreReviewResult } from "@/api/score";

// 接口定义
interface ReviewItem {
  id: number;
  student_sno: string;
  student_name: string;
  question_type: string;
  content: string;
  status: string;
  apply_time: string;
  review_comment?: string;
  review_time?: string;
}

// 响应式数据
const loading = ref(false);
const dialogVisible = ref(false);
const isView = ref(false);
const reviewList = ref<ReviewItem[]>([]);
const currentReview = ref<ReviewItem | null>(null);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 表单相关
const reviewFormRef = ref<FormInstance>();
const reviewForm = ref({
  status: "",
  comment: "",
});

const rules: FormRules = {
  status: [{ required: true, message: "请选择审核结果", trigger: "change" }],
  comment: [{ required: true, message: "请输入审核意见", trigger: "blur" }],
};

// 格式化函数
const formatDate = (date: string) => {
  return date ? dayjs(date).format("YYYY-MM-DD HH:mm:ss") : "";
};

const formatQuestionType = (type: string) => {
  const typeMap: Record<string, string> = {
    academic: "学业成绩",
    moral: "德育成绩",
    sports: "体育成绩",
    other: "其他",
  };
  return typeMap[type] || type;
};

const formatStatus = (status: string) => {
  const statusMap: Record<string, string> = {
    pending: "待审核",
    approved: "已通过",
    rejected: "已驳回",
  };
  return statusMap[status] || status;
};

const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    pending: "warning",
    approved: "success",
    rejected: "danger",
  };
  return typeMap[status] || "info";
};

// 获取审核列表
const getReviewList = async () => {
  loading.value = true;
  try {
    const { data: response } = await getScoreReviewList();

    if (response.code === 200 && response.data) {
      reviewList.value = response.data.list;
      total.value = response.data.total;
    } else {
      ElMessage.error(response.message || "获取列表失败");
    }
  } catch (error) {
    console.error("获取审核列表失败:", error);
    ElMessage.error("获取审核列表失败");
  } finally {
    loading.value = false;
  }
};

// 处理审核
const handleReview = (row: ReviewItem) => {
  currentReview.value = row;
  reviewForm.value = {
    status: "",
    comment: "",
  };
  isView.value = false;
  dialogVisible.value = true;
};

// 查看详情
const viewReviewDetail = (row: ReviewItem) => {
  currentReview.value = row;
  isView.value = true;
  dialogVisible.value = true;
};

// 提交审核
const submitReview = async () => {
  if (!reviewFormRef.value) return;

  await reviewFormRef.value.validate(async (valid) => {
    if (valid && currentReview.value) {
      try {
        const { data: response } = await submitScoreReviewResult({
          review_id: currentReview.value.id,
          status: reviewForm.value.status,
          comment: reviewForm.value.comment,
        });

        if (response.code === 200) {
          ElMessage.success("审核成功");
          dialogVisible.value = false;
          getReviewList(); // 刷新列表
        } else {
          ElMessage.error(response.message || "审核失败");
        }
      } catch (error) {
        console.error("审核失败:", error);
        ElMessage.error("审核失败");
      }
    }
  });
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
.review-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 84px);
}

.review-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.review-dialog :deep(.el-dialog__body) {
  padding: 20px 30px;
}

.review-form {
  margin: 0;
}

.info-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.info-section :deep(.el-form-item) {
  margin-bottom: 0;
}

.content-item {
  margin-bottom: 24px;
}

.content-box {
  padding: 12px 16px;
  background-color: #f8f9fa;
  border-radius: 4px;
  min-height: 60px;
  max-height: 200px;
  overflow-y: auto;
  line-height: 1.6;
  color: #606266;
  border: 1px solid #e4e7ed;
  white-space: pre-wrap;
  word-break: break-all;
}

.review-result {
  margin-top: 24px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

:deep(.el-form-item.is-required .el-form-item__label::before) {
  margin-right: 2px;
}
</style>
