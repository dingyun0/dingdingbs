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
      // 过滤出活动公告
      const allActivateAnnouncements = res.data.data.list.filter(
        (item: any) => item.type === "activate"
      );

      // 计算总数
      total.value = allActivateAnnouncements.length;

      // 计算当前页的数据
      const startIndex = (currentPage.value - 1) * pageSize.value;
      const endIndex = startIndex + pageSize.value;
      DataList.value = allActivateAnnouncements.slice(startIndex, endIndex);
    } else {
      ElMessage.error(res.data.msg || "获取数据失败");
    }
  } catch (error) {
    console.error("获取数据失败:", error);
  }
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
