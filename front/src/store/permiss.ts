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
        "11",
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
        "10",
        "101",
        "13",
        "131",
      ],
      teacher: ["0", "3", "31", "32", "33", "34", "7", "121"],
      student: ["0", "8", "7", "9", "91", "92", "11", "111", "112"],
    };
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
    return {
      key,
      defaultList,
    };
  },
  actions: {
    handleSet(val: string[]) {
      this.key = val;
    },
  },
});
