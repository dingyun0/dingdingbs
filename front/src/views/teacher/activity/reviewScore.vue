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
        <el-table-column prop="semester" label="学期" width="120" />
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
      width="50%"
      :close-on-click-modal="false"
    >
      <el-form
        ref="reviewFormRef"
        :model="reviewForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="学生学号">
          <span>{{ currentReview?.student_sno }}</span>
        </el-form-item>
        <el-form-item label="学生姓名">
          <span>{{ currentReview?.student_name }}</span>
        </el-form-item>
        <el-form-item label="学期">
          <span>{{ currentReview?.semester }}</span>
        </el-form-item>
        <el-form-item label="疑问类型">
          <span>{{
            formatQuestionType(currentReview?.question_type || "")
          }}</span>
        </el-form-item>
        <el-form-item label="疑问说明">
          <div class="content-box">{{ currentReview?.content }}</div>
        </el-form-item>
        <el-form-item label="申请时间">
          <span>{{ formatDate(currentReview?.apply_time || "") }}</span>
        </el-form-item>
        <template v-if="!isView">
          <el-form-item label="审核结果" prop="status">
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

// 接口定义
interface ReviewItem {
  id: number;
  student_sno: string;
  student_name: string;
  semester: string;
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
    // TODO: 替换为实际的API调用
    // const res = await getScoreReviewList({
    //   page: currentPage.value,
    //   page_size: pageSize.value,
    // });
    // reviewList.value = res.data.data.list;
    // total.value = res.data.data.total;

    // 模拟数据
    reviewList.value = [
      {
        id: 1,
        student_sno: "2021001",
        student_name: "张三",
        semester: "2023-2024-1",
        question_type: "academic",
        content: "我的期末考试成绩似乎有误",
        status: "pending",
        apply_time: "2024-01-15 14:30:00",
      },
      {
        id: 2,
        student_sno: "2021002",
        student_name: "李四",
        semester: "2023-2024-1",
        question_type: "moral",
        content: "德育分计算可能有误",
        status: "approved",
        apply_time: "2024-01-10 09:15:00",
        review_comment: "已核实并更正",
        review_time: "2024-01-11 10:20:00",
      },
    ];
    total.value = 2;
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
    if (valid) {
      try {
        // TODO: 替换为实际的API调用
        // const res = await submitScoreReviewResult({
        //   review_id: currentReview.value?.id,
        //   status: reviewForm.value.status,
        //   comment: reviewForm.value.comment,
        // });

        ElMessage.success("审核成功");
        dialogVisible.value = false;
        getReviewList(); // 刷新列表
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

.content-box {
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 4px;
  min-height: 60px;
  line-height: 1.6;
  color: #606266;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-dialog__body) {
  padding: 20px 30px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
