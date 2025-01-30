<template>
  <div class="login-bg">
    <div class="login-container">
      <div class="login-header">
        <img class="logo mr10" src="../../assets/img/logo.svg" alt="" />
        <div class="login-title">后台管理系统</div>
      </div>
      <el-form :model="param" :rules="rules" ref="login" size="large">
        <el-form-item prop="username">
          <el-input v-model="param.username" placeholder="用户名">
            <template #prepend>
              <el-icon>
                <User />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            placeholder="密码"
            v-model="param.password"
            @keyup.enter="submitForm(login)"
          >
            <template #prepend>
              <el-icon>
                <Lock />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <div class="pwd-tips">
          <el-checkbox
            class="pwd-checkbox"
            v-model="checked"
            label="记住密码"
          />
        </div>
        <el-button
          class="login-btn"
          type="primary"
          size="large"
          @click="submitForm(login)"
          >登录</el-button
        >
        <p class="login-text">
          没有账号？<el-link type="primary" @click="$router.push('/register')"
            >立即注册</el-link
          >
        </p>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { useTabsStore } from "@/store/tabs";
import { usePermissStore } from "@/store/permiss";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import { getRouterReq, loginReq, userInfoReq } from "@/api";
import { setToken } from "@/utils/auth";

interface LoginInfo {
  username: string;
  password: string;
}
const lgStr = localStorage.getItem("login-param");
const defParam = lgStr ? JSON.parse(lgStr) : null;
const checked = ref(lgStr ? true : false);

const router = useRouter();
const param = reactive<LoginInfo>({
  username: defParam ? defParam.username : "",
  password: defParam ? defParam.password : "",
});
const rules: FormRules = {
  username: [
    {
      required: true,
      message: "请输入用户名",
      trigger: "blur",
    },
  ],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
};
const permiss = usePermissStore();
const login = ref<FormInstance>();
const loginFunc = () => {
  loginReq(param)
    .then(async ({ data }) => {
      console.log("登录响应:", data);

      if (data.code === 200) {
        ElMessage.success("登录成功");
        setToken(data.data.token);
        localStorage.setItem("vuems_name", param.username);

        try {
          // 获取用户信息
          const userInfo = await userInfoReq();
          console.log("用户信息:", userInfo);

          // 获取路由权限
          const routeInfo = await getRouterReq();
          console.log("获取到的路由信息:", routeInfo.data);
          console.log("12312", routeInfo.data.data.routes);

          // 设置权限
          if (routeInfo.data.data && routeInfo.data.data.routes) {
            console.log("111111111111");

            permiss.handleSet(routeInfo.data.data.routes);
          }

          router.push("/");
        } catch (error) {
          console.error("获取信息失败:", error);
          ElMessage.error("获取用户信息失败");
        }
      } else {
        ElMessage.error(data.msg || "登录失败");
      }
    })
    .catch((error) => {
      console.error("登录请求失败:", error);
      ElMessage.error("登录失败");
    });
};
const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid: boolean) => {
    if (valid) {
      loginFunc();
    }
  });
};
//   ElMessage.success("登录成功");
//   localStorage.setItem("vuems_name", param.username);
//   const keys =
//     permiss.defaultList[param.username == "admin" ? "admin" : "user"];
//   permiss.handleSet(keys);
//   router.push("/");
//   if (checked.value) {
//     localStorage.setItem("login-param", JSON.stringify(param));
//   } else {
//     localStorage.removeItem("login-param");
//   }
// } else {
//   ElMessage.error("登录失败");
//   return false;
// }
// });
// }

// const tabs = useTabsStore();
// tabs.clearTabs();
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

.pwd-tips {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  margin: -10px 0 10px;
  color: #787878;
}

.pwd-checkbox {
  height: auto;
}

.login-btn {
  display: block;
  width: 100%;
}

.login-tips {
  font-size: 12px;
  color: #999;
}

.login-text {
  display: flex;
  align-items: center;
  margin-top: 20px;
  font-size: 14px;
  color: #787878;
}
</style>
