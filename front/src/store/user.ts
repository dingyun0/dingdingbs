import { defineStore } from "pinia";

interface UserState {
  id: number | string;
  username: string;
  roles: string;
  token: string;
}

export const useUserStore = defineStore("user", {
  state: (): UserState => ({
    id: "",
    username: localStorage.getItem("vuems_name") || "",
    roles: "",
    token: localStorage.getItem("token") || "",
  }),

  actions: {
    // 设置用户信息
    setUserInfo(userInfo: any) {
      this.id = userInfo.id;
      this.username = userInfo.username;
      this.roles = userInfo.roles;
    },

    // 设置 token
    setToken(token: string) {
      this.token = token;
      localStorage.setItem("token", token);
    },

    // 设置用户名
    setUsername(username: string) {
      this.username = username;
      localStorage.setItem("vuems_name", username);
    },

    // 清除用户信息
    clearUserInfo() {
      this.id = "";
      this.username = "";
      this.roles = "";
      this.token = "";
      localStorage.removeItem("token");
      localStorage.removeItem("vuems_name");
    },
  },
});
