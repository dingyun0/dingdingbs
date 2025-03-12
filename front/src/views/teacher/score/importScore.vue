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
        <el-link href="/template.xlsx" target="_blank">下载模板</el-link>
        <el-button
          type="primary"
          @click="handleSave"
          :disabled="!tableData.length"
          style="margin-left: 10px"
        >
          保存成绩
        </el-button>
      </div>
      <el-table
        :data="tableData"
        border
        class="table"
        header-cell-class-name="table-header"
      >
        <el-table-column
          prop="id"
          label="ID"
          width="55"
          align="center"
        ></el-table-column>
        <el-table-column prop="sno" label="学号"></el-table-column>
        <el-table-column prop="name" label="姓名"></el-table-column>
        <el-table-column prop="class_name" label="班级"></el-table-column>

        <el-table-column
          prop="操作系统课程设计成绩"
          label="操作系统课程设计成绩"
        ></el-table-column>
        <el-table-column
          prop="无线网络技术成绩"
          label="无线网络技术成绩"
        ></el-table-column>
        <el-table-column
          prop="计算机网络课程设计"
          label="计算机网络课程设计"
        ></el-table-column>
        <el-table-column prop="操作系统" label="操作系统"></el-table-column>
        <el-table-column
          prop="人工智能与网络技术学科前沿"
          label="人工智能与网络技术学科前沿"
        ></el-table-column>
        <el-table-column
          prop="信息安全原理及应用"
          label="信息安全原理及应用"
        ></el-table-column>
        <el-table-column
          prop="Linux操作系统"
          label="Linux操作系统"
        ></el-table-column>
        <el-table-column
          prop="Java程序设计"
          label="Java程序设计"
        ></el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts" name="import">
import { UploadProps } from "element-plus";
import { ref, reactive, onMounted } from "vue";
import * as XLSX from "xlsx";
import { saveScoreReq } from "@/api/score";
import { ElMessage } from "element-plus";

interface TableItem {
  id: number;
  name: string;
  sno: string;
  class_name: string;
  操作系统课程设计成绩: string;
  无线网络技术成绩: string;
  计算机网络课程设计: string;
  操作系统: string;
  人工智能与网络技术学科前沿: string;
  信息安全原理及应用: string;
  Linux操作系统: string;
  Java程序设计: string;
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
//
const handleMany = async () => {
  const list = importList.value.map((item: any, index: number) => {
    return {
      id: index + 1,
      name: item["姓名"],
      sno: String(item["学号"]),
      class_name: item["班级"],
      操作系统课程设计成绩: String(item["操作系统课程设计成绩"]),
      无线网络技术成绩: String(item["无线网络技术成绩"]),
      计算机网络课程设计: String(item["计算机网络课程设计"]),
      操作系统: String(item["操作系统"]),
      人工智能与网络技术学科前沿: String(
        item["人工智能与网络技术学科前沿（创新创业教育）"]
      ),
      信息安全原理及应用: String(item["信息安全原理及应用"]),
      Linux操作系统: String(item["Linux 操作系统"]),
      Java程序设计: String(item["Java 程序设计"]),
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
  console.log("handleSave被调用");
  try {
    console.log("11111111111111111111111");

    console.log("发送的数据:", tableData.value);

    const data = {
      scores: tableData.value.map((item) => ({
        name: item.name,
        sno: item.sno,
        class_name: item.class_name,
        操作系统课程设计成绩: item.操作系统课程设计成绩,
        无线网络技术成绩: item.无线网络技术成绩,
        计算机网络课程设计: item.计算机网络课程设计,
        操作系统: item.操作系统,
        人工智能与网络技术学科前沿: item.人工智能与网络技术学科前沿,
        信息安全原理及应用: item.信息安全原理及应用,
        Linux操作系统: item.Linux操作系统,
        Java程序设计: item.Java程序设计,
      })),
    };
    console.log("发送的数据结构:", JSON.stringify(data, null, 2));
    await saveScoreReq(data);
    ElMessage.success("保存成功");
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
