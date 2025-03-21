<template>
  <div>
    <div class="container">
      <div class="handle-box">
        <el-button class="mr10" type="primary" @click="showImportDialog">
          填写成绩基本信息
        </el-button>
        <el-upload
          ref="uploadRef"
          action="#"
          :limit="1"
          accept=".xlsx, .xls"
          :show-file-list="false"
          :before-upload="beforeUpload"
          :http-request="handleMany"
        >
          <el-button class="mr10" type="success" :disabled="!hasSetBasicInfo"
            >批量导入</el-button
          >
        </el-upload>
        <el-button
          link
          type="primary"
          @click="generateTemplate"
          :disabled="!hasSetBasicInfo"
        >
          下载模板
        </el-button>
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
          v-for="col in columns"
          :key="col.prop"
          :prop="col.prop"
          :label="col.label"
          :width="col.width"
          :align="col.align"
        >
        </el-table-column>
      </el-table>
    </div>

    <el-dialog
      title="填写成绩基本信息"
      v-model="dialogVisible"
      width="30%"
      :close-on-click-modal="false"
    >
      <el-form :model="filterForm" label-width="100px">
        <el-form-item label="学院">
          <el-select
            v-model="filterForm.department"
            placeholder="请选择学院"
            style="width: 100%"
          >
            <el-option
              v-for="item in options.colleges"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="专业">
          <el-select
            v-model="filterForm.major"
            placeholder="请选择专业"
            style="width: 100%"
          >
            <el-option
              v-for="item in options.majors"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="年级">
          <el-select
            v-model="filterForm.grade"
            placeholder="请选择年级"
            style="width: 100%"
          >
            <el-option
              v-for="item in options.grades"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleConfirmBasicInfo"
            >确定</el-button
          >
        </span>
      </template>
    </el-dialog>

    <el-upload
      ref="uploadRef"
      action="#"
      :limit="1"
      accept=".xlsx, .xls"
      :show-file-list="false"
      :before-upload="beforeUpload"
      :http-request="handleMany"
      style="display: none"
    >
    </el-upload>
  </div>
</template>

<script setup lang="ts" name="import">
import { UploadProps, UploadInstance } from "element-plus";
import { ref, reactive, onMounted, computed } from "vue";
import * as XLSX from "xlsx";
import { saveScoreReq } from "@/api/score";
import { ElMessage } from "element-plus";
import { getSessionOptionsReq, getFilteredCoursesReq } from "@/api/session";
import {
  SessionOptionsResponse,
  FilteredCoursesResponse,
} from "@/types/session";

// interface TableItem {
//   id: number;
//   name: string;
//   sno: string;
//   class_name: string;
//   操作系统课程设计成绩: string;
//   无线网络技术成绩: string;
//   计算机网络课程设计: string;
//   操作系统: string;
//   人工智能与网络技术学科前沿: string;
//   信息安全原理及应用: string;
//   Linux操作系统: string;
//   Java程序设计: string;
// }

const tableData = ref([]);
const dialogVisible = ref(false);
const uploadRef = ref<UploadInstance>();

// 筛选表单数据
const filterForm = ref({
  department: "",
  major: "",
  grade: "",
});

const options = ref<{
  colleges: string[];
  majors: string[];
  grades: string[];
}>({
  colleges: [],
  majors: [],
  grades: [],
});

// 动态列配置
const columns = ref([
  { prop: "id", label: "ID", width: "55", align: "center" },
  { prop: "sno", label: "学号" },
  { prop: "name", label: "姓名" },
  { prop: "class_name", label: "班级" },
]);

// 获取选项数据
const getOptions = async () => {
  try {
    const res = await getSessionOptionsReq();
    console.log("API返回数据:", res);

    if (res.code === 200) {
      options.value = res.data;
      console.log("选项数据:", options.value);
    } else {
      ElMessage.error(res.message || "获取选项失败");
    }
  } catch (error) {
    console.error("获取选项失败:", error);
    ElMessage.error("获取选项失败");
  }
};

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
    const baseInfo = {
      id: index + 1,
      name: item["姓名"],
      sno: String(item["学号"]),
      class_name: item["班级"],
    };

    // 动态添加课程成绩
    columns.value.forEach((col) => {
      if (!["id", "sno", "name", "class_name"].includes(col.prop)) {
        baseInfo[col.prop] = String(item[col.label] || "");
      }
    });

    return baseInfo;
  });
  tableData.value.push(...list);
  checkButtonState();
};

// 添加这个函数来检查按钮状态
const checkButtonState = () => {
  console.log("tableData长度:", tableData.value.length);
  console.log("按钮是否禁用:", !tableData.value.length);
};

// 在数据加载后调用
onMounted(() => {
  getOptions();
  checkButtonState();
});

// 添加一个状态来控制是否已设置基本信息
const hasSetBasicInfo = ref(false);

// 修改显示对话框的处理函数
const showImportDialog = async () => {
  await getOptions();
  dialogVisible.value = true;
};

// 新增确认基本信息的处理函数
const handleConfirmBasicInfo = async () => {
  try {
    // 验证表单是否填写完整
    if (
      !filterForm.value.department ||
      !filterForm.value.major ||
      !filterForm.value.grade
    ) {
      ElMessage.warning("请填写完整的筛选条件");
      return;
    }

    const res = await getFilteredCoursesReq({
      department: filterForm.value.department,
      major: filterForm.value.major,
      grade: filterForm.value.grade,
    });

    if (res.data.code === 200) {
      columns.value = [
        { prop: "id", label: "ID", width: "55", align: "center" },
        { prop: "sno", label: "学号" },
        { prop: "name", label: "姓名" },
        { prop: "class_name", label: "班级" },
        ...res.data.data.map((course) => ({
          prop: course.course_id,
          label: course.course_name,
        })),
      ];

      hasSetBasicInfo.value = true;
      dialogVisible.value = false;
      ElMessage.success("基本信息设置成功");
    } else {
      ElMessage.error(res.data.message || "获取课程列表失败");
    }
  } catch (error) {
    console.error("获取课程列表失败:", error);
    ElMessage.error("获取课程列表失败");
  }
};

// 修改保存逻辑，加入筛选条件
const handleSave = async () => {
  try {
    const data = {
      department: filterForm.value.department,
      major: filterForm.value.major,
      grade: filterForm.value.grade,
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
    await saveScoreReq(data);
    ElMessage.success("保存成功");
    tableData.value = [];
    filterForm.value = {
      department: "",
      major: "",
      grade: "",
    };
  } catch (error) {
    console.error("保存失败:", error);
    ElMessage.error(error.response?.data?.msg || "保存失败");
  }
};

// 添加生成模板的函数
const generateTemplate = () => {
  try {
    if (!hasSetBasicInfo.value) {
      ElMessage.warning("请先填写成绩基本信息");
      return;
    }

    const headers = [
      "学号",
      "姓名",
      "班级",
      ...columns.value
        .filter(
          (col) => !["id", "sno", "name", "class_name"].includes(col.prop)
        )
        .map((col) => col.label),
    ];

    const exampleRow = headers.reduce((acc, header) => {
      acc[header] = "";
      return acc;
    }, {});

    const ws = XLSX.utils.json_to_sheet([exampleRow], {
      header: headers,
    });

    // 设置列宽
    const colWidth = headers.map(() => ({ wch: 15 }));
    ws["!cols"] = colWidth;

    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "成绩模板");

    // 下载文件
    XLSX.writeFile(
      wb,
      `成绩导入模板_${filterForm.value.department}_${filterForm.value.major}_${filterForm.value.grade}.xlsx`
    );
  } catch (error) {
    console.error("生成模板失败:", error);
    ElMessage.error("生成模板失败");
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

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
