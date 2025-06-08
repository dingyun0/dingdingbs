<template>
  <div class="container">
    <div class="table-container">
      <el-table
        v-if="reviewList.length > 0"
        :data="reviewList"
        border
        style="width: 100%"
      >
        <el-table-column prop="activity_id" label="活动ID" width="80" />
        <el-table-column prop="activity_title" label="活动名称" width="180" />
        <el-table-column prop="student_sno" label="学生学号" width="120" />
        <el-table-column label="活动类型" width="100">
          <template #default="scope">
            {{ scope.row.activity_category }}
          </template>
        </el-table-column>
        <el-table-column label="申请时间" width="160">
          <template #default="scope">
            {{ formatDate(scope.row.apply_time) }}
          </template>
        </el-table-column>
        <el-table-column label="活动分" width="80">
          <template #default="scope">
            {{ scope.row.credits }}
          </template>
        </el-table-column>
        <el-table-column label="审核状态" width="100">
          <template #default="scope">
            {{ formatStatus(scope.row.status) }}
          </template>
        </el-table-column>
        <el-table-column label="证明材料" width="120">
          <template #default="scope">
            <div v-if="hasProofFiles(scope.row)" class="proof-images">
              <el-image
                :src="getFirstProofImage(scope.row)"
                fit="cover"
                class="proof-thumbnail"
                :preview-src-list="getProofImages(scope.row.proof_files)"
                preview-teleported
              >
                <template #error>
                  <div class="image-error">
                    <el-icon><i-ep-picture-failed /></el-icon>
                  </div>
                </template>
              </el-image>
              <span
                v-if="getProofImages(scope.row.proof_files).length > 1"
                class="image-count"
              >
                +{{ getProofImages(scope.row.proof_files).length - 1 }}
              </span>
            </div>
            <span v-else>无材料</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="100">
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
        <el-form-item label="活动类型">
          <span>{{ currentActivity?.activity_category }}</span>
        </el-form-item>
        <el-form-item label="活动分">
          <span>{{ currentActivity?.credits }}</span>
        </el-form-item>
        <el-form-item label="申请时间">
          <span>{{ formatDate(currentActivity?.apply_time) }}</span>
        </el-form-item>
        <el-form-item label="申请描述" v-if="currentActivity?.comment">
          <span class="form-text">{{ currentActivity?.comment }}</span>
        </el-form-item>
        <el-form-item label="证明材料" v-if="hasProofFiles(currentActivity)">
          <div>
            <div class="proof-images-container">
              <el-image
                v-for="(url, index) in getProofImages(
                  currentActivity?.proof_files
                )"
                :key="index"
                :src="url"
                fit="contain"
                class="proof-image"
                :preview-src-list="getProofImages(currentActivity?.proof_files)"
                :initial-index="index"
                preview-teleported
              >
                <template #error>
                  <div class="image-error">
                    <el-icon><i-ep-picture-failed /></el-icon>
                  </div>
                </template>
              </el-image>
            </div>
          </div>
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

// 设置API基础URL
const API_BASE_URL = "http://127.0.0.1:9005";

interface ReviewItem {
  id: number;
  activity_id: number;
  activity_title: string;
  student_sno: string;
  teacher_id: number;
  activity_category: string;
  credits: string;
  status: string;
  apply_time: string;
  review_time?: string;
  review_comment?: string;
  proof_files?: string;
  comment?: string;
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
    已申请: "审核中",
    申请通过: "已通过",
    申请未通过: "未通过",
    审核中: "审核中",
  };
  return statusMap[status] || status;
};

// 检查是否有证明材料
const hasProofFiles = (item: ReviewItem | null): boolean => {
  if (!item) return false;
  return !!item.proof_files && item.proof_files.trim() !== "";
};

// 获取第一张证明图片
const getFirstProofImage = (item: ReviewItem): string => {
  if (!item.proof_files) return "";
  const images = getProofImages(item.proof_files);
  return images.length > 0 ? images[0] : "";
};

// 获取证明图片数组
const getProofImages = (proofFiles: string | undefined): string[] => {
  if (!proofFiles) return [];
  console.log("处理证明图片URL:", proofFiles);

  // 将逗号分隔的URL字符串转换为数组
  return proofFiles
    .split(",")
    .filter((url) => url.trim() !== "")
    .map((url) => {
      // 如果已经是完整URL，直接返回
      if (url.startsWith("http://") || url.startsWith("https://")) {
        return url;
      }

      // 确保URL路径正确（避免双斜杠问题）
      if (url.startsWith("/")) {
        return `${API_BASE_URL}${url}`;
      } else {
        return `${API_BASE_URL}/${url}`;
      }
    });
};

// 获取待审核列表
const getReviewList = async () => {
  try {
    const res = await getReviewListReq();
    if (res.data.code === 200) {
      reviewList.value = res.data.data;
      console.log("审核列表数据:", JSON.stringify(reviewList.value, null, 2));

      // 检查每个项目的proof_files字段
      reviewList.value.forEach((item, index) => {
        console.log(`项目 ${index} 的proof_files:`, item.proof_files);
        if (item.proof_files) {
          console.log("转换后的图片URL:", getProofImages(item.proof_files));
        }
      });
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
  console.log("当前活动详情:", JSON.stringify(row, null, 2));
  console.log("证明材料:", row.proof_files);
  if (row.proof_files) {
    console.log("转换后的图片URL:", getProofImages(row.proof_files));
  }

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
    const res = await reviewActivity({
      review_id: currentActivity.value?.id,
      review_comment: reviewForm.value.review_comment,
      comment: reviewForm.value.comment,
      category: currentActivity.value?.activity_category,
    });

    if (res.data.code === 200) {
      ElMessage.success("审核成功");
      dialogVisible.value = false;
      await getReviewList(); // 刷新列表
    } else {
      ElMessage.error(res.data.msg || "审核失败");
    }
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

.form-text {
  display: block;
  line-height: 1.5;
  word-break: break-word;
  white-space: pre-wrap;
}

.proof-images {
  display: flex;
  align-items: center;
  gap: 5px;
}

.proof-thumbnail {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  object-fit: cover;
  cursor: pointer;
}

.image-count {
  font-size: 12px;
  color: #909399;
  margin-left: 5px;
}

.proof-images-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 8px;
}

.proof-image {
  width: 120px;
  height: 120px;
  border-radius: 4px;
  object-fit: cover;
  cursor: pointer;
  border: 1px solid #ebeef5;
}

.image-error {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background-color: #f5f7fa;
  color: #909399;
  font-size: 20px;
}
</style>
