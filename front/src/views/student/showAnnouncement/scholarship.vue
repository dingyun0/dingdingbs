<template>
  <div>
    <table-custom
      ref="tableRef"
      :columns="columns"
      :request="getTableData"
      :table-data="DataList"
      :has-selection="false"
      :has-index="true"
      :current-page="currentPage"
      :page-size="pageSize"
      :total="total"
      :page-change="handlePageChange"
    >
    </table-custom>
  </div>
</template>

<script setup lang="ts" name="notice-announcement">
import { ref, reactive, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import TableCustom from "@/components/table-custom.vue";
import TableEdit from "@/components/table-edit.vue";
import {
  addAnnouncementReq,
  updateAnnouncementReq,
  deleteAnnouncementReq,
  getAnnouncementListReq,
} from "@/api/announcement";

const tableRef = ref();
const visible = ref(false);
const isEdit = ref(false);
const rowData = ref({});
const DataList = ref([]);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 表格列配置 - 移除操作列
const columns = [
  { label: "标题", prop: "title" },
  { label: "内容", prop: "content" },
  { label: "发布者", prop: "publisher" },
  { label: "类型", prop: "type" },
  { label: "状态", prop: "status" },
  { label: "发布时间", prop: "publish_date" },
];

// 表单配置
const options = {
  labelWidth: "120px",
  span: 24,
  list: [
    {
      label: "标题",
      prop: "title",
      type: "input",
      placeholder: "请输入公告标题",
      required: true,
    },
    {
      label: "内容",
      prop: "content",
      type: "input",
      placeholder: "请输入公告内容",
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
      label: "类型",
      prop: "type",
      type: "select",
      options: [
        { label: "学校公告", value: "school" },
        { label: "奖学金公告", value: "scholarship" },
        { label: "活动公告", value: "activate" },
      ],
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
    const res = await getAnnouncementListReq({
      page: 1, // 获取第一页
      page_size: 999999, // 设置一个足够大的数以获取所有数据
    });
    if (res.data.code === 200) {
      // 过滤出奖学金公告
      const allScholarshipAnnouncements = res.data.data.list.filter(
        (item: any) => item.type === "scholarship"
      );

      // 计算总数
      total.value = allScholarshipAnnouncements.length;

      // 计算当前页的数据
      const startIndex = (currentPage.value - 1) * pageSize.value;
      const endIndex = startIndex + pageSize.value;
      DataList.value = allScholarshipAnnouncements.slice(startIndex, endIndex);
    } else {
      ElMessage.error(res.data.msg || "获取数据失败");
    }
  } catch (error) {
    console.error("获取数据失败:", error);
  }
};

// 添加公告
const handleAdd = () => {
  rowData.value = {};
  isEdit.value = false;
  visible.value = true;
};
// 编辑公告
const handleEdit = (row: any) => {
  rowData.value = { ...row };
  isEdit.value = true;
  visible.value = true;
};

// 删除公告
const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm("确认删除该公告?", "提示", {
      type: "warning",
    });
    await deleteAnnouncementReq(row.id);
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
      await updateAnnouncementReq(formData);
      ElMessage.success("更新成功");
    } else {
      await addAnnouncementReq(formData);
      ElMessage.success("添加成功");
    }
    closeDialog();
    // 重新获取数据
    await getTableData();
  } catch (error) {
    console.error("操作失败:", error);
  }
};

// 关闭对话框
const closeDialog = () => {
  visible.value = false;
  rowData.value = {};
};

// 页码变化处理
const handlePageChange = async (page: number) => {
  console.log("222", page);

  currentPage.value = page;
  await getTableData();
};

// 初始化时获取数据
onMounted(async () => {
  await getTableData();
});
</script>
