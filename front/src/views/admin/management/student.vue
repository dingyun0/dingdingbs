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
      title="查看详情"
      v-model="visible1"
      width="700px"
      destroy-on-close
    >
      <TableDetail :data="viewData"></TableDetail>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="student-management">
import { ref, reactive } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { studentAllInfoReq, deleteUserReq } from "@/api";
import TableCustom from "@/components/table-custom.vue";
import TableDetail from "@/components/table-detail.vue";
import TableSearch from "@/components/table-search.vue";

// 查询相关
const query = reactive({
  name: "",
});
const searchOpt = ref([{ type: "input", label: "姓名：", prop: "name" }]);
const handleSearch = () => {
  changePage(page.index);
};

// 表格相关
let columns = ref([
  { type: "index", label: "序号", width: 55, align: "center" },
  { prop: "sno", label: "学号", width: 120 },
  { prop: "name", label: "姓名", width: 120 },
  { prop: "department", label: "学院", width: 180 },
  { prop: "major", label: "专业", width: 180 },
  { prop: "grade", label: "年级", width: 100 },
  { prop: "class_name", label: "班级", width: 120 },
  { prop: "joined_time", label: "注册时间", width: 180 },
  { prop: "operator", label: "操作", width: 150 },
]);

const page = reactive({
  index: 1,
  size: 10,
  total: 0,
});

const tableData = ref([]);
const getData = async () => {
  try {
    const res = await studentAllInfoReq({
      page: page.index,
      page_size: page.size,
    });
    if (res.data && res.data.data) {
      tableData.value = res.data.data.list;
      page.total = res.data.data.total;
    }
  } catch (error) {
    console.error("获取学生数据失败:", error);
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
    { prop: "sno", label: "学号" },
    { prop: "name", label: "姓名" },
    { prop: "department", label: "学院" },
    { prop: "major", label: "专业" },
    { prop: "grade", label: "年级" },
    { prop: "class_name", label: "班级" },
    { prop: "joined_time", label: "注册时间" },
  ];
  visible1.value = true;
};

// 删除操作
const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm(
      `确认删除学生 ${row.name} 吗？此操作不可恢复！`,
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
</script>

<style scoped></style>
