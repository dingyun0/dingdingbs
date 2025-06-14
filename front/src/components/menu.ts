import { Menus } from "@/types/menu";

export const menuData: Menus[] = [
  {
    id: "181",
    icon: "Calendar",
    index: "/admin/guide",
    title: "管理员端指南",
  },
  {
    id: "191",
    icon: "Calendar",
    index: "/teacher/guide",
    title: "老师端指南",
  },
  {
    id: "201",
    icon: "Calendar",
    index: "/student/guide",
    title: "学生端指南",
  },
  {
    id: "1",
    title: "系统管理",
    index: "1",
    icon: "HomeFilled",
    children: [
      {
        id: "12",
        pid: "1",
        index: "/management-allUsers",
        title: "角色管理",
      },
      {
        id: "13",
        pid: "1",
        index: "/management-student",
        title: "学生管理",
      },
      {
        id: "14",
        pid: "1",
        index: "/management-teacher",
        title: "老师管理",
      },
    ],
  },
  {
    id: "2",
    title: "组件",
    index: "2-1",
    icon: "Calendar",
    children: [
      {
        id: "21",
        pid: "3",
        index: "/form",
        title: "表单",
      },
      {
        id: "22",
        pid: "3",
        index: "/upload",
        title: "上传",
      },
      {
        id: "23",
        pid: "2",
        index: "/carousel",
        title: "走马灯",
      },
      {
        id: "24",
        pid: "2",
        index: "/calendar",
        title: "日历",
      },
      {
        id: "25",
        pid: "2",
        index: "/watermark",
        title: "水印",
      },
      {
        id: "26",
        pid: "2",
        index: "/tour",
        title: "分布引导",
      },
      {
        id: "27",
        pid: "2",
        index: "/steps",
        title: "步骤条",
      },
      {
        id: "28",
        pid: "2",
        index: "/statistic",
        title: "统计",
      },
      {
        id: "29",
        pid: "3",
        index: "29",
        title: "三级菜单",
        children: [
          {
            id: "291",
            pid: "29",
            index: "/editor",
            title: "富文本编辑器",
          },
          {
            id: "292",
            pid: "29",
            index: "/markdown",
            title: "markdown编辑器",
          },
        ],
      },
    ],
  },

  {
    id: "33",
    icon: "Guide",
    index: "/importScore",
    title: "成绩管理",
  },
  {
    id: "16",
    icon: "Guide",
    index: "16",
    title: "审核管理",
    children: [
      {
        id: "161",
        pid: "Calendar",
        index: "/activity/reviewActivity",
        title: "审核学生活动申请",
      },
      {
        id: "162",
        pid: "Calendar",
        index: "/activity/reviewScore",
        title: "审核学生成绩疑惑",
      },
    ],
  },
  {
    id: "34",
    icon: "Guide",
    index: "/exportComprehensive",
    title: "综测管理",
  },

  {
    id: "4",
    icon: "PieChart",
    index: "4",
    title: "图表",
    children: [
      {
        id: "41",
        pid: "4",
        index: "/schart",
        title: "schart图表",
      },
      {
        id: "42",
        pid: "4",
        index: "/echarts",
        title: "echarts图表",
      },
    ],
  },
  {
    id: "5",
    icon: "Guide",
    index: "5",
    title: "公告管理",
    children: [
      {
        id: "51",
        pid: "5",
        index: "/announcement/activity",
        title: "活动公告",
      },
      {
        id: "52",
        pid: "5",
        index: "/announcement/scholarship",
        title: "奖学金公告",
      },
      {
        id: "53",
        pid: "5",
        index: "/announcement/school",
        title: "学校公告",
      },
    ],
  },
  {
    id: "9",
    icon: "Guide",
    index: "9",
    title: "查看公告",
    children: [
      {
        id: "91",
        pid: "9",
        index: "/showAnnouncement/school",
        title: "学校公告",
      },
      {
        id: "92",
        pid: "9",
        index: "/showAnnouncement/scholarship",
        title: "奖学金公告",
      },
      // {
      //   id: "93",
      //   pid: "9",
      //   index: "/showAnnouncement/activate",
      //   title: "活动公告",
      // },
    ],
  },
  // {
  //   id: "10",
  //   icon: "Calendar",
  //   index: "/activity/activity",
  //   title: "活动",
  // },
  {
    id: "171",
    icon: "Guide",
    index: "/college/collegeMajor",
    title: "学院管理",
  },
  {
    id: "11",
    icon: "Guide",
    index: "11",
    title: "查看活动",
    children: [
      {
        id: "111",
        pid: "Calendar",
        index: "/activity/showActivity",
        title: "查看活动",
      },
      {
        id: "113",
        pid: "Calendar",
        index: "/activity/otherActivity",
        title: "其他活动加分申请",
      },
      {
        id: "112",
        pid: "Calendar",
        index: "/activity/reviewMessage",
        title: "查看活动审核结果",
      },
    ],
  },

  {
    id: "13",
    icon: "Guide",
    index: "13",
    title: "课程管理",
    children: [
      {
        id: "131",
        pid: "Calendar",
        index: "/importSession",
        title: "导入课程",
      },
    ],
  },
  {
    id: "8",
    icon: "Calendar",
    index: "/showComprehensive",
    title: "查看成绩",
    children: [
      {
        id: "81",
        pid: "8",
        index: "/showComprehensive",
        title: "查看综测成绩",
      },
      {
        id: "82",
        pid: "8",
        index: "/reviewResult",
        title: "查看综测审核结果",
      },
    ],
  },
  {
    id: "7",
    icon: "Brush",
    index: "/theme",
    title: "主题管理",
  },
  {
    id: "151",
    icon: "Calendar",
    index: "/ucenter",
    title: "个人中心",
  },

  {
    id: "6",
    icon: "DocumentAdd",
    index: "6",
    title: "附加页面",
    children: [
      {
        id: "61",
        pid: "6",
        index: "/ucenter",
        title: "个人中心",
      },
      {
        id: "62",
        pid: "6",
        index: "/login",
        title: "登录",
      },
      {
        id: "63",
        pid: "6",
        index: "/register",
        title: "注册",
      },
      {
        id: "64",
        pid: "6",
        index: "/reset-pwd",
        title: "重设密码",
      },
      {
        id: "65",
        pid: "6",
        index: "/403",
        title: "403",
      },
      {
        id: "66",
        pid: "6",
        index: "/404",
        title: "404",
      },
    ],
  },
];
