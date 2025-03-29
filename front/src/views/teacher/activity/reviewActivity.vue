<template>
  <div class="container">
    <div class="table-container">
      <el-table
        v-if="reviewList.length > 0"
        :data="reviewList"
        border
        style="width: 100%"
      >
        <el-table-column prop="activity_id" label="活动ID" width="100" />
        <el-table-column prop="activity_title" label="活动名称" width="200" />
        <el-table-column prop="student_sno" label="学生学号" width="150" />
        <el-table-column prop="apply_time" label="申请时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.apply_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="review_comment" label="审核状态" width="120">
          <template #default="scope">
            {{ formatStatus(scope.row.status) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="200">
          <template #default="scope">
            <el-button
              v-if="scope.row.review_comment === '审核中'"
              type="primary"
              size="small"
              @click="handleReview(scope.row)"
            >
              审核
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-else description="暂无待审核的活动" />
    </div>

    <!-- 审核对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="活动审核"
      width="50%"
      :close-on-click-modal="false"
    >
      <el-form :model="reviewForm" label-width="100px">
        <el-form-item label="活动名称">
          <span>{{ currentActivity?.activity_title }}</span>
        </el-form-item>
        <el-form-item label="申请学生">
          <span>{{ currentActivity?.student_sno }}</span>
        </el-form-item>
        <el-form-item label="申请时间">
          <span>{{ formatDate(currentActivity?.apply_time) }}</span>
        </el-form-item>
        <el-form-item label="审核结果" required>
          <el-radio-group v-model="reviewForm.review_comment">
            <el-radio label="通过">通过</el-radio>
            <el-radio label="不通过">不通过</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="审核意见" required>
          <el-input
            v-model="reviewForm.comment"
            type="textarea"
            :rows="4"
            placeholder="请输入审核意见"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitReview"> 确认 </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import { useUserStore } from "@/store/user";
import { getReviewListReq, reviewActivity } from "@/api/activity";

interface ReviewItem {
  id: number;
  activity_id: number;
  activity_title: string;
  student_sno: string;
  teacher_id: number;
  status: string;
  apply_time: string;
  review_time?: string;
  review_comment?: string;
}

const userStore = useUserStore();
const reviewList = ref<ReviewItem[]>([]);
const dialogVisible = ref(false);
const currentActivity = ref<ReviewItem | null>(null);
const reviewForm = ref({
  review_comment: "",
  comment: "",
});

// 格式化日期
const formatDate = (date: string) => {
  if (!date) return "";
  return new Date(date).toLocaleString();
};

// 格式化状态
const formatStatus = (status: string) => {
  const statusMap: { [key: string]: string } = {
    pending: "审核中",
    approved: "已通过",
    rejected: "未通过",
  };
  return statusMap[status] || status;
};

// 获取待审核列表
// 获取待审核列表
const getReviewList = async () => {
  try {
    const res = await getReviewListReq();
    if (res.data.code === 200) {
      reviewList.value = res.data.data;
    } else {
      ElMessage.warning(res.data.msg || "获取审核列表失败");
    }
  } catch (error) {
    console.error("获取审核列表失败:", error);
    ElMessage.error("获取审核列表失败");
  }
};

// 打开审核对话框
const handleReview = (row: ReviewItem) => {
  currentActivity.value = row;
  reviewForm.value = {
    review_comment: "",
    comment: "",
  };
  dialogVisible.value = true;
};

// 提交审核
const submitReview = async () => {
  if (!reviewForm.value.review_comment) {
    ElMessage.warning("请选择审核结果");
    return;
  }
  if (!reviewForm.value.comment.trim()) {
    ElMessage.warning("请输入审核意见");
    return;
  }

  try {
    // TODO: 替换为实际的API调用
    const res = await reviewActivity({
      review_id: currentActivity.value?.id,
      review_comment: reviewForm.value.review_comment,
      comment: reviewForm.value.comment,
    });

    ElMessage.success("审核成功");
    dialogVisible.value = false;
    await getReviewList(); // 刷新列表
  } catch (error) {
    console.error("审核失败:", error);
    ElMessage.error("审核失败");
  }
};

onMounted(() => {
  getReviewList();
});
</script>

<style scoped>
.container {
  padding: 20px;
}

.table-container {
  background-color: #fff;
  border-radius: 4px;
  padding: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

:deep(.el-form-item__content) span {
  line-height: 32px;
}
</style>
