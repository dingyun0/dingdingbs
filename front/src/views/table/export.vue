<template>
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
          label="综测成绩"
          width="100"
        ></el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts" name="export">
import { ref, onMounted } from "vue";
import * as XLSX from "xlsx";
import { ElMessage } from "element-plus";
import { getSessionAll } from "@/api/session";
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
}

const tableData = ref<StudentScore[]>([]);
const courseData = ref<CourseInfo[]>([]);

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

// 获取成绩数据并计算绩点
const getScoreData = async () => {
  try {
    const response = await getScoreAll();
    console.log("11111111111", response);

    const scores = response.data.data || [];

    // 确保课程数据已加载
    if (courseData.value.length === 0) {
      await getCourseData();
    }

    // 创建课程名称到学分的映射
    const courseCredits: Record<string, number> = {};
    const courseNature: Record<string, string> = {};

    courseData.value.forEach((course) => {
      courseCredits[course.course_name] = parseFloat(course.credit) || 0;
      courseNature[course.course_name] = course.nature;
    });

    // 处理每个学生的成绩
    tableData.value = scores.map((score: any) => {
      // 计算每门课的绩点
      const courseGradePoints: Record<string, number> = {
        操作系统课程设计成绩: calculateGradePoint(score.操作系统课程设计成绩),
        无线网络技术成绩: calculateGradePoint(score.无线网络技术成绩),
        计算机网络课程设计: calculateGradePoint(score.计算机网络课程设计),
        操作系统: calculateGradePoint(score.操作系统),
        人工智能与网络技术学科前沿: calculateGradePoint(
          score.人工智能与网络技术学科前沿
        ),
        信息安全原理及应用: calculateGradePoint(score.信息安全原理及应用),
        Linux操作系统: calculateGradePoint(score.Linux操作系统),
        Java程序设计: calculateGradePoint(score.Java程序设计),
      };

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

      // 计算综测成绩
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

// 页面加载时获取数据
onMounted(async () => {
  await getScoreData();
});

// 导出Excel
const exportXlsx = () => {
  // 表头
  const headers = [
    "学号",
    "姓名",
    "班级",
    "操作系统课程设计成绩",
    "无线网络技术成绩",
    "计算机网络课程设计",
    "操作系统",
    "人工智能与网络技术学科前沿",
    "信息安全原理及应用",
    "Linux操作系统",
    "Java程序设计",
    "学分绩点",
    "学年绩点",
    "综测成绩",
  ];

  const list = [headers];

  // 添加数据行
  tableData.value.forEach((item) => {
    const row = [
      item.sno,
      item.name,
      item.class_name,
      item.操作系统课程设计成绩,
      item.无线网络技术成绩,
      item.计算机网络课程设计,
      item.操作系统,
      item.人工智能与网络技术学科前沿,
      item.信息安全原理及应用,
      item.Linux操作系统,
      item.Java程序设计,
      item.creditGpa,
      item.yearGpa,
      item.comprehensiveScore,
    ];
    list.push(row);
  });

  // 创建工作表
  let WorkSheet = XLSX.utils.aoa_to_sheet(list);
  let new_workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(new_workbook, WorkSheet, "成绩表");
  XLSX.writeFile(new_workbook, `学生成绩表.xlsx`);
};

// 添加保存功能
const handleSave = async () => {
  try {
    console.log("保存综合测评数据");

    const data = {
      tests: tableData.value.map((item) => ({
        sno: item.sno,
        name: item.name,
        class_name: item.class_name,
        操作系统课程设计成绩: item.操作系统课程设计成绩,
        无线网络技术成绩: item.无线网络技术成绩,
        计算机网络课程设计: item.计算机网络课程设计,
        操作系统: item.操作系统,
        人工智能与网络技术学科前沿: item.人工智能与网络技术学科前沿,
        信息安全原理及应用: item.信息安全原理及应用,
        Linux操作系统: item.Linux操作系统,
        Java程序设计: item.Java程序设计,
        credit_gpa: item.creditGpa,
        year_gpa: item.yearGpa,
        comprehensive_score: item.comprehensiveScore,
      })),
    };

    console.log("发送的数据结构:", JSON.stringify(data, null, 2));
    const res = await saveComprehensiveTestReq(data);
    if (res.code === 200) {
      ElMessage.success(`成功保存 ${res.data.success} 条综合测评数据`);
    } else {
      ElMessage.error(res.message || "保存失败");
    }
  } catch (error) {
    console.error("保存失败:", error);
    ElMessage.error(error.response?.data?.msg || "保存失败");
  }
};
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
