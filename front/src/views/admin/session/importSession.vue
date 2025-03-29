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
        <el-button type="primary" @click="handleAdd" style="margin-left: 10px">
          添加课程
        </el-button>
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
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button type="primary" link @click="handleEdit(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" link @click="handleDelete(scope.$index)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 编辑/添加对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加课程' : '编辑课程'"
      width="50%"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="课程ID" prop="course_id">
          <el-input v-model="form.course_id" placeholder="请输入课程ID" />
        </el-form-item>
        <el-form-item label="课程名" prop="course_name">
          <el-input v-model="form.course_name" placeholder="请输入课程名" />
        </el-form-item>
        <el-form-item label="学分" prop="credit">
          <el-input v-model="form.credit" placeholder="请输入学分" />
        </el-form-item>
        <el-form-item label="学时" prop="hours">
          <el-input v-model="form.hours" placeholder="请输入学时" />
        </el-form-item>
        <el-form-item label="课程性质" prop="nature">
          <el-input v-model="form.nature" placeholder="请输入课程性质" />
        </el-form-item>
        <el-form-item label="所属学院" prop="college">
          <el-input v-model="form.college" placeholder="请输入所属学院" />
        </el-form-item>
        <el-form-item label="所属专业" prop="major">
          <el-input v-model="form.major" placeholder="请输入所属专业" />
        </el-form-item>
        <el-form-item label="适用年级" prop="grade">
          <el-input v-model="form.grade" placeholder="请输入适用年级" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="session">
import { UploadProps } from "element-plus";
import { ref, onMounted, onBeforeMount } from "vue";
import * as XLSX from "xlsx";
import { getSessionAll, saveSessionReq } from "@/api/session";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";

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
const dialogVisible = ref(false);
const dialogType = ref<"add" | "edit">("add");
const currentIndex = ref(-1);
const formRef = ref<FormInstance>();

const form = ref({
  course_id: "",
  course_name: "",
  credit: "",
  hours: "",
  nature: "",
  college: "",
  major: "",
  grade: "",
});

const rules: FormRules = {
  course_id: [{ required: true, message: "请输入课程ID", trigger: "blur" }],
  course_name: [{ required: true, message: "请输入课程名", trigger: "blur" }],
  credit: [{ required: true, message: "请输入学分", trigger: "blur" }],
  hours: [{ required: true, message: "请输入学时", trigger: "blur" }],
  nature: [{ required: true, message: "请输入课程性质", trigger: "blur" }],
  college: [{ required: true, message: "请输入所属学院", trigger: "blur" }],
  major: [{ required: true, message: "请输入所属专业", trigger: "blur" }],
  grade: [{ required: true, message: "请输入适用年级", trigger: "blur" }],
};

// 获取表格数据
const getData = async () => {
  const res = await getSessionAll();

  tableData.value = res.data.data;
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
      id: tableData.value.length + index + 1,
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
};

// 添加课程
const handleAdd = () => {
  dialogType.value = "add";
  form.value = {
    course_id: "",
    course_name: "",
    credit: "",
    hours: "",
    nature: "",
    college: "",
    major: "",
    grade: "",
  };
  dialogVisible.value = true;
};

// 编辑课程
const handleEdit = (row: TableItem) => {
  dialogType.value = "edit";
  currentIndex.value = tableData.value.findIndex((item) => item.id === row.id);
  form.value = { ...row };
  dialogVisible.value = true;
};

// 删除课程
const handleDelete = (index: number) => {
  tableData.value.splice(index, 1);
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;

  await formRef.value.validate((valid) => {
    if (valid) {
      const newItem = {
        id:
          dialogType.value === "add"
            ? tableData.value.length + 1
            : tableData.value[currentIndex.value].id,
        ...form.value,
      };

      if (dialogType.value === "add") {
        tableData.value.push(newItem);
      } else {
        tableData.value[currentIndex.value] = newItem;
      }

      dialogVisible.value = false;
      ElMessage.success(dialogType.value === "add" ? "添加成功" : "编辑成功");
    }
  });
};

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
    await saveSessionReq(data);
    ElMessage.success("保存成功");
    tableData.value = []; // 清空表格数据
  } catch (error) {
    console.error("保存失败:", error);
    ElMessage.error(error.response?.data?.msg || "保存失败");
  }
};
onBeforeMount(async () => {
  getData();
});
</script>

<style scoped>
.handle-box {
  display: flex;
  margin-bottom: 20px;
  align-items: center;
}

.table {
  width: 100%;
  font-size: 14px;
}

.mr10 {
  margin-right: 10px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
