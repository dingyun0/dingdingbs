<template>
  <div class="container">
    <div class="table-container">
      <el-table
        v-if="activityList"
        :data="activityList"
        border
        class="table"
        :default-expand-all="true"
      >
        <el-table-column
          prop="title"
          label="活动标题"
          width="150"
          show-overflow-tooltip
        />
        <el-table-column
          prop="content"
          label="活动内容"
          width="200"
          show-overflow-tooltip
        />
        <el-table-column prop="publisher" label="发布者" width="100" />
        <el-table-column prop="category" label="活动类型" width="100">
          <template #default="scope">
            {{ formatCategory(scope.row.category) }}
          </template>
        </el-table-column>
        <el-table-column prop="credits" label="加分数" width="80" />
        <el-table-column prop="deadline" label="截止时间" width="160">
          <template #default="scope">
            {{ formatDate(scope.row.deadline) }}
          </template>
        </el-table-column>
        <el-table-column prop="quota" label="名额数量" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            {{ formatStatus(scope.row.status) }}
          </template>
        </el-table-column>
        <el-table-column prop="publish_date" label="发布时间" width="160">
          <template #default="scope">
            {{ formatDate(scope.row.publish_date) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button
              type="primary"
              link
              :disabled="scope.row.status === 'inactive'"
              @click="handleApply(scope.row)"
            >
              申请
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-else description="暂无活动信息" />
    </div>

    <!-- 选择老师弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      title="选择申请老师"
      width="50%"
      :close-on-click-modal="false"
    >
      <el-form>
        <el-form-item label="选择老师" required>
          <el-select v-model="selectedTeacher" placeholder="请选择老师">
            <el-option
              v-for="teacher in teacherList"
              :key="teacher.id"
              :label="teacher.name"
              :value="teacher.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { applyActivityReq, getActivityListReq } from "@/api/activity";
import { getTeacherNameReq } from "@/api/index";
import { useUserStore } from "@/store/user";

interface ActivityData {
  title: string;
  content: string;
  publisher: string;
  category: string;
  credits: number;
  deadline: string;
  quota: number;
  status: string;
  publish_date: string;
}

interface TeacherData {
  id: number;
  name: string;
}

const userStore = useUserStore();
const activityList = ref<ActivityData[]>([]);
const teacherList = ref<TeacherData[]>([]);
const selectedTeacher = ref("");
const dialogVisible = ref(false);
const currentActivity = ref<ActivityData | null>(null);

// 格式化日期
const formatDate = (date: string) => {
  return new Date(date).toLocaleString();
};

// 格式化活动类型
const formatCategory = (category: string) => {
  const categoryMap: { [key: string]: string } = {
    academic: "学业",
    sports: "文体",
    labor: "劳动",
    innovation: "创新",
  };
  return categoryMap[category] || category;
};

// 格式化状态
const formatStatus = (status: string) => {
  const statusMap: { [key: string]: string } = {
    active: "激活",
    inactive: "未激活",
  };
  return statusMap[status] || status;
};

// 获取活动列表
const getActivityList = async () => {
  try {
    const res = await getActivityListReq({
      page: 1,
      page_size: 999999, // 获取所有活动
    });
    if (res.data.code === 200) {
      activityList.value = res.data.data.list;
    } else {
      ElMessage.warning(res.data.msg || "获取活动列表失败");
    }
  } catch (error) {
    console.error("获取活动列表失败:", error);
    ElMessage.error("获取活动列表失败");
  }
};

// 获取老师列表
const getTeacherList = async () => {
  try {
    console.log("22222222222222222222222");

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

// 检查活动是否可以申请
const checkActivityAvailable = (activity: ActivityData) => {
  const now = new Date();
  const deadline = new Date(activity.deadline);

  if (deadline < now) {
    return { available: false, reason: "活动已过截止日期" };
  }

  if (activity.quota <= 0) {
    return { available: false, reason: "活动名额已满" };
  }

  return { available: true, reason: "" };
};

// 申请活动
const handleApply = async (row: ActivityData) => {
  const { available, reason } = checkActivityAvailable(row);

  if (!available) {
    ElMessage.warning(`因为${reason}，已经无法申请`);
    return;
  }
  console.log("9999999999999", row);

  // 设置当前活动
  currentActivity.value = row;

  // 获取老师列表
  await getTeacherList();

  // 重置选择的老师
  selectedTeacher.value = "";

  // 显示选择老师的弹窗
  dialogVisible.value = true;
};

// 提交申请
const handleSubmit = async () => {
  if (!selectedTeacher.value) {
    ElMessage.warning("请选择申请老师");
    return;
  }

  if (!currentActivity.value) {
    ElMessage.error("当前活动信息丢失");
    return;
  }

  try {
    console.log("提交申请:", {
      activity_id: currentActivity.value.id,
      activity_title: currentActivity.value.title,
      teacher_id: selectedTeacher.value,
      student_sno: userStore.sno, // 使用学号而不是userId
    });
    console.log("99999999", currentActivity.value.category);

    const res = await applyActivityReq({
      activity_id: currentActivity.value.id,
      activity_title: currentActivity.value.title,
      teacher_id: selectedTeacher.value,
      student_sno: userStore.sno,
      activity_category: currentActivity.value.category,
    });

    ElMessage.success("申请成功");
    dialogVisible.value = false;
    // 重新获取活动列表以更新名额
    await getActivityList();
  } catch (error) {
    console.error("申请失败:", error);
    ElMessage.error("申请失败");
  }
};

onMounted(() => {
  getActivityList();
});
</script>

<style scoped>
.container {
  padding: 20px;
}

.table-container {
  background-color: #fff;
  border-radius: 4px;
  overflow: hidden;
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

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
