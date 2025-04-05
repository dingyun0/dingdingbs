<template>
  <!-- 成绩疑问对话框 -->
  <el-dialog v-model="reviewDialogVisible" title="提交成绩疑问" width="50%">
    <el-form :model="reviewForm" label-width="100px">
      <el-form-item label="问题类型" required>
        <el-select
          v-model="reviewForm.question_type"
          placeholder="请选择问题类型"
        >
          <el-option label="成绩录入错误" value="input_error" />
          <el-option label="成绩计算错误" value="calculation_error" />
          <el-option label="其他问题" value="other" />
        </el-select>
      </el-form-item>
      <el-form-item label="问题说明" required>
        <el-input
          v-model="reviewForm.content"
          type="textarea"
          :rows="4"
          placeholder="请详细描述您的问题..."
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="reviewDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReview">提交</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { useUserStore } from "@/stores/user";
import { submitScoreReview } from "@/api/scoreReview";

const userStore = useUserStore();

interface ReviewForm {
  student_sno: string;
  student_name: string;
  teacher_id: string;
  semester: string;
  question_type: string;
  content: string;
  status: string;
  apply_time: Date;
  review_time: Date | null;
}

// 成绩疑问对话框数据
const reviewDialogVisible = ref(false);
const reviewForm = ref<ReviewForm>({
  student_sno: userStore.sno,
  student_name: userStore.name,
  teacher_id: "",
  semester: "",
  question_type: "",
  content: "",
  status: "pending",
  apply_time: new Date(),
  review_time: null,
});

// 打开成绩疑问对话框
const openReviewDialog = (teacherId: string, semester: string) => {
  reviewForm.value.teacher_id = teacherId;
  reviewForm.value.semester = semester;
  reviewDialogVisible.value = true;
};

// 提交成绩疑问
const submitReview = async () => {
  if (!reviewForm.value.question_type || !reviewForm.value.content) {
    ElMessage.warning("请填写完整的疑问信息");
    return;
  }

  try {
    const res = await submitScoreReview(reviewForm.value);
    if (res.code === 200) {
      ElMessage.success("提交成功");
      reviewDialogVisible.value = false;
      // 重置表单
      reviewForm.value.question_type = "";
      reviewForm.value.content = "";
    } else {
      ElMessage.error(res.message || "提交失败");
    }
  } catch (error) {
    console.error("提交成绩疑问失败:", error);
    ElMessage.error("提交失败，请稍后重试");
  }
};

defineExpose({
  openReviewDialog,
});
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
