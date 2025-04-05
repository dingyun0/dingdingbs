<template>
  <div class="container">
    <div class="table-container">
      <div class="header-actions">
        <el-button type="primary" @click="handleApplyReview">
          对成绩有疑惑？提出申请
        </el-button>
      </div>

      <el-table
        v-if="studentInfo"
        :data="[studentInfo]"
        border
        class="table"
        :default-expand-all="true"
        row-key="sno"
      >
        <!-- 固定列 -->
        <el-table-column prop="sno" label="学号" width="100" fixed />
        <el-table-column prop="name" label="姓名" width="80" fixed />
        <el-table-column prop="department" label="学院" width="120" fixed />
        <el-table-column prop="major" label="专业" width="120" fixed />
        <el-table-column prop="grade" label="年级" width="80" fixed />

        <!-- 动态课程列 -->
        <el-table-column
          v-for="course in courseColumns"
          :key="course.prop"
          :prop="course.prop"
          :label="course.label"
          width="150"
          show-overflow-tooltip
        />

        <!-- 固定的计算列 -->
        <el-table-column prop="credit_gpa" label="学分绩点" width="100" />
        <el-table-column prop="year_gpa" label="学年绩点" width="100" />
        <el-table-column prop="comprehensive" label="学业分" width="100" />
        <el-table-column prop="academic" label="学业分加分" width="100" />
        <el-table-column prop="labor" label="劳动分加分" width="100" />
        <el-table-column prop="sports" label="文体分加分" width="100" />
        <el-table-column prop="innovation" label="思想分加分" width="100" />
        <el-table-column prop="zongce" label="综合测评" width="100" />
        <el-table-column prop="排名" label="专业排名" width="100" />
        <el-table-column prop="获奖情况" label="获奖情况" width="100" />
      </el-table>
      <el-empty v-else description="暂无综合测评信息" />
    </div>

    <!-- 成绩疑问申请对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="提交成绩疑问"
      width="50%"
      :close-on-click-modal="false"
    >
      <el-form
        ref="reviewFormRef"
        :model="reviewForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="选择老师" prop="teacher_id">
          <el-select
            v-model="reviewForm.teacher_id"
            placeholder="请选择老师"
            style="width: 100%"
          >
            <el-option
              v-for="teacher in teacherList"
              :key="teacher.id"
              :label="teacher.name"
              :value="teacher.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="疑问类型" prop="question_type">
          <el-select
            v-model="reviewForm.question_type"
            placeholder="请选择疑问类型"
            style="width: 100%"
          >
            <el-option label="学业成绩" value="academic" />
            <el-option label="活动成绩" value="activity" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="疑问说明" prop="content">
          <el-input
            v-model="reviewForm.content"
            type="textarea"
            :rows="4"
            placeholder="请详细说明您的疑问..."
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitReview">提交</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getStudentTestBySno } from "@/api/comprehensive-test";
import { getFilteredCoursesReq } from "@/api/session";
import { getTeacherNameReq } from "@/api/index";
import { getScoreReviewReq } from "@/api/score";
import { useUserStore } from "@/store/user";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";

const studentInfo = ref(null);
const courseColumns = ref([]);
const userStore = useUserStore();
const dialogVisible = ref(false);
const teacherList = ref([]);

// 表单相关
const reviewFormRef = ref<FormInstance>();
const reviewForm = ref({
  teacher_id: "",
  question_type: "",
  content: "",
});

const rules: FormRules = {
  teacher_id: [{ required: true, message: "请选择老师", trigger: "change" }],
  question_type: [
    { required: true, message: "请选择疑问类型", trigger: "change" },
  ],
  content: [{ required: true, message: "请输入疑问说明", trigger: "blur" }],
};

// 获取老师列表
const getTeacherList = async () => {
  try {
    const res = await getTeacherNameReq();
    if (res.data.code === 200) {
      teacherList.value = res.data.data;
    } else {
      ElMessage.warning(res.data.msg || "获取老师列表失败");
    }
  } catch (error) {
    console.error("获取老师列表失败:", error);
    ElMessage.error("获取老师列表失败");
  }
};

// 处理提交疑问申请
const handleApplyReview = () => {
  if (!studentInfo.value) {
    ElMessage.warning("请先获取成绩信息");
    return;
  }
  reviewForm.value = {
    teacher_id: "",
    question_type: "",
    content: "",
  };
  dialogVisible.value = true;
  getTeacherList();
};

// 提交疑问申请
const submitReview = async () => {
  if (!reviewFormRef.value) return;

  await reviewFormRef.value.validate(async (valid) => {
    if (valid && studentInfo.value) {
      try {
        const res = await getScoreReviewReq({
          student_sno: studentInfo.value.sno,
          student_name: studentInfo.value.name,
          teacher_id: reviewForm.value.teacher_id,
          question_type: reviewForm.value.question_type,
          content: reviewForm.value.content,
        });

        if (res.data.code === 200) {
          ElMessage.success("提交成功");
          dialogVisible.value = false;
        } else {
          ElMessage.warning(res.data.message || "提交失败");
        }
      } catch (error) {
        console.error("提交失败:", error);
        ElMessage.error("提交失败");
      }
    }
  });
};

// 获取课程列表
const getCourseColumns = async (
  department: string,
  major: string,
  grade: string
) => {
  try {
    const res = await getFilteredCoursesReq({
      department,
      major,
      grade,
    });

    if (res.data.code === 200) {
      courseColumns.value = res.data.data.map((course) => ({
        prop: course.course_name,
        label: course.course_name,
      }));
    }
  } catch (error) {
    console.error("获取课程列表失败:", error);
    ElMessage.error("获取课程列表失败");
  }
};

// 获取学生综测信息
const getStudentInfo = async () => {
  try {
    const sno = userStore.sno; // 修改为使用 userId
    if (!sno) {
      ElMessage.warning("当前用户无学号信息");
      return;
    }

    const res = await getStudentTestBySno(sno);
    if (res.data.code === 200 && res.data.data) {
      studentInfo.value = res.data.data;
      // 获取该学生对应的课程列表
      await getCourseColumns(
        res.data.data.department,
        res.data.data.major,
        res.data.data.grade
      );
    } else {
      ElMessage.warning(res.data.message || "暂无综合测评信息");
    }
  } catch (error) {
    console.error("获取学生信息失败:", error);
    ElMessage.error("获取学生信息失败");
  }
};

onMounted(() => {
  getStudentInfo();
});
</script>

<style scoped>
.container {
  padding: 20px;
}

.table-container {
  background-color: #fff;
  border-radius: 4px;
  overflow: auto;
}

.header-actions {
  padding: 16px;
  border-bottom: 1px solid #ebeef5;
}

.table {
  width: 100%;
}

:deep(.el-table__header) {
  font-weight: bold;
  background-color: #f5f7fa;
}

:deep(.el-table__row) {
  cursor: default;
}

:deep(.el-table .cell) {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

:deep(.el-table__fixed) {
  height: 100% !important;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-dialog__body) {
  padding: 20px 30px;
}
</style>
