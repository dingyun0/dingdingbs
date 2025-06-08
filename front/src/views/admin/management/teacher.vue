<template>
  <div>
    <div class="container">
      <TableCustom
        :columns="columns"
        :tableData="tableData"
        :total="page.total"
        :current-page="page.index"
        :page-size="page.size"
        :viewFunc="handleView"
        :delFunc="handleDelete"
        :page-change="changePage"
        :editFunc="handleEdit"
      >
      </TableCustom>
    </div>
    <el-dialog
      title="查看详情"
      v-model="visible1"
      width="700px"
      destroy-on-close
    >
      <TableDetail :data="viewData"></TableDetail>
    </el-dialog>
    <el-dialog
      title="编辑教师信息"
      v-model="visible"
      width="700px"
      destroy-on-close
      :close-on-click-modal="false"
      @close="closeDialog"
    >
      <TableEdit
        :options="options"
        :formData="rowData"
        :edit="isEdit"
        :update="updateData"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="teacher-management">
import { ref, reactive, onBeforeMount } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { teacherAllInfoReq, deleteUserReq, updateTeacherInfo } from "@/api";
import { getCollegeList } from "@/api/college";
import TableCustom from "@/components/table-custom.vue";
import TableDetail from "@/components/table-detail.vue";
import TableSearch from "@/components/table-search.vue";
import TableEdit from "@/components/table-edit.vue";
import { FormOption } from "@/types/form-option";

// 查询相关
const query = reactive({
  name: "",
});

const handleSearch = () => {
  changePage(page.index);
};

// 表格相关
let columns = ref([
  { type: "index", label: "序号", width: 55, align: "center" },
  { prop: "username", label: "姓名", width: 120 },
  { prop: "department", label: "学院", width: 180 },
  { prop: "major", label: "专业", width: 180 },
  { prop: "title", label: "职称", width: 120 },
  { prop: "joined_time", label: "注册时间", width: 180 },
  { prop: "operator", label: "操作", width: 250 },
]);

const page = reactive({
  index: 1,
  size: 10,
  total: 0,
});

const tableData = ref([]);
const getData = async () => {
  try {
    const res = await teacherAllInfoReq({
      page: page.index,
      page_size: page.size,
    });
    if (res.data && res.data.data) {
      tableData.value = res.data.data.list;
      page.total = res.data.data.total;
    }
  } catch (error) {
    console.error("获取教师数据失败:", error);
    ElMessage.error("获取数据失败");
  }
};

// 初始化
getData();

const changePage = async (val: number) => {
  page.index = val;
  await getData();
};

// 查看详情
const visible1 = ref(false);
const viewData = ref({
  row: {},
  list: [],
});

const handleView = (row: any) => {
  viewData.value.row = { ...row };
  viewData.value.list = [
    { prop: "username", label: "姓名" },
    { prop: "department", label: "学院" },
    { prop: "major", label: "专业" },
    { prop: "title", label: "职称" },
    { prop: "joined_time", label: "注册时间" },
  ];
  visible1.value = true;
};

// 删除操作
const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm(
      `确认删除教师 ${row.username} 吗？此操作不可恢复！`,
      "警告",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );
    await deleteUserReq(row.user_id);
    ElMessage.success("删除成功");
    getData();
  } catch (error) {
    if (error !== "cancel") {
      console.error("删除失败:", error);
      ElMessage.error("删除失败");
    }
  }
};

// 存储从API获取的学院数据
const collegeData = ref<any[]>([]);

// 获取学院数据
const fetchCollegeData = async () => {
  try {
    const res = await getCollegeList();
    if (res.data) {
      collegeData.value = res.data;
    }
  } catch (error) {
    console.error("获取学院数据失败:", error);
    ElMessage.error("获取学院数据失败");
  }
};

// 处理学院数据为下拉选项格式
const getDepartments = () => {
  const deptMap = new Map();
  collegeData.value.forEach((item) => {
    if (!deptMap.has(item.department)) {
      deptMap.set(item.department, {
        label: item.department,
        value: item.department,
        majors: new Set(),
      });
    }
    deptMap.get(item.department).majors.add(item.major);
  });
  return Array.from(deptMap.values()).map((dept) => ({
    label: dept.label,
    value: dept.value,
    majors: Array.from(dept.majors),
  }));
};

// 获取指定学院的专业列表
const getMajors = (department: string) => {
  const dept = getDepartments().find((d) => d.value === department);
  if (dept) {
    return dept.majors.map((major) => ({
      label: major as string,
      value: major as string,
    }));
  }
  return [];
};

// 处理学院变更
const handleDepartmentChange = (value: string) => {
  console.log("学院变更为:", value);
  // 更新专业选项
  const majorField = options.value.list.find((item) => item.prop === "major");
  if (majorField) {
    majorField.options = getMajors(value);
  }
  // 清空已选专业
  if (rowData.value) {
    rowData.value.major = "";
  }
};

// 编辑相关
const options = ref<FormOption>({
  labelWidth: "100px",
  span: 12,
  list: [
    {
      type: "input",
      label: "姓名",
      prop: "username",
      required: true,
    },
    {
      type: "select",
      label: "学院",
      prop: "department",
      required: true,
      options: [],
      change: handleDepartmentChange,
    },
    {
      type: "select",
      label: "专业",
      prop: "major",
      required: true,
      options: [],
    },
    {
      type: "input",
      label: "职称",
      prop: "title",
      required: false,
    },
  ],
});

const visible = ref(false);
const isEdit = ref(false);
const rowData = ref<any>({});

// 编辑用户
const handleEdit = (row: any) => {
  console.log("编辑按钮被点击", row);
  rowData.value = {
    id: row.user_id,
    username: row.username,
    department: row.department,
    major: row.major,
    title: row.title,
    roles: "teacher",
  };
  isEdit.value = true;
  visible.value = true;
};

// 更新数据
const updateData = async (formData: any) => {
  try {
    console.log("正在更新数据", formData);
    await updateTeacherInfo({
      id: formData.id,
      name: formData.username,
      department: formData.department,
      major: formData.major,
      title: formData.title,
    });

    ElMessage.success("更新成功");
    visible.value = false;
    getData();
  } catch (error) {
    console.error("更新失败:", error);
    ElMessage.error("更新失败");
  }
};

const closeDialog = () => {
  visible.value = false;
  isEdit.value = false;
  rowData.value = {};
};

// 组件挂载前获取学院数据
onBeforeMount(async () => {
  await fetchCollegeData();
  // 设置学院选项
  const departmentField = options.value.list.find(
    (item) => item.prop === "department"
  );
  if (departmentField) {
    departmentField.options = getDepartments();
  }
  await getData();
});
</script>

<style scoped></style>
