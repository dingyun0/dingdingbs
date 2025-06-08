<template>
  <div>
    <table-custom
      ref="tableRef"
      :columns="columns"
      :request="getTableData"
      :table-data="DataList"
      :has-selection="true"
      :has-index="true"
    >
      <template #toolbarBtn>
        <el-button type="primary" @click="handleAdd">添加学院信息</el-button>
      </template>

      <template #operation="scope">
        <el-button type="primary" link @click="handleEdit(scope.rows)">
          编辑
        </el-button>
        <el-button type="danger" link @click="handleDelete(scope.rows)">
          删除
        </el-button>
      </template>
    </table-custom>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      :title="isEdit ? '编辑学院信息' : '添加学院信息'"
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
  </div>
</template>

<script setup lang="ts" name="college">
import { ref, reactive, onBeforeMount } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import TableCustom from "@/components/table-custom.vue";
import TableEdit from "@/components/table-edit.vue";
import {
  getCollegeList,
  addCollegeReq,
  updateCollegeReq,
  deleteCollegeReq,
} from "@/api/college";

interface CollegeData {
  id?: number;
  department: string;
  major: string;
  grade: string;
  department_code: string;
  major_code: string;
  grade_code: string;
  created_at?: string;
  updated_at?: string;
}

const tableRef = ref();
const visible = ref(false);
const isEdit = ref(false);
const rowData = ref<CollegeData>({} as CollegeData);
const DataList = ref<CollegeData[]>([]);

// 表格列配置
const columns = [
  { label: "学院名称", prop: "department" },
  { label: "专业名称", prop: "major" },
  { label: "年级", prop: "grade" },
  { label: "学院代码", prop: "department_code" },
  { label: "专业代码", prop: "major_code" },
  { label: "年级代码", prop: "grade_code" },
  { label: "创建时间", prop: "created_at" },
  { label: "更新时间", prop: "updated_at" },
  { label: "操作", prop: "operation", width: 160, fixed: "right" },
];

// 表单配置
const options = {
  labelWidth: "120px",
  span: 24,
  list: [
    {
      label: "学院名称",
      prop: "department",
      type: "input",
      placeholder: "请输入学院名称",
      required: true,
    },
    {
      label: "专业名称",
      prop: "major",
      type: "input",
      placeholder: "请输入专业名称",
      required: true,
    },
    {
      label: "年级",
      prop: "grade",
      type: "input",
      placeholder: "请输入年级",
      required: true,
    },
    {
      label: "学院代码",
      prop: "department_code",
      type: "input",
      placeholder: "请输入学院代码",
      required: true,
    },
    {
      label: "专业代码",
      prop: "major_code",
      type: "input",
      placeholder: "请输入专业代码",
      required: true,
    },
    {
      label: "年级代码",
      prop: "grade_code",
      type: "input",
      placeholder: "请输入年级代码",
      required: true,
    },
  ],
};

// 获取表格数据
const getTableData = async () => {
  try {
    const res = await getCollegeList();
    // 直接使用返回的数据，因为后端已经格式化好了
    DataList.value = res.data;
  } catch (error) {
    console.error("获取数据失败:", error);
    ElMessage.error("获取数据失败");
  }
};

// 添加学院信息
const handleAdd = () => {
  rowData.value = {} as CollegeData;
  isEdit.value = false;
  visible.value = true;
};

// 编辑学院信息
const handleEdit = (row: CollegeData) => {
  rowData.value = { ...row };
  isEdit.value = true;
  visible.value = true;
};

// 删除学院信息
const handleDelete = async (row: CollegeData) => {
  try {
    await ElMessageBox.confirm("确认删除该学院信息?", "提示", {
      type: "warning",
    });
    const res = await deleteCollegeReq(row.id!);
    if (res.data.code === 200) {
      ElMessage.success("删除成功");
      await getTableData();
    } else {
      ElMessage.error(res.data.msg || "删除失败");
    }
  } catch (error) {
    console.error("删除失败:", error);
    ElMessage.error("删除失败");
  }
};

// 更新数据
const updateData = async (formData: CollegeData) => {
  try {
    let res;
    if (isEdit.value) {
      const updateData = {
        ...formData,
        id: rowData.value.id,
      };
      res = await updateCollegeReq(updateData);
    } else {
      res = await addCollegeReq(formData);
    }

    // 直接使用返回的数据
    if (res.data) {
      ElMessage.success(isEdit.value ? "更新成功" : "添加成功");
      closeDialog();
      await getTableData();
    } else {
      ElMessage.error(res.data.msg || "操作失败");
    }
  } catch (error) {
    console.error("操作失败:", error);
    ElMessage.error("操作失败，请重试");
  }
};

// 关闭对话框
const closeDialog = () => {
  visible.value = false;
  rowData.value = {} as CollegeData;
};

// 初始化时获取数据
onBeforeMount(async () => {
  await getTableData();
});
</script>
