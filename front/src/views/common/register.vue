<template>
  <div class="login-bg">
    <div class="login-container">
      <div class="login-header">
        <img class="logo mr10" src="../../assets/img/logo.svg" alt="" />
        <div class="login-title">智评奖学金管理系统</div>
      </div>
      <el-form :model="param" :rules="rules" ref="register" size="large">
        <el-form-item prop="username">
          <el-input v-model="param.username" placeholder="用户名">
            <template #prepend>
              <el-icon>
                <User />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="sno">
          <el-input v-model="param.sno" placeholder="学号">
            <template #prepend>
              <el-icon>
                <Document />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="department">
          <el-select
            v-model="param.department"
            placeholder="请选择学院"
            style="width: 100%"
          >
            <template #prefix>
              <el-icon><School /></el-icon>
            </template>
            <el-option
              v-for="dept in departments"
              :key="dept.value"
              :label="dept.label"
              :value="dept.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item prop="major">
          <el-select
            v-model="param.major"
            placeholder="请选择专业"
            style="width: 100%"
            :disabled="!param.department"
          >
            <template #prefix>
              <el-icon><Notebook /></el-icon>
            </template>
            <el-option
              v-for="major in availableMajors"
              :key="major"
              :label="major"
              :value="major"
            />
          </el-select>
        </el-form-item>
        <el-form-item prop="grade">
          <el-select
            v-model="param.grade"
            placeholder="请选择年级"
            style="width: 100%"
          >
            <template #prefix>
              <el-icon><Calendar /></el-icon>
            </template>
            <el-option
              v-for="grade in availableGrades"
              :key="grade"
              :label="grade"
              :value="grade"
            />
          </el-select>
        </el-form-item>
        <el-form-item prop="class_name">
          <el-input v-model="param.class_name" placeholder="班级">
            <template #prepend>
              <el-icon>
                <Collection />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            placeholder="密码"
            v-model="param.password"
            @keyup.enter="submitForm(register)"
          >
            <template #prepend>
              <el-icon>
                <Lock />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input
            type="password"
            placeholder="确认密码"
            v-model="param.confirmPassword"
            @keyup.enter="submitForm(register)"
          >
            <template #prepend>
              <el-icon>
                <Lock />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-button
          class="login-btn"
          type="primary"
          size="large"
          @click="submitForm(register)"
          >注册</el-button
        >
        <p class="login-text">
          已有账号，<el-link type="primary" @click="$router.push('/login')"
            >立即登录</el-link
          >
        </p>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onBeforeMount } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";
import { Register } from "@/types/user";
import { registerReq } from "@/api";
import { getCollegeList } from "@/api/college";

const router = useRouter();
const param = reactive<Register>({
  username: "",
  password: "",
  confirmPassword: "",
  sno: "",
  department: "",
  major: "",
  grade: "",
  class_name: "",
});

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
    ...dept,
    majors: Array.from(dept.majors),
  }));
});

// 根据选择的学院计算可选的专业
const availableMajors = computed(() => {
  const selectedDept = departments.value.find(
    (dept) => dept.value === param.department
  );
  return selectedDept ? selectedDept.majors : [];
});

// 获取可选的年级
const availableGrades = computed(() => {
  if (!param.department || !param.major) return [];
  const grades = new Set();
  collegeData.value
    .filter(
      (item) =>
        item.department === param.department && item.major === param.major
    )
    .forEach((item) => grades.add(item.grade));
  return Array.from(grades);
});

// 监听学院变化，重置专业选择
watch(
  () => param.department,
  () => {
    param.major = "";
    param.grade = "";
  }
);

// 监听专业变化，重置年级选择
watch(
  () => param.major,
  () => {
    param.grade = "";
  }
);

const rules: FormRules = {
  username: [
    {
      required: true,
      message: "请输入用户名",
      trigger: "blur",
    },
  ],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
  email: [{ required: true, message: "请输入邮箱", trigger: "blur" }],
  sno: [{ required: true, message: "请输入学号", trigger: "blur" }],
  department: [{ required: true, message: "请选择学院", trigger: "change" }],
  major: [{ required: true, message: "请选择专业", trigger: "change" }],
  grade: [{ required: true, message: "请选择年级", trigger: "change" }],
  class_name: [{ required: true, message: "请输入班级", trigger: "blur" }],
};

const register = ref<FormInstance>();

const registerFunc = () => {
  registerReq(param)
    .then((res) => {
      console.log("注册响应:", res);
      if (res.data.code === 200) {
        ElMessage.success(res.data.msg || "注册成功，请登录");
        router.push("/login");
      } else {
        ElMessage.error(res.data.msg || "注册失败");
      }
    })
    .catch((error) => {
      console.error("注册请求失败:", error);
      ElMessage.error("注册失败");
    });
};

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid: boolean) => {
    if (valid) {
      if (param.password !== param.confirmPassword) {
        ElMessage.error("两次密码输入不一致");
        return;
      } else {
        registerFunc();
      }
    } else {
      return false;
    }
  });
};

// 组件挂载前获取学院数据
onBeforeMount(async () => {
  await fetchCollegeData();
});
</script>

<style scoped>
.login-bg {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100vh;
  background: url(../../assets/img/login-bg.jpg) center/cover no-repeat;
}

.login-header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 40px;
}

.logo {
  width: 35px;
}

.login-title {
  font-size: 22px;
  color: #333;
  font-weight: bold;
}

.login-container {
  width: 450px;
  border-radius: 5px;
  background: #fff;
  padding: 40px 50px 50px;
  box-sizing: border-box;
}

.login-btn {
  display: block;
  width: 100%;
}

.login-text {
  display: flex;
  align-items: center;
  margin-top: 20px;
  font-size: 14px;
  color: #787878;
}

/* 添加下拉框的图标样式 */
:deep(.el-select .el-input .el-input__prefix) {
  left: 10px;
}

:deep(.el-select .el-input input) {
  padding-left: 35px;
}
</style>
