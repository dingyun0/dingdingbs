import { defineStore } from "pinia";

interface ObjectList {
  [key: string]: string[];
}

export const usePermissStore = defineStore("permiss", {
  state: () => {
    const defaultList: ObjectList = {
      admin: [
        "0",
        "1",
        "12",
        "13",
        "14",
        "2",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "291",
        "292",
        "3",
        "31",
        "32",
        "33",
        "34",
        "4",
        "41",
        "42",
        "5",
        "51",
        "52",
        "53",
        "7",
        "6",
        "61",
        "62",
        "63",
        "64",
        "65",
        "66",
        "13",
        "131",
        "151",
        "171",
      ],
      teacher: [
        "0",
        "3",
        "31",
        "32",
        "33",
        "34",
        "7",
        "12",
        "16",
        "161",
        "162",
        "151",
      ],
      student: [
        "0",
        "8",
        "81",
        "82",
        "7",
        "9",
        "91",
        "92",
        "11",
        "111",
        "112",
        "151",
      ],
    };

    // 首先尝试从localStorage恢复权限
    const savedPermissions = localStorage.getItem("vuems_permissions");
    if (savedPermissions) {
      return {
        key: JSON.parse(savedPermissions),
        defaultList,
      };
    }

    // 如果没有保存的权限，则根据用户名分配默认权限
    const username = localStorage.getItem("vuems_name");
    console.log(username);
    let key: string[] = [];
    if (username == "admin") {
      key = defaultList.admin;
    } else if (username == "teacher") {
      key = defaultList.teacher;
    } else if (username == "student") {
      key = defaultList.student;
    }

    // 保存默认权限到localStorage
    if (key.length > 0) {
      localStorage.setItem("vuems_permissions", JSON.stringify(key));
    }

    return {
      key,
      defaultList,
    };
  },
  actions: {
    handleSet(val: string[]) {
      this.key = val;
      // 当设置新的权限时，同时保存到localStorage
      localStorage.setItem("vuems_permissions", JSON.stringify(val));
    },
    // 清除权限信息
    clearPermissions() {
      this.key = [];
      localStorage.removeItem("vuems_permissions");
    },
  },
});
