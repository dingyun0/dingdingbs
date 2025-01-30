import axios from "axios";
import { getToken } from "@/utils/auth";
import { ElMessage } from "element-plus";

const service = axios.create({
  baseURL: "http://127.0.0.1:9005/ai",
  timeout: 5000,
});

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error("请求错误:", error);
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error("响应错误:", error);
    if (error.response) {
      switch (error.response.status) {
        case 401:
          ElMessage.error("未授权，请重新登录");
          // 清除 token 并跳转到登录页
          localStorage.clear();
          window.location.href = "/#/login";
          break;
        case 403:
          ElMessage.error("拒绝访问");
          break;
        case 404:
          ElMessage.error("请求错误,未找到该资源");
          break;
        case 500:
          ElMessage.error("服务器端出错");
          break;
        default:
          ElMessage.error("未知错误");
      }
    }
    return Promise.reject(error);
  }
);

export default service;
