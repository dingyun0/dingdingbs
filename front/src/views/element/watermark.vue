<template>
  <div class="container">
    <div class="table-container">
      <el-table
        v-if="studentInfo"
        :data="[studentInfo]"
        border
        class="table"
        :default-expand-all="true"
        row-key="sno"
        :tree-props="{ children: 'children' }"
      >
        <el-table-column prop="sno" label="学号" width="100" />
        <el-table-column prop="name" label="姓名" width="80" />
        <el-table-column prop="class_name" label="班级" width="100" />
        <el-table-column
          prop="操作系统课程设计成绩"
          label="操作系统课程设计"
          width="150"
          show-overflow-tooltip
        />
        <el-table-column
          prop="无线网络技术成绩"
          label="无线网络技术"
          width="120"
          show-overflow-tooltip
        />
        <el-table-column
          prop="计算机网络课程设计"
          label="计算机网络课程设计"
          width="150"
          show-overflow-tooltip
        />
        <el-table-column
          prop="操作系统"
          label="操作系统"
          width="100"
          show-overflow-tooltip
        />
        <el-table-column
          prop="人工智能与网络技术学科前沿"
          label="人工智能与网络技术"
          width="150"
          show-overflow-tooltip
        />
        <el-table-column
          prop="信息安全原理及应用"
          label="信息安全"
          width="100"
          show-overflow-tooltip
        />
        <el-table-column
          prop="Linux操作系统"
          label="Linux"
          width="100"
          show-overflow-tooltip
        />
        <el-table-column
          prop="Java程序设计"
          label="Java"
          width="100"
          show-overflow-tooltip
        />
        <el-table-column
          prop="credit_gpa"
          label="学分绩点"
          width="100"
          show-overflow-tooltip
        />
        <el-table-column
          prop="year_gpa"
          label="学年绩点"
          width="100"
          show-overflow-tooltip
        />
        <el-table-column
          prop="comprehensive_score"
          label="学业分成绩"
          width="100"
          show-overflow-tooltip
        />
      </el-table>
      <el-empty v-else description="暂无学业分信息" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getStudentTestBySno } from "@/api/comprehensive-test";
import { useUserStore } from "@/store/user";
import { ElMessage } from "element-plus";

const studentInfo = ref(null);
const userStore = useUserStore();

const getStudentInfo = async () => {
  try {
    const sno = userStore.sno;
    if (!sno) {
      ElMessage.warning("当前用户无学号信息");
      return;
    }
    const res = await getStudentTestBySno(sno);
    if (res.data.code === 200) {
      studentInfo.value = res.data.data;
    } else {
      ElMessage.warning(res.data.message);
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
</style>
