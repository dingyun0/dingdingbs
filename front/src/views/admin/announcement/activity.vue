<template>
  <div>
    <table-custom
      ref="tableRef"
      :columns="columns"
      :request="getTableData"
      :table-data="DataList"
      :has-selection="true"
      :has-index="true"
      :current-page="currentPage"
      :page-size="pageSize"
      :total="total"
      :page-change="handlePageChange"
    >
      <template #toolbarBtn>
        <el-button type="primary" @click="handleAdd">添加活动</el-button>
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
      :title="isEdit ? '编辑活动' : '添加活动'"
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

<script setup lang="ts" name="activity">
import { ref, reactive, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import TableCustom from "@/components/table-custom.vue";
import TableEdit from "@/components/table-edit.vue";
import {
  addActivityReq,
  updateActivityReq,
  deleteActivityReq,
  getActivityListReq,
} from "@/api/activity";

interface ActivityData {
  id?: number;
  title: string;
  content: string;
  publisher: string;
  category: string;
  credits: number;
  deadline: string;
  quota: number;
  status: string;
  publish_date?: string;
}

const tableRef = ref();
const visible = ref(false);
const isEdit = ref(false);
const rowData = ref<ActivityData>({} as ActivityData);
const DataList = ref<ActivityData[]>([]);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 表格列配置
const columns = [
  { label: "活动标题", prop: "title" },
  { label: "活动内容", prop: "content" },
  { label: "发布者", prop: "publisher" },
  { label: "活动类型", prop: "category" },
  { label: "加分数", prop: "credits" },
  { label: "截止时间", prop: "deadline" },
  { label: "名额数量", prop: "quota" },
  { label: "状态", prop: "status" },
  { label: "发布时间", prop: "publish_date" },
  { label: "操作", prop: "operation", width: 160, fixed: "right" },
];

// 表单配置
const options = {
  labelWidth: "120px",
  span: 24,
  list: [
    {
      label: "活动标题",
      prop: "title",
      type: "input",
      placeholder: "请输入活动标题",
      required: true,
    },
    {
      label: "活动内容",
      prop: "content",
      type: "input",
      placeholder: "请输入活动内容",
      required: true,
    },
    {
      label: "发布者",
      prop: "publisher",
      type: "input",
      placeholder: "请输入发布者",
      required: true,
    },
    {
      label: "活动类型",
      prop: "category",
      type: "select",
      options: [
        { label: "学业", value: "academic" },
        { label: "文体", value: "sports" },
        { label: "劳动", value: "labor" },
        { label: "创新", value: "innovation" },
      ],
      required: true,
    },
    {
      label: "加分数",
      prop: "credits",
      type: "number",
      required: true,
    },
    {
      label: "截止时间",
      prop: "deadline",
      type: "date",
      format: "YYYY-MM-DD HH:mm:ss",
      required: true,
    },
    {
      label: "名额数量",
      prop: "quota",
      type: "number",
      required: true,
    },
    {
      label: "状态",
      prop: "status",
      type: "select",
      options: [
        { label: "激活", value: "active" },
        { label: "未激活", value: "inactive" },
      ],
      required: true,
    },
  ],
};

// 获取表格数据
const getTableData = async () => {
  try {
    const res = await getActivityListReq({
      page: currentPage.value,
      page_size: pageSize.value,
    });
    if (res.data.code === 200) {
      // 处理日期格式和数据转换
      DataList.value = res.data.data.list.map((item: any) => ({
        ...item,
        publish_date: new Date(item.publish_date).toLocaleString(),
        deadline: new Date(item.deadline).toLocaleString(),
        category: formatCategory(item.category),
        status: formatStatus(item.status),
      }));
      total.value = res.data.data.total;
    } else {
      ElMessage.error(res.data.msg || "获取数据失败");
    }
  } catch (error) {
    console.error("获取数据失败:", error);
  }
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

// 添加活动
const handleAdd = () => {
  rowData.value = {} as ActivityData;
  isEdit.value = false;
  visible.value = true;
};

// 编辑活动
const handleEdit = (row: any) => {
  // 将中文显示转换回英文值
  const editData = {
    ...row,
    id: row.id, // 确保id被包含
    category: reverseFormatCategory(row.category),
    status: reverseFormatStatus(row.status),
  } as ActivityData;
  rowData.value = editData;
  isEdit.value = true;
  visible.value = true;
};

// 反向转换活动类型（中文转英文）
const reverseFormatCategory = (categoryZh: string) => {
  const reverseCategoryMap: { [key: string]: string } = {
    学业: "academic",
    文体: "sports",
    劳动: "labor",
    创新: "innovation",
  };
  return reverseCategoryMap[categoryZh] || categoryZh;
};

// 反向转换状态（中文转英文）
const reverseFormatStatus = (statusZh: string) => {
  const reverseStatusMap: { [key: string]: string } = {
    激活: "active",
    未激活: "inactive",
  };
  return reverseStatusMap[statusZh] || statusZh;
};

// 删除活动
const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm("确认删除该活动?", "提示", {
      type: "warning",
    });
    await deleteActivityReq(row.id);
    ElMessage.success("删除成功");
    // 重新获取数据
    await getTableData();
  } catch (error) {
    console.error("删除失败:", error);
  }
};

// 更新数据
const updateData = async (formData: any) => {
  try {
    if (isEdit.value) {
      // 确保编辑时包含id
      const updateData = {
        ...formData,
        id: rowData.value.id,
      } as ActivityData;
      await updateActivityReq(updateData);
      ElMessage.success("更新成功");
    } else {
      await addActivityReq(formData);
      ElMessage.success("添加成功");
    }
    closeDialog();
    // 重新获取数据
    await getTableData();
  } catch (error) {
    console.error("操作失败:", error);
    ElMessage.error("操作失败，请重试");
  }
};

// 关闭对话框
const closeDialog = () => {
  visible.value = false;
  rowData.value = {} as ActivityData;
};

// 页码变化处理
const handlePageChange = async (page: number) => {
  currentPage.value = page;
  await getTableData();
};

// 初始化时获取数据
onMounted(async () => {
  await getTableData();
});
</script>
