<!-- <template>
  <div>
    <div class="container">
      <div class="handle-box">
        <el-button type="primary" @click="exportXlsx">导出Excel</el-button>
        <el-button
          type="success"
          @click="handleSave"
          :disabled="!tableData.length"
          >保存综合测评</el-button
        >
      </div>
      <el-table
        :data="tableData"
        border
        class="table"
        header-cell-class-name="table-header"
      >
        <el-table-column prop="sno" label="学号" width="100"></el-table-column>
        <el-table-column prop="name" label="姓名" width="80"></el-table-column>
        <el-table-column
          prop="class_name"
          label="班级"
          width="100"
        ></el-table-column>
        <el-table-column
          prop="操作系统课程设计成绩"
          label="操作系统课程设计成绩"
          width="150"
        ></el-table-column>
        <el-table-column
          prop="无线网络技术成绩"
          label="无线网络技术成绩"
          width="150"
        ></el-table-column>
        <el-table-column
          prop="计算机网络课程设计"
          label="计算机网络课程设计"
          width="150"
        ></el-table-column>
        <el-table-column
          prop="操作系统"
          label="操作系统"
          width="100"
        ></el-table-column>
        <el-table-column
          prop="人工智能与网络技术学科前沿"
          label="人工智能与网络技术学科前沿"
          width="220"
        ></el-table-column>
        <el-table-column
          prop="信息安全原理及应用"
          label="信息安全原理及应用"
          width="150"
        ></el-table-column>
        <el-table-column
          prop="Linux操作系统"
          label="Linux操作系统"
          width="130"
        ></el-table-column>
        <el-table-column
          prop="Java程序设计"
          label="Java程序设计"
          width="130"
        ></el-table-column>
        <el-table-column
          prop="creditGpa"
          label="学分绩点"
          width="100"
        ></el-table-column>
        <el-table-column
          prop="yearGpa"
          label="学年绩点"
          width="100"
        ></el-table-column>
        <el-table-column
          prop="comprehensiveScore"
          label="学业分成绩"
          width="100"
        ></el-table-column>
      </el-table>
    </div>
  </div>
</template> -->

<template>
  <div>
    <div class="container">
      <div class="handle-box">
        <el-button class="mr10" type="primary" @click="showFilterDialog">
          填写成绩基本信息
        </el-button>
        <el-button
          type="primary"
          @click="exportXlsx"
          :disabled="!hasSetBasicInfo"
          >导出Excel</el-button
        >
        <el-button
          type="success"
          @click="handleSave"
          :disabled="!tableData.length"
          >保存综合测评</el-button
        >
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
        >
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加筛选对话框 -->
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
  </div>
</template>

<!-- <script setup lang="ts" name="export">
import { ref, onMounted } from "vue";
import * as XLSX from "xlsx";
import { ElMessage } from "element-plus";
import {
  getSessionAll,
  getSessionOptionsReq,
  getFilteredCoursesReq,
} from "@/api/session";
import { getScoreAll } from "@/api/score";
import { saveComprehensiveTestReq } from "@/api/comprehensive-test";

// ... existing code ...

// 添加新的状态变量
const dialogVisible = ref(false);
const hasSetBasicInfo = ref(false);
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
  { prop: "sno", label: "学号", width: "100" },
  { prop: "name", label: "姓名", width: "80" },
  { prop: "class_name", label: "班级", width: "100" },
]);

// 显示筛选对话框
const showFilterDialog = async () => {
  try {
    const res = await getSessionOptionsReq();
    console.log("获取学院的那些选择", res.data);

    if (res.code === 200) {
      options.value = res.data;
      dialogVisible.value = true;
    } else {
      ElMessage.error(res.message || "获取选项失败");
    }
  } catch (error) {
    console.error("获取选项失败:", error);
    ElMessage.error("获取选项失败");
  }
};

// 确认基本信息
const handleConfirmBasicInfo = async () => {
  try {
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
      // 设置基础列
      columns.value = [
        { prop: "sno", label: "学号", width: "100" },
        { prop: "name", label: "姓名", width: "80" },
        { prop: "class_name", label: "班级", width: "100" },
        // 添加课程列
        ...res.data.data.map((course) => ({
          prop: course.course_name,
          label: course.course_name,
          width: "150",
        })),
        // 添加计算列
        { prop: "creditGpa", label: "学分绩点", width: "100" },
        { prop: "yearGpa", label: "学年绩点", width: "100" },
        { prop: "comprehensiveScore", label: "学业分成绩", width: "100" },
      ];

      hasSetBasicInfo.value = true;
      dialogVisible.value = false;
      // 获取成绩数据
      await getScoreData();
      ElMessage.success("基本信息设置成功");
    } else {
      ElMessage.error(res.data.message || "获取课程列表失败");
    }
  } catch (error) {
    console.error("获取课程列表失败:", error);
    ElMessage.error("获取课程列表失败");
  }
};

// 修改获取成绩数据的方法
const getScoreData = async () => {
  try {
    const response = await getScoreAll({
      department: filterForm.value.department,
      major: filterForm.value.major,
      grade: filterForm.value.grade,
    });

    if (!response.data.data) {
      ElMessage.warning("未找到成绩数据");
      tableData.value = [];
      return;
    }

    const scores = response.data.data;

    // 确保课程数据已加载
    if (courseData.value.length === 0) {
      await getCourseData();
    }

    // 创建课程名称到学分的映射
    const courseCredits = {};
    const courseNature = {};

    courseData.value.forEach((course) => {
      courseCredits[course.course_name] = parseFloat(course.credit) || 0;
      courseNature[course.course_name] = course.nature;
    });

    // 获取当前显示的课程列
    const courseCols = columns.value.filter(
      (col) =>
        ![
          "sno",
          "name",
          "class_name",
          "creditGpa",
          "yearGpa",
          "comprehensiveScore",
        ].includes(col.prop)
    );

    // 过滤掉所有课程成绩都为空的学生
    const filteredScores = scores.filter((score) => {
      // 检查是否至少有一门课程有成绩
      return courseCols.some((col) => {
        const courseScore = score[col.prop];
        return courseScore && courseScore.trim() !== "";
      });
    });

    // 处理每个学生的成绩
    tableData.value = filteredScores.map((score) => {
      // 计算每门课的绩点
      const courseGradePoints = {};

      // 动态获取所有课程成绩并计算绩点
      courseCols.forEach((col) => {
        courseGradePoints[col.prop] = calculateGradePoint(score[col.prop]);
      });

      // 计算学分绩点之和
      let totalCreditGpa = 0;
      let totalCredits = 0;
      let totalCreditGpaNonElective = 0;
      let totalCreditsNonElective = 0;

      Object.keys(courseGradePoints).forEach((courseName) => {
        const credit = courseCredits[courseName] || 0;
        const gradePoint = courseGradePoints[courseName];
        const creditGpa = credit * gradePoint;

        totalCreditGpa += creditGpa;
        totalCredits += credit;

        // 如果不是公选课，计入非公选课总和
        const nature = courseNature[courseName] || "";
        if (nature !== "公选课") {
          totalCreditGpaNonElective += creditGpa;
          totalCreditsNonElective += credit;
        }
      });

      // 计算学年绩点
      const yearGpa = totalCredits > 0 ? totalCreditGpa / totalCredits : 0;

      // 计算学业分成绩
      const nonElectiveGpa =
        totalCreditsNonElective > 0
          ? totalCreditGpaNonElective / totalCreditsNonElective
          : 0;
      const comprehensiveScore = (nonElectiveGpa + 5) * 9;

      return {
        ...score,
        creditGpa: parseFloat(totalCreditGpa.toFixed(2)),
        yearGpa: parseFloat(yearGpa.toFixed(2)),
        comprehensiveScore: parseFloat(comprehensiveScore.toFixed(2)),
      };
    });

    console.log("处理后的成绩数据:", tableData.value);
  } catch (error) {
    console.error("获取成绩数据失败:", error);
    ElMessage.error("获取成绩数据失败");
  }
};

// 修改保存方法，添加筛选条件
const handleSave = async () => {
  try {
    const data = {
      department: filterForm.value.department,
      major: filterForm.value.major,
      grade: filterForm.value.grade,
      tests: tableData.value.map((item) => ({
        sno: item.sno,
        name: item.name,
        class_name: item.class_name,
        ...Object.fromEntries(
          columns.value
            .filter(
              (col) =>
                ![
                  "sno",
                  "name",
                  "class_name",
                  "creditGpa",
                  "yearGpa",
                  "comprehensiveScore",
                  "academic",
                  "labor",
                  "sports",
                  "innovation",
                  "zongce"
                ].includes(col.prop)
            )
            .map((col) => [col.prop, item[col.prop]])
        ),
        credit_gpa: item.creditGpa,
        year_gpa: item.yearGpa,
        
        academic: item.academic,
        labor: item.labor,
        sports: item.sports,
        innovation: item.innovation,
        zongce: item.zongce,
        comprehensive: item.comprehensiveScore
      })),
    };

    const res = await saveComprehensiveTestReq(data);
    if (res.data.code === 200) {
      ElMessage.success(`成功保存 ${res.data.data.success} 条综合测评数据`);
    } else {
      ElMessage.error(res.data.message || "保存失败");
    }
  } catch (error) {
    console.error("保存失败:", error);
    ElMessage.error(error.response?.data?.msg || "保存失败");
  }
};

// 修改导出Excel方法
const exportXlsx = () => {
  if (!hasSetBasicInfo.value) {
    ElMessage.warning("请先填写成绩基本信息");
    return;
  }

  const headers = columns.value.map((col) => col.label);
  const list = [headers];

  tableData.value.forEach((item) => {
    const row = columns.value.map((col) => String(item[col.prop] || ""));
    list.push(row);
  });

  const WorkSheet = XLSX.utils.aoa_to_sheet(list);
  const new_workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(new_workbook, WorkSheet, "成绩表");
  XLSX.writeFile(
    new_workbook,
    `学生成绩表_${filterForm.value.department}_${filterForm.value.major}_${filterForm.value.grade}.xlsx`
  );
};

// 移除原有的onMounted初始化
onMounted(() => {
  // 不再自动加载数据，等待用户选择筛选条件
});
</script>

<style scoped>
.handle-box {
  margin-bottom: 20px;
}

.mr10 {
  margin-right: 10px;
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
</style> -->

<script setup lang="ts">
import { ref, onMounted } from "vue";
import * as XLSX from "xlsx";
import { ElMessage } from "element-plus";
import {
  getSessionAll,
  getSessionOptionsReq,
  getFilteredCoursesReq,
} from "@/api/session";
import { getActivityScoresReq } from "@/api/activity";
import { getScoreAll } from "@/api/score";
import { saveComprehensiveTestReq } from "@/api/comprehensive-test";

interface CourseInfo {
  course_id: string;
  course_name: string;
  credit: string;
  hours: string;
  nature: string;
  department: string;
}

interface StudentScore {
  id: number;
  sno: string;
  name: string;
  class_name: string;
  操作系统课程设计成绩: string;
  无线网络技术成绩: string;
  计算机网络课程设计: string;
  操作系统: string;
  人工智能与网络技术学科前沿: string;
  信息安全原理及应用: string;
  Linux操作系统: string;
  Java程序设计: string;
  creditGpa: number;
  yearGpa: number;
  comprehensiveScore: number;
  academic: number;
  labor: number;
  sports: number;
  innovation: number;
  zongce: number;
}

const tableData = ref([]);
const courseData = ref([]);

const dialogVisible = ref(false);
const hasSetBasicInfo = ref(false);
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
  { prop: "sno", label: "学号", width: "100" },
  { prop: "name", label: "姓名", width: "80" },
  { prop: "class_name", label: "班级", width: "100" },
]);

// 计算绩点
const calculateGradePoint = (score: string): number => {
  if (!score || score === "") return 0;

  const numScore = parseFloat(score);
  if (isNaN(numScore)) return 0;

  if (numScore < 60) return 0;
  if (numScore === 60) return 2.0;
  if (numScore > 60 && numScore < 70) return 2.0 + (numScore - 60) * 0.1;
  if (numScore >= 70 && numScore < 80) return 3.0 + (numScore - 70) * 0.1;
  if (numScore >= 80 && numScore < 90) return 4.0 + (numScore - 80) * 0.1;
  if (numScore >= 90) return 5.0 + (numScore - 90) * 0.1;

  return 0;
};

// 获取课程数据
const getCourseData = async () => {
  try {
    const response = await getSessionAll();
    courseData.value = response.data.data || [];
    console.log("课程数据:", courseData.value);
  } catch (error) {
    console.error("获取课程数据失败:", error);
    ElMessage.error("获取课程数据失败");
  }
};

//获取活动分数
const getActivityScores = async (
  sno: string,
  category: string
): Promise<number> => {
  try {
    const response = await getActivityScoresReq({
      student_sno: sno,
      activity_category: category,
    });

    if (response.data.code === 200) {
      // 计算该类型的总加分
      return response.data.data.reduce((sum, activity) => {
        return sum + (parseFloat(activity.credits) || 0);
      }, 0);
    }
    return 0;
  } catch (error) {
    console.error(`获取${category}活动加分失败:`, error);
    return 0;
  }
};
// 显示筛选对话框
const showFilterDialog = async () => {
  try {
    const res = await getSessionOptionsReq();
    if (res.code === 200) {
      options.value = res.data;
      dialogVisible.value = true;
    } else {
      ElMessage.error(res.message || "获取选项失败");
    }
  } catch (error) {
    console.error("获取选项失败:", error);
    ElMessage.error("获取选项失败");
  }
};

// 确认基本信息
const handleConfirmBasicInfo = async () => {
  try {
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
      // 设置基础列
      columns.value = [
        { prop: "sno", label: "学号", width: "100" },
        { prop: "name", label: "姓名", width: "80" },
        { prop: "class_name", label: "班级", width: "100" },
        // 添加课程列
        ...res.data.data.map((course) => ({
          prop: course.course_name,
          label: course.course_name,
          width: "150",
        })),
        // 添加计算列
        { prop: "creditGpa", label: "学分绩点", width: "100" },
        { prop: "yearGpa", label: "学年绩点", width: "100" },
        { prop: "comprehensiveScore", label: "学业分成绩", width: "100" },
        { prop: "academic", label: "学业分加分", width: "100" },
        { prop: "labor", label: "劳动分加分", width: "100" },
        { prop: "sports", label: "文体分加分", width: "100" },
        { prop: "innovation", label: "思想分加分", width: "100" },
        { prop: "zongce", label: "综测分数", width: "100" },
      ];

      hasSetBasicInfo.value = true;
      dialogVisible.value = false;
      // 获取成绩数据
      await getScoreData();
      ElMessage.success("基本信息设置成功");
    } else {
      ElMessage.error(res.data.message || "获取课程列表失败");
    }
  } catch (error) {
    console.error("获取课程列表失败:", error);
    ElMessage.error("获取课程列表失败");
  }
};

// 修改获取成绩数据的方法
// const getScoreData = async () => {
//   try {
//     const response = await getScoreAll({
//       department: filterForm.value.department,
//       major: filterForm.value.major,
//       grade: filterForm.value.grade,
//     });

//     if (!response.data.data) {
//       ElMessage.warning("未找到成绩数据");
//       tableData.value = [];
//       return;
//     }

//     const scores = response.data.data;

//     // 确保课程数据已加载
//     if (courseData.value.length === 0) {
//       await getCourseData();
//     }

//     // 创建课程名称到学分的映射
//     const courseCredits = {};
//     const courseNature = {};

//     courseData.value.forEach((course) => {
//       courseCredits[course.course_name] = parseFloat(course.credit) || 0;
//       courseNature[course.course_name] = course.nature;
//     });

//     // 获取当前显示的课程列
//     const courseCols = columns.value.filter(
//       (col) =>
//         ![
//           "sno",
//           "name",
//           "class_name",
//           "creditGpa",
//           "yearGpa",
//           "comprehensiveScore",
//         ].includes(col.prop)
//     );

//     // 过滤掉所有课程成绩都为空的学生
//     const filteredScores = scores.filter((score) => {
//       // 检查是否至少有一门课程有成绩
//       return courseCols.some((col) => {
//         const courseScore = score[col.prop];
//         return courseScore && courseScore.trim() !== "";
//       });
//     });

//     // 处理每个学生的成绩
//     tableData.value = filteredScores.map((score) => {
//       // 计算每门课的绩点
//       const courseGradePoints = {};

//       // 动态获取所有课程成绩并计算绩点
//       courseCols.forEach((col) => {
//         courseGradePoints[col.prop] = calculateGradePoint(score[col.prop]);
//       });

//       // 计算学分绩点之和
//       let totalCreditGpa = 0;
//       let totalCredits = 0;
//       let totalCreditGpaNonElective = 0;
//       let totalCreditsNonElective = 0;

//       Object.keys(courseGradePoints).forEach((courseName) => {
//         const credit = courseCredits[courseName] || 0;
//         const gradePoint = courseGradePoints[courseName];
//         const creditGpa = credit * gradePoint;

//         totalCreditGpa += creditGpa;
//         totalCredits += credit;

//         // 如果不是公选课，计入非公选课总和
//         const nature = courseNature[courseName] || "";
//         if (nature !== "公选课") {
//           totalCreditGpaNonElective += creditGpa;
//           totalCreditsNonElective += credit;
//         }
//       });

//       // 计算学年绩点
//       const yearGpa = totalCredits > 0 ? totalCreditGpa / totalCredits : 0;

//       // 计算学业分成绩
//       const nonElectiveGpa =
//         totalCreditsNonElective > 0
//           ? totalCreditGpaNonElective / totalCreditsNonElective
//           : 0;
//       const comprehensiveScore = (nonElectiveGpa + 5) * 9;

//       return {
//         ...score,
//         creditGpa: parseFloat(totalCreditGpa.toFixed(2)),
//         yearGpa: parseFloat(yearGpa.toFixed(2)),
//         comprehensiveScore: parseFloat(comprehensiveScore.toFixed(2)),
//       };
//     });

//     console.log("处理后的成绩数据:", tableData.value);
//   } catch (error) {
//     console.error("获取成绩数据失败:", error);
//     ElMessage.error("获取成绩数据失败");
//   }
// };

// 修改获取成绩数据的方法
const getScoreData = async () => {
  try {
    const response = await getScoreAll({
      department: filterForm.value.department,
      major: filterForm.value.major,
      grade: filterForm.value.grade,
    });

    if (!response.data.data) {
      ElMessage.warning("未找到成绩数据");
      tableData.value = [];
      return;
    }

    const scores = response.data.data;

    // 确保课程数据已加载
    if (courseData.value.length === 0) {
      await getCourseData();
    }

    // 创建课程名称到学分的映射
    const courseCredits = {};
    const courseNature = {};

    courseData.value.forEach((course) => {
      courseCredits[course.course_name] = parseFloat(course.credit) || 0;
      courseNature[course.course_name] = course.nature;
    });

    // 获取当前显示的课程列
    const courseCols = columns.value.filter(
      (col) =>
        ![
          "sno",
          "name",
          "class_name",
          "creditGpa",
          "yearGpa",
          "comprehensiveScore",
          "academic",
          "labor",
          "sports",
          "innovation",
          "zongce",
        ].includes(col.prop)
    );

    // 过滤掉所有课程成绩都为空的学生
    const filteredScores = scores.filter((score) => {
      // 检查是否至少有一门课程有成绩
      return courseCols.some((col) => {
        const courseScore = score[col.prop];
        return courseScore && courseScore.trim() !== "";
      });
    });

    // 处理每个学生的成绩
    const processedScores = [];
    for (const score of filteredScores) {
      // 计算每门课的绩点
      const courseGradePoints = {};

      // 动态获取所有课程成绩并计算绩点
      courseCols.forEach((col) => {
        courseGradePoints[col.prop] = calculateGradePoint(score[col.prop]);
      });

      // 计算学分绩点之和
      let totalCreditGpa = 0;
      let totalCredits = 0;
      let totalCreditGpaNonElective = 0;
      let totalCreditsNonElective = 0;

      Object.keys(courseGradePoints).forEach((courseName) => {
        const credit = courseCredits[courseName] || 0;
        const gradePoint = courseGradePoints[courseName];
        const creditGpa = credit * gradePoint;

        totalCreditGpa += creditGpa;
        totalCredits += credit;

        // 如果不是公选课，计入非公选课总和
        const nature = courseNature[courseName] || "";
        if (nature !== "公选课") {
          totalCreditGpaNonElective += creditGpa;
          totalCreditsNonElective += credit;
        }
      });

      // 计算学年绩点
      const yearGpa = totalCredits > 0 ? totalCreditGpa / totalCredits : 0;

      // 计算学业分成绩
      const nonElectiveGpa =
        totalCreditsNonElective > 0
          ? totalCreditGpaNonElective / totalCreditsNonElective
          : 0;
      const comprehensiveScore = (nonElectiveGpa + 5) * 9;

      // 获取各类活动加分
      const academicScore = await getActivityScores(score.sno, "academic");
      const laborScore = await getActivityScores(score.sno, "labor");
      const sportsScore = await getActivityScores(score.sno, "sports");
      const innovationScore = await getActivityScores(score.sno, "innovation");

      // 计算综测分数
      const academicTotal = comprehensiveScore + academicScore;
      const laborTotal = 45 + laborScore;
      const sportsTotal = 45 + sportsScore;
      const innovationTotal = 40 + innovationScore;

      const zongce =
        academicTotal * 0.65 +
        laborTotal * 0.05 +
        sportsTotal * 0.05 +
        innovationTotal * 0.15;

      processedScores.push({
        ...score,
        creditGpa: parseFloat(totalCreditGpa.toFixed(2)),
        yearGpa: parseFloat(yearGpa.toFixed(2)),
        comprehensiveScore: parseFloat(comprehensiveScore.toFixed(2)),
        academic: parseFloat(academicScore.toFixed(2)),
        labor: parseFloat(laborScore.toFixed(2)),
        sports: parseFloat(sportsScore.toFixed(2)),
        innovation: parseFloat(innovationScore.toFixed(2)),
        zongce: parseFloat(zongce.toFixed(2)),
      });
    }

    tableData.value = processedScores;
    console.log("处理后的成绩数据:", tableData.value);
  } catch (error) {
    console.error("获取成绩数据失败:", error);
    ElMessage.error("获取成绩数据失败");
  }
};

// 修改导出Excel方法
const exportXlsx = () => {
  if (!hasSetBasicInfo.value) {
    ElMessage.warning("请先填写成绩基本信息");
    return;
  }

  const headers = columns.value.map((col) => col.label);
  const list = [headers];

  tableData.value.forEach((item) => {
    const row = columns.value.map((col) => String(item[col.prop] || ""));
    list.push(row);
  });

  const WorkSheet = XLSX.utils.aoa_to_sheet(list);
  const new_workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(new_workbook, WorkSheet, "成绩表");
  XLSX.writeFile(
    new_workbook,
    `学生成绩表_${filterForm.value.department}_${filterForm.value.major}_${filterForm.value.grade}.xlsx`
  );
};

// 修改保存方法
const handleSave = async () => {
  try {
    const data = {
      department: filterForm.value.department,
      major: filterForm.value.major,
      grade: filterForm.value.grade,
      tests: tableData.value.map((item) => ({
        sno: item.sno,
        name: item.name,
        class_name: item.class_name,
        ...Object.fromEntries(
          columns.value
            .filter(
              (col) =>
                ![
                  "sno",
                  "name",
                  "class_name",
                  "creditGpa",
                  "yearGpa",
                  "comprehensiveScore",
                  "academic",
                  "labor",
                  "sports",
                  "innovation",
                  "zongce",
                ].includes(col.prop)
            )
            .map((col) => [col.prop, item[col.prop]])
        ),
        credit_gpa: item.creditGpa,
        year_gpa: item.yearGpa,

        academic: item.academic,
        labor: item.labor,
        sports: item.sports,
        innovation: item.innovation,
        zongce: item.zongce,
        comprehensive: item.comprehensiveScore,
      })),
    };

    const res = await saveComprehensiveTestReq(data);
    if (res.data.code === 200) {
      ElMessage.success(`成功保存 ${res.data.data.success} 条综合测评数据`);
    } else {
      ElMessage.error(res.data.message || "保存失败");
    }
  } catch (error) {
    console.error("保存失败:", error);
    ElMessage.error(error.response?.data?.msg || "保存失败");
  }
};

// 移除原有的onMounted初始化
onMounted(() => {
  // 不再自动加载数据，等待用户选择筛选条件
});
</script>

<style scoped>
.handle-box {
  margin-bottom: 20px;
}

.handle-select {
  width: 120px;
}

.handle-input {
  width: 300px;
}

.table {
  width: 100%;
  font-size: 14px;
}

.red {
  color: #f56c6c;
}

.table-td-thumb {
  display: block;
  margin: auto;
  width: 40px;
  height: 40px;
}
</style>
