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
import { ref, reactive } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { CirclePlusFilled } from "@element-plus/icons-vue";
import { User } from "@/types/user";
import {
  userAllInfoReq,
  updateUserRoleReq,
  deleteUserReq,
  updateTeacherRoleReq,
} from "@/api";
import TableCustom from "@/components/table-custom.vue";
import TableDetail from "@/components/table-detail.vue";
import TableSearch from "@/components/table-search.vue";
import { FormOption, FormOptionList } from "@/types/form-option";
import TableEdit from "@/components/table-edit.vue";

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
getData();

const changePage = async (val: number) => {
  console.log("changePage被调用，新页码:", val);
  page.index = val;
  console.log("page.index更新为:", page.index);
  await getData();
};

// 监听角色选择变化
const handleRoleChange = (value: string) => {
  console.log("角色变更为:", value);

  if (value === "teacher") {
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
        options: [
          { label: "计算机学院", value: "计算机学院" },
          { label: "信息工程学院", value: "信息工程学院" },
        ],
      },
      {
        type: "select",
        label: "专业",
        prop: "major",
        required: true,
        options: [
          { label: "计算机科学与技术", value: "计算机科学与技术" },
          { label: "软件工程", value: "软件工程" },
        ],
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
const rowData = ref({});

// 编辑用户
const handleEdit = (row: User) => {
  console.log("当前用户数据:", row);
  rowData.value = {
    id: row.id,
    roles: row.roles,
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

// 更新数据
const updateData = async (formData: any) => {
  try {
    if (formData.roles === "teacher") {
      // 更新用户角色和教师信息
      await updateTeacherRoleReq({
        id: formData.id,
        roles: formData.roles,
        department: formData.department,
        major: formData.major,
        title: formData.title,
      });
    } else {
      // 仅更新用户角色
      await updateUserRoleReq({
        id: formData.id,
        roles: formData.roles,
      });
    }

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
</script>

<style scoped></style>
