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
        <el-button
          type="info"
          @click="showInputtedInfo"
          style="margin-left: 10px"
        >
          查看当前已录入信息
        </el-button>
        <el-button type="primary" @click="handleAdd" style="margin-left: 10px">
          添加成绩
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
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="scope">
            <el-button type="primary" link @click="handleEdit(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" link @click="handleDelete(scope.row)">
              删除
            </el-button>
          </template>
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
              v-for="dept in departments"
              :key="dept.value"
              :label="dept.label"
              :value="dept.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="专业">
          <el-select
            v-model="filterForm.major"
            placeholder="请选择专业"
            style="width: 100%"
            :disabled="!filterForm.department"
          >
            <el-option
              v-for="major in availableMajors"
              :key="major"
              :label="major"
              :value="major"
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
              v-for="grade in options.grades"
              :key="grade"
              :label="grade"
              :value="grade"
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

    <el-dialog title="已录入成绩信息" v-model="inputtedInfoVisible" width="50%">
      <el-table :data="inputtedColleges" border>
        <el-table-column prop="department" label="学院" />
        <el-table-column prop="major" label="专业" />
        <el-table-column prop="grade" label="年级" />
        <el-table-column label="操作" width="120" align="center">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="handleViewScores(scope.row)"
            >
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <el-dialog
      :title="isEdit ? '编辑成绩' : '添加成绩'"
      v-model="dialogFormVisible"
      width="50%"
      :close-on-click-modal="false"
    >
      <el-form :model="formData" label-width="120px">
        <el-form-item label="学号">
          <el-input v-model="formData.sno" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="formData.name" />
        </el-form-item>
        <el-form-item label="学院">
          <el-select
            v-model="formData.department"
            placeholder="请选择学院"
            style="width: 100%"
          >
            <el-option
              v-for="dept in departments"
              :key="dept.value"
              :label="dept.label"
              :value="dept.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="专业">
          <el-select
            v-model="formData.major"
            placeholder="请选择专业"
            style="width: 100%"
            :disabled="!formData.department"
          >
            <el-option
              v-for="major in formMajors"
              :key="major"
              :label="major"
              :value="major"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="年级">
          <el-select
            v-model="formData.grade"
            placeholder="请选择年级"
            style="width: 100%"
          >
            <el-option
              v-for="grade in options.grades"
              :key="grade"
              :label="grade"
              :value="grade"
            />
          </el-select>
        </el-form-item>
        <!-- 动态课程成绩表单项 -->
        <el-form-item
          v-for="col in dynamicColumns"
          :key="col.prop"
          :label="col.label"
        >
          <el-input v-model="formData[col.prop]" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmForm">确定</el-button>
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
import { ref, reactive, onMounted, computed, onBeforeMount, watch } from "vue";
import * as XLSX from "xlsx";
import { saveScoreReq, addScoreReq, updateScoreReq } from "@/api/score";
import { ElMessage, ElMessageBox } from "element-plus";
import { getSessionOptionsReq, getFilteredCoursesReq } from "@/api/session";
import { getCollegeList } from "@/api/college";
import { getInputtedCollege, getCollegeScores } from "@/api/score";
import {
  SessionOptionsResponse,
  FilteredCoursesResponse,
} from "@/types/session";

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
  grades: ["21级", "22级", "23级", "24级"],
});

// 动态列配置
const columns = ref([
  { prop: "id", label: "ID", width: "55", align: "center" },
  { prop: "sno", label: "学号" },
  { prop: "name", label: "姓名" },
  { prop: "department", label: "学院" },
  { prop: "major", label: "专业" },
  { prop: "grade", label: "年级" },
]);

// 存储从API获取的学院数据
const collegeData = ref<any[]>([]);

// 获取学院数据
const fetchCollegeData = async () => {
  try {
    const res = await getCollegeList();
    if (res.data) {
      collegeData.value = res.data;
    }
  } catch (error) {
    console.error("获取学院数据失败:", error);
    ElMessage.error("获取学院数据失败");
  }
};

// 处理学院数据为下拉选项格式
const departments = computed(() => {
  const deptMap = new Map();
  collegeData.value.forEach((item) => {
    if (!deptMap.has(item.department)) {
      deptMap.set(item.department, {
        label: item.department,
        value: item.department,
        majors: new Set(),
      });
    }
    deptMap.get(item.department).majors.add(item.major);
  });
  return Array.from(deptMap.values()).map((dept) => ({
    label: dept.label,
    value: dept.value,
    majors: Array.from(dept.majors),
  }));
});

// 根据选择的学院计算可选的专业
const availableMajors = computed(() => {
  const selectedDept = departments.value.find(
    (dept) => dept.value === filterForm.value.department
  );
  return selectedDept ? selectedDept.majors : [];
});

// 监听学院变化，重置专业选择
watch(
  () => filterForm.value.department,
  () => {
    filterForm.value.major = "";
    filterForm.value.grade = "";
  }
);

// 监听专业变化，重置年级选择
watch(
  () => filterForm.value.major,
  () => {
    filterForm.value.grade = "";
  }
);

// 组件挂载前获取学院数据
onBeforeMount(async () => {
  await fetchCollegeData();
});

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
      department: item["学院"],
      major: item["专业"],
      grade: item["年级"],
    };

    // 动态添加课程成绩
    columns.value.forEach((col) => {
      if (
        !["id", "sno", "name", "department", "major", "grade"].includes(
          col.prop
        )
      ) {
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
  checkButtonState();
});

// 添加一个状态来控制是否已设置基本信息
const hasSetBasicInfo = ref(false);

// 修改显示对话框的处理函数
const showImportDialog = async () => {
  await fetchCollegeData();
  dialogVisible.value = true;
};

// 修改确认基本信息的处理函数
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
      // 清空表格数据
      tableData.value = [];

      // 更新列配置
      columns.value = [
        { prop: "id", label: "ID", width: "55", align: "center" },
        { prop: "sno", label: "学号" },
        { prop: "name", label: "姓名" },
        { prop: "department", label: "学院" },
        { prop: "major", label: "专业" },
        { prop: "grade", label: "年级" },
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

// 修改保存逻辑，加入筛选条件和动态课程成绩
const handleSave = async () => {
  try {
    // 获取课程字段列表
    const courseFields = columns.value
      .filter(
        (col) =>
          !["id", "sno", "name", "department", "major", "grade"].includes(
            col.prop
          )
      )
      .map((col) => col.label);

    const data = {
      scores: tableData.value.map((item) => {
        // 创建基础学生信息
        const scoreData = {
          name: item.name,
          sno: item.sno,
          department: item.department,
          major: item.major,
          grade: item.grade,
        };

        // 动态添加课程成绩
        columns.value
          .filter(
            (col) =>
              !["id", "sno", "name", "department", "major", "grade"].includes(
                col.prop
              )
          )
          .forEach((col) => {
            scoreData[col.label] = item[col.prop] || "";
          });

        return scoreData;
      }),
      course_fields: courseFields, // 添加课程字段列表
    };

    console.log("发送到后端的数据:", JSON.stringify(data, null, 2));

    await saveScoreReq(data);
    ElMessage.success("保存成功");
    tableData.value = [];
    filterForm.value = {
      department: "",
      major: "",
      grade: "",
    };
    hasSetBasicInfo.value = false;
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
      "学院",
      "专业",
      "年级",
      ...columns.value
        .filter(
          (col) =>
            !["id", "sno", "name", "department", "major", "grade"].includes(
              col.prop
            )
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

// 添加已录入信息相关的状态和方法
const inputtedInfoVisible = ref(false);
const inputtedColleges = ref([]);

const showInputtedInfo = async () => {
  try {
    const res = await getInputtedCollege();
    if (res.data.code === 200) {
      inputtedColleges.value = res.data.data;
      inputtedInfoVisible.value = true;
    } else {
      ElMessage.error(res.data.message || "获取已录入信息失败");
    }
  } catch (error) {
    console.error("获取已录入信息失败:", error);
    ElMessage.error("获取已录入信息失败");
  }
};

// 添加查看成绩处理函数
const handleViewScores = async (row) => {
  try {
    // 关闭弹窗
    inputtedInfoVisible.value = false;

    // 请求成绩数据
    const res = await getCollegeScores({
      department: row.department,
      major: row.major,
      grade: row.grade,
    });

    if (res.data.code === 200) {
      // 更新表格数据
      tableData.value = res.data.data;

      // 根据返回的数据动态更新列配置
      if (res.data.data.length > 0) {
        const firstRow = res.data.data[0];
        columns.value = [
          { prop: "sno", label: "学号", width: "120" },
          { prop: "name", label: "姓名", width: "100" },
          { prop: "department", label: "学院" },
          { prop: "major", label: "专业" },
          { prop: "grade", label: "年级" },
          ...Object.keys(firstRow)
            .filter(
              (key) =>
                !["sno", "name", "department", "major", "grade"].includes(key)
            )
            .map((key) => ({
              prop: key,
              label: key,
              width: "120",
            })),
        ];
      }

      ElMessage.success("获取成绩数据成功");
    } else {
      ElMessage.warning(res.data.message || "获取成绩数据失败");
    }
  } catch (error) {
    console.error("获取成绩数据失败:", error);
    ElMessage.error("获取成绩数据失败");
  }
};

// 在 script setup 中更新以下内容
interface FormData {
  id?: number;
  sno: string;
  name: string;
  department: string;
  major: string;
  grade: string;
  [key: string]: any; // 用于动态课程字段
}

const dialogFormVisible = ref(false);
const isEdit = ref(false);
const formData = ref<FormData>({
  sno: "",
  name: "",
  department: "",
  major: "",
  grade: "",
});
const currentEditingId = ref<number | null>(null);

// 修改添加成绩方法
const handleAdd = () => {
  isEdit.value = false;
  formData.value = {
    sno: "",
    name: "",
    department: "",
    major: "",
    grade: "",
  };
  // 添加动态课程字段
  columns.value.forEach((col) => {
    if (
      !["id", "sno", "name", "department", "major", "grade"].includes(col.prop)
    ) {
      formData.value[col.prop] = "";
    }
  });
  dialogFormVisible.value = true;
};

// 修改编辑方法
const handleEdit = (row: any) => {
  isEdit.value = true;
  currentEditingId.value = row.id;
  formData.value = { ...row };
  dialogFormVisible.value = true;
};

// 确认表单方法
const confirmForm = async () => {
  try {
    // 构造成绩数据
    const scoreData = {
      sno: formData.value.sno,
      name: formData.value.name,
      department: formData.value.department,
      major: formData.value.major,
      grade: formData.value.grade,
      scores: {},
    };

    // 添加动态课程成绩
    dynamicColumns.value.forEach((col) => {
      scoreData.scores[col.prop] = formData.value[col.prop] || "";
    });

    if (isEdit.value) {
      // 编辑现有记录
      const response = await updateScoreReq(scoreData);
      if (response.data.code === 200) {
        const index = tableData.value.findIndex(
          (item) => item.id === currentEditingId.value
        );
        if (index > -1) {
          tableData.value[index] = { ...formData.value };
          ElMessage.success("修改成功");
        }
      } else {
        ElMessage.error(response.data.msg || "修改失败");
        return;
      }
    } else {
      // 添加新记录
      const response = await addScoreReq(scoreData);
      if (response.data.code === 200) {
        const newRow = {
          id: tableData.value.length + 1,
          ...formData.value,
        };
        tableData.value.push(newRow);
        ElMessage.success("添加成功");
      } else {
        ElMessage.error(response.data.msg || "添加失败");
        return;
      }
    }
    dialogFormVisible.value = false;
  } catch (error) {
    console.error("操作失败:", error);
    ElMessage.error("操作失败，请重试");
  }
};

// 获取动态课程列
const dynamicColumns = computed(() => {
  return columns.value.filter(
    (col) =>
      !["id", "sno", "name", "department", "major", "grade"].includes(col.prop)
  );
});

const handleDelete = (row) => {
  ElMessageBox.confirm("确认要删除这条成绩记录吗？", "提示", {
    type: "warning",
  })
    .then(() => {
      const index = tableData.value.findIndex((item) => item.id === row.id);
      if (index > -1) {
        tableData.value.splice(index, 1);
        ElMessage.success("删除成功");
      }
    })
    .catch(() => {
      // 取消删除操作
    });
};

// 为表单添加专业选项计算属性
const formMajors = computed(() => {
  const selectedDept = departments.value.find(
    (dept) => dept.value === formData.value.department
  );
  return selectedDept ? selectedDept.majors : [];
});

// 监听表单中学院变化
watch(
  () => formData.value.department,
  () => {
    formData.value.major = ""; // 重置专业选择
    formData.value.grade = ""; // 重置年级选择
  }
);

// 监听表单中专业变化
watch(
  () => formData.value.major,
  () => {
    formData.value.grade = ""; // 重置年级选择
  }
);

// 确保组件挂载时获取学院数据
onMounted(async () => {
  await fetchCollegeData();
});
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
