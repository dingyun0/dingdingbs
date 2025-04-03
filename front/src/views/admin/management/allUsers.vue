<template>
  <div>
    <TableSearch :query="query" :options="searchOpt" :search="handleSearch" />
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
      :title="isEdit ? '编辑' : '新增'"
      v-model="visible"
      width="700px"
      destroy-on-close
      :close-on-click-modal="false"
      @close="closeDialog"
    >
      <TableEdit
        :form-data="rowData"
        :options="options"
        :edit="isEdit"
        :update="updateData"
      />
    </el-dialog>
    <el-dialog
      title="查看详情"
      v-model="visible1"
      width="700px"
      destroy-on-close
    >
      <TableDetail :data="viewData"></TableDetail>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="system-user">
import { ref, reactive, onBeforeMount } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { CirclePlusFilled } from "@element-plus/icons-vue";
import { User } from "@/types/user";
import {
  userAllInfoReq,
  updateUserRoleReq,
  deleteUserReq,
  updateTeacherRoleReq,
} from "@/api";
import { getCollegeList } from "@/api/college";
import TableCustom from "@/components/table-custom.vue";
import TableDetail from "@/components/table-detail.vue";
import TableSearch from "@/components/table-search.vue";
import { FormOption, FormOptionList } from "@/types/form-option";
import TableEdit from "@/components/table-edit.vue";

// 存储从API获取的学院数据
const collegeData = ref<any[]>([]);
interface EditUserData {
  id?: number;
  username?: string;
  roles?: string | string[];
  department?: string;
  major?: string;
  title?: string;
  teacher_id?: string;
}
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
  console.log("拿到的学院是", department);

  const dept = getDepartments().find((d) => d.value === department);
  if (dept) {
    return dept.majors.map((major) => ({
      label: major as string,
      value: major as string,
    }));
  }
  return [];
};

// 查询相关
const query = reactive({
  name: "",
});
const searchOpt = ref<FormOptionList[]>([
  { type: "input", label: "用户名：", prop: "name" },
]);
const handleSearch = () => {
  changePage(page.index);
};

// 表格相关
let columns = ref([
  { type: "index", label: "序号", width: 55, align: "center" },
  { prop: "username", label: "用户名" },
  { prop: "roles", label: "角色" },
  { prop: "joined_time", label: "注册时间" },
  { prop: "last_login_time", label: "最后登录时间" },
  { prop: "operator", label: "操作", width: 250 },
]);
const page = reactive({
  index: 1,
  size: 10,
  total: 0,
});
const tableData = ref<User[]>([]);
const getData = async () => {
  try {
    console.log("正在获取页码:", page.index, "的数据");
    const res = await userAllInfoReq({
      page: page.index,
      page_size: page.size,
    });
    console.log("获取到的数据:", res.data);

    if (res.data && res.data.data) {
      tableData.value = res.data.data.list;
      page.total = res.data.data.total;
      console.log("获取到数据:", tableData.value);
    }
  } catch (error) {
    console.error("获取用户数据失败:", error);
    ElMessage.error("获取用户数据失败");
  }
};

const changePage = async (val: number) => {
  console.log("changePage被调用，新页码:", val);
  page.index = val;
  console.log("page.index更新为:", page.index);
  await getData();
};

// 监听角色选择变化
const handleRoleChange = (value: string) => {
  console.log("角色变更为:", value);
  // 更新 rowData 中的角色
  if (rowData.value) {
    rowData.value.roles = [value];
  }

  if (value === "teacher") {
    const departments = getDepartments();
    options.value.list = [
      {
        type: "select",
        label: "角色",
        prop: "roles",
        required: true,
        options: [
          { label: "管理员", value: "admin" },
          { label: "教师", value: "teacher" },
          { label: "学生", value: "student" },
        ],
        change: handleRoleChange,
      },
      {
        type: "input",
        label: "教师ID",
        prop: "teacher_id",
        required: true,
        placeholder: "请输入教师ID",
      },
      {
        type: "select",
        label: "学院",
        prop: "department",
        required: true,
        options: departments,
        change: handleDepartmentChange as (value: any) => void,
      },
      {
        type: "select",
        label: "专业",
        prop: "major",
        required: true,
        options: rowData.value.department
          ? getMajors(rowData.value.department)
          : [],
      },
      {
        type: "input",
        label: "职称",
        prop: "title",
        required: false,
        placeholder: "请输入职称",
      },
    ];
  } else {
    // 如果不是教师角色，只保留角色选择
    options.value.list = [
      {
        type: "select",
        label: "角色",
        prop: "roles",
        required: true,
        options: [
          { label: "管理员", value: "admin" },
          { label: "教师", value: "teacher" },
          { label: "学生", value: "student" },
        ],
        change: handleRoleChange,
      },
    ];
  }
};

// 新增/编辑弹窗相关
let options = ref<FormOption>({
  labelWidth: "100px",
  span: 12,
  list: [
    {
      type: "select",
      label: "角色",
      prop: "roles",
      required: true,
      options: [
        { label: "管理员", value: "admin" },
        { label: "教师", value: "teacher" },
        { label: "学生", value: "student" },
      ],
      change: handleRoleChange,
    },
  ],
});
const visible = ref(false);
const isEdit = ref(false);
const rowData = ref<EditUserData>({});

// 编辑用户
const handleEdit = (row) => {
  console.log("当前用户数据:", row);
  rowData.value = {
    id: row.id,
    username: row.username,
    roles: row.roles,
    department: row.department,
    major: row.major,
    title: row.title,
    teacher_id: row.teacher_id,
  };
  console.log("rowData:", rowData.value);
  isEdit.value = true;
  visible.value = true;

  // 手动触发角色变更
  setTimeout(() => {
    if (row.roles === "teacher") {
      handleRoleChange("teacher");
    }
  }, 100);
};

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

// 更新数据
const updateData = async (formData: any) => {
  try {
    console.log("提交的表单数据:", formData);

    // 统一使用 updateTeacherRoleReq 进行更新
    await updateTeacherRoleReq({
      id: formData.id,
      name: formData.username,
      roles: formData.roles,
      department: formData.department || "",
      major: formData.major || "",
      title: formData.title || "",
      teacher_id: formData.teacher_id || "",
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

// 查看详情弹窗相关
const visible1 = ref(false);
const viewData = ref({
  row: {},
  list: [],
});
const handleView = (row: User) => {
  viewData.value.row = { ...row };
  viewData.value.list = [
    {
      prop: "id",
      label: "用户ID",
    },
    {
      prop: "username",
      label: "用户名",
    },
    {
      prop: "roles",
      label: "角色",
    },
    {
      prop: "joined_time",
      label: "注册时间",
    },
    {
      prop: "last_login_time",
      label: "最后登录时间",
    },
    {
      prop: "sno",
      label: "学号",
    },
  ];
  visible1.value = true;
};

// 删除相关
const handleDelete = async (row: User) => {
  try {
    await ElMessageBox.confirm(
      `确认删除用户 ${row.username} 吗？此操作不可恢复！`,
      "警告",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );

    await deleteUserReq(row.id);
    ElMessage.success("删除成功");
    // 重新获取数据
    getData();
  } catch (error) {
    if (error !== "cancel") {
      console.error("删除用户失败:", error);
      ElMessage.error("删除用户失败");
    }
  }
};

// 组件挂载前获取学院数据
onBeforeMount(async () => {
  await fetchCollegeData();
  await getData();
});
</script>

<style scoped></style>
