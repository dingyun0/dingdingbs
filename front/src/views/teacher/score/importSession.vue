<template>
  <div>
    <div class="container">
      <div class="handle-box">
        <el-upload
          action="#"
          :limit="1"
          accept=".xlsx, .xls"
          :show-file-list="false"
          :before-upload="beforeUpload"
          :http-request="handleMany"
        >
          <el-button class="mr10" type="success">批量导入</el-button>
        </el-upload>
        <el-link href="/template_session.xlsx" target="_blank"
          >下载模板</el-link
        >
        <el-button
          type="primary"
          @click="handleSave"
          :disabled="!tableData.length"
          style="margin-left: 10px"
        >
          保存课程信息
        </el-button>
      </div>
      <el-table
        :data="tableData"
        border
        class="table"
        header-cell-class-name="table-header"
      >
        <el-table-column
          prop="course_id"
          label="课程ID"
          width="80"
          align="center"
        ></el-table-column>
        <el-table-column prop="course_name" label="课程名"></el-table-column>
        <el-table-column prop="credit" label="学分"></el-table-column>
        <el-table-column prop="hours" label="学时"></el-table-column>
        <el-table-column prop="nature" label="课程性质"></el-table-column>
        <el-table-column prop="college" label="所属学院"></el-table-column>
        <el-table-column prop="major" label="所属专业"></el-table-column>
        <el-table-column prop="grade" label="适用年级"></el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts" name="session">
import { UploadProps } from "element-plus";
import { ref, onMounted } from "vue";
import * as XLSX from "xlsx";
import { saveSessionReq } from "@/api/session";
import { ElMessage } from "element-plus";

interface TableItem {
  id: number;
  course_id: string;
  course_name: string;
  credit: string;
  hours: string;
  nature: string;
  college: string;
  major: string;
  grade: string;
}

const tableData = ref<TableItem[]>([]);
// 获取表格数据
const getData = () => {
  tableData.value = [];
};
getData();

const importList = ref<any>([]);
const beforeUpload: UploadProps["beforeUpload"] = async (rawFile) => {
  importList.value = await analysisExcel(rawFile);
  return true;
};
const analysisExcel = (file: any) => {
  return new Promise(function (resolve, reject) {
    const reader = new FileReader();
    reader.onload = function (e: any) {
      const data = e.target.result;
      let datajson = XLSX.read(data, {
        type: "binary",
      });

      const sheetName = datajson.SheetNames[0];
      const result = XLSX.utils.sheet_to_json(datajson.Sheets[sheetName]);
      resolve(result);
    };
    reader.readAsBinaryString(file);
  });
};

const handleMany = async () => {
  const list = importList.value.map((item: any, index: number) => {
    return {
      id: index + 1,
      course_id: String(item["课程ID"]),
      course_name: item["课程名"],
      credit: String(item["学分"]),
      hours: String(item["学时"]),
      nature: item["课程性质"],
      college: item["所属学院"],
      major: item["所属专业"],
      grade: item["适用年级"],
    };
  });
  tableData.value.push(...list);
  checkButtonState();
};

// 添加这个函数来检查按钮状态
const checkButtonState = () => {
  console.log("tableData长度:", tableData.value.length);
  console.log("按钮是否禁用:", !tableData.length);
};

// 在数据加载后调用
onMounted(() => {
  checkButtonState();
});

const handleSave = async () => {
  try {
    const data = {
      sessions: tableData.value.map((item) => ({
        course_id: item.course_id,
        course_name: item.course_name,
        credit: item.credit,
        hours: item.hours,
        nature: item.nature,
        college: item.college,
        major: item.major,
        grade: item.grade,
      })),
    };
    console.log("发送的数据结构:", JSON.stringify(data, null, 2)); // 检查发送的数据
    await saveSessionReq(data);
    ElMessage.success("保存成功");
    tableData.value = []; // 清空表格数据
  } catch (error) {
    console.error("保存失败:", error);
    ElMessage.error(error.response?.data?.msg || "保存失败");
  }
};
</script>

<style scoped>
.handle-box {
  display: flex;
  margin-bottom: 20px;
}

.table {
  width: 100%;
  font-size: 14px;
}
</style>
