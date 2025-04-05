import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import { usePermissStore } from "../store/permiss";
import Home from "../views/home.vue";
import NProgress from "nprogress";
import "nprogress/nprogress.css";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/dashboard",
  },
  {
    path: "/",
    name: "Home",
    component: Home,
    children: [
      {
        path: "/dashboard",
        name: "dashboard",
        meta: {
          title: "系统首页",
          noAuth: true,
        },
        component: () =>
          import(/* webpackChunkName: "dashboard" */ "../views/dashboard.vue"),
      },

      {
        path: "/management-allUsers",
        name: "management-allUsers",
        meta: {
          title: "用户管理",
          permiss: "12",
        },
        component: () =>
          import(
            /* webpackChunkName: "system-role" */ "../views/admin/management/allUsers.vue"
          ),
      },
      {
        path: "/management-student",
        name: "management-student",
        meta: {
          title: "学生管理",
          permiss: "13",
        },
        component: () =>
          import(
            /* webpackChunkName: "system-role" */ "../views/admin/management/student.vue"
          ),
      },
      {
        path: "/management-teacher",
        name: "management-teacher",
        meta: {
          title: "老师管理",
          permiss: "14",
        },
        component: () =>
          import(
            /* webpackChunkName: "system-role" */ "../views/admin/management/teacher.vue"
          ),
      },

      {
        path: "/schart",
        name: "schart",
        meta: {
          title: "schart图表",
          permiss: "41",
        },
        component: () =>
          import(/* webpackChunkName: "schart" */ "../views/chart/schart.vue"),
      },
      {
        path: "/echarts",
        name: "echarts",
        meta: {
          title: "echarts图表",
          permiss: "42",
        },
        component: () =>
          import(
            /* webpackChunkName: "echarts" */ "../views/chart/echarts.vue"
          ),
      },

      {
        path: "/announcement/activity",
        name: "activity",
        meta: {
          title: "活动公告",
          permiss: "51",
        },
        component: () =>
          import(
            /* webpackChunkName: "icon" */ "../views/admin/announcement/activity.vue"
          ),
      },
      {
        path: "/announcement/scholarship",
        name: "scholarship",
        meta: {
          title: "奖学金公告",
          permiss: "52",
        },
        component: () =>
          import(
            /* webpackChunkName: "icon" */ "../views/admin/announcement/scholarship.vue"
          ),
      },
      {
        path: "/announcement/school",
        name: "school",
        meta: {
          title: "学校公告",
          permiss: "53",
        },
        component: () =>
          import(
            /* webpackChunkName: "icon" */ "../views/admin/announcement/school.vue"
          ),
      },
      {
        path: "/ucenter",
        name: "ucenter",
        meta: {
          title: "个人中心",
        },
        component: () =>
          import(
            /* webpackChunkName: "ucenter" */ "../views/common/ucenter.vue"
          ),
      },
      {
        path: "/editor",
        name: "editor",
        meta: {
          title: "富文本编辑器",
          permiss: "29",
        },
        component: () =>
          import(/* webpackChunkName: "editor" */ "../views/pages/editor.vue"),
      },
      {
        path: "/markdown",
        name: "markdown",
        meta: {
          title: "markdown编辑器",
          permiss: "292",
        },
        component: () =>
          import(
            /* webpackChunkName: "markdown" */ "../views/pages/markdown.vue"
          ),
      },
      {
        path: "/exportComprehensive",
        name: "exportComprehensive",
        meta: {
          title: "导出学业分Excel",
          permiss: "34",
        },
        component: () =>
          import(
            /* webpackChunkName: "export" */ "../views/teacher/score/exportComprehensive.vue"
          ),
      },
      {
        path: "/importScore",
        name: "importScore",
        meta: {
          title: "导入成绩Excel",
          permiss: "33",
        },
        component: () =>
          import(
            /* webpackChunkName: "import" */ "../views/teacher/score/importScore.vue"
          ),
      },

      {
        path: "/theme",
        name: "theme",
        meta: {
          title: "主题设置",
          permiss: "7",
        },
        component: () =>
          import(/* webpackChunkName: "theme" */ "../views/common/theme.vue"),
      },
      {
        path: "/showComprehensive",
        name: "showComprehensive",
        meta: {
          title: "查看综测分",
          permiss: "81",
        },
        component: () =>
          import(
            /* webpackChunkName: "theme" */ "../views/student/comprehensive/showComprehensive.vue"
          ),
      },
      {
        path: "/reviewResult",
        name: "reviewResult",
        meta: {
          title: "查看综测审核结果",
          permiss: "82",
        },
        component: () =>
          import(
            /* webpackChunkName: "theme" */ "../views/student/comprehensive/reviewResult.vue"
          ),
      },

      {
        path: "/showAnnouncement/school",
        name: "showSchoolAnnouncement",
        meta: {
          title: "查看学校公告",
          permiss: "91",
        },
        component: () =>
          import(
            /* webpackChunkName: "theme" */ "../views/student/showAnnouncement/school.vue"
          ),
      },
      {
        path: "/showAnnouncement/scholarship",
        name: "showScholarshipAnnouncement",
        meta: {
          title: "查看奖学金公告",
          permiss: "92",
        },
        component: () =>
          import(
            /* webpackChunkName: "theme" */ "../views/student/showAnnouncement/scholarship.vue"
          ),
      },
      // {
      //   path: "/showAnnouncement/activate",
      //   name: "showActivateAnnouncement",
      //   meta: {
      //     title: "查看活动公告",
      //     permiss: "93",
      //   },
      //   component: () =>
      //     import(
      //       /* webpackChunkName: "theme" */ "../views/student/showAnnouncement/activate.vue"
      //     ),
      // },
      // {
      //   path: "/activity/activity",
      //   name: "activity",
      //   meta: {
      //     title: "活动",
      //     permiss: "101",
      //   },
      //   component: () =>
      //     import(
      //       /* webpackChunkName: "theme" */ "../views/admin/announcement/activity.vue"
      //     ),
      // },
      {
        path: "/activity/showActivity",
        name: "showActivity",
        meta: {
          title: "查看活动",
          permiss: "111",
        },
        component: () =>
          import(
            /* webpackChunkName: "theme" */ "../views/student/activity/showActivity.vue"
          ),
      },
      {
        path: "/activity/reviewMessage",
        name: "reviewMessage",
        meta: {
          title: "查看活动审核结果",
          permiss: "112",
        },
        component: () =>
          import(
            /* webpackChunkName: "theme" */ "../views/student/activity/reviewMessage.vue"
          ),
      },
      {
        path: "/activity/reviewActivity",
        name: "reviewActivity",
        meta: {
          title: "审核学生活动申请",
          permiss: "161",
        },
        component: () =>
          import(
            /* webpackChunkName: "theme" */ "../views/teacher/activity/reviewActivity.vue"
          ),
      },
      {
        path: "/activity/reviewScore",
        name: "reviewScore",
        meta: {
          title: "审核学生成绩疑惑",
          permiss: "162",
        },
        component: () =>
          import(
            /* webpackChunkName: "theme" */ "../views/teacher/activity/reviewScore.vue"
          ),
      },
      {
        path: "/college/collegeMajor",
        name: "collegeMajor",
        meta: {
          title: "学院专业管理",
          permiss: "171",
        },
        component: () =>
          import(
            /* webpackChunkName: "theme" */ "../views/admin/college/college_major.vue"
          ),
      },
      {
        path: "/importSession",
        name: "importSession",
        meta: {
          title: "导入所有课程",
          permiss: "131",
        },
        component: () =>
          import(
            /* webpackChunkName: "theme" */ "../views/admin/session/importSession.vue"
          ),
      },
      {
        path: "/ucenter",
        name: "ucenter",
        meta: {
          title: "个人中心",
          permiss: "151",
        },
        component: () =>
          import(/* webpackChunkName: "theme" */ "../views/common/ucenter.vue"),
      },

      {
        path: "/watermark",
        name: "watermark",
        meta: {
          title: "水印",
          permiss: "25",
        },
        component: () =>
          import(
            /* webpackChunkName: "watermark" */ "../views/element/watermark.vue"
          ),
      },
      {
        path: "/carousel",
        name: "carousel",
        meta: {
          title: "走马灯",
          permiss: "23",
        },
        component: () =>
          import(
            /* webpackChunkName: "carousel" */ "../views/element/carousel.vue"
          ),
      },
      {
        path: "/tour",
        name: "tour",
        meta: {
          title: "分步引导",
          permiss: "26",
        },
        component: () =>
          import(/* webpackChunkName: "tour" */ "../views/element/tour.vue"),
      },
      {
        path: "/steps",
        name: "steps",
        meta: {
          title: "步骤条",
          permiss: "27",
        },
        component: () =>
          import(/* webpackChunkName: "steps" */ "../views/element/steps.vue"),
      },
      {
        path: "/form",
        name: "forms",
        meta: {
          title: "表单",
          permiss: "21",
        },
        component: () =>
          import(/* webpackChunkName: "form" */ "../views/element/form.vue"),
      },
      {
        path: "/upload",
        name: "upload",
        meta: {
          title: "上传",
          permiss: "22",
        },
        component: () =>
          import(
            /* webpackChunkName: "upload" */ "../views/element/upload.vue"
          ),
      },
      {
        path: "/statistic",
        name: "statistic",
        meta: {
          title: "统计",
          permiss: "28",
        },
        component: () =>
          import(
            /* webpackChunkName: "statistic" */ "../views/element/statistic.vue"
          ),
      },
    ],
  },
  {
    path: "/login",
    meta: {
      title: "登录",
      noAuth: true,
    },
    component: () =>
      import(/* webpackChunkName: "login" */ "../views/common/login.vue"),
  },
  {
    path: "/register",
    meta: {
      title: "注册",
      noAuth: true,
    },
    component: () =>
      import(/* webpackChunkName: "register" */ "../views/common/register.vue"),
  },
  {
    path: "/reset-pwd",
    meta: {
      title: "重置密码",
      noAuth: true,
    },
    component: () =>
      import(
        /* webpackChunkName: "reset-pwd" */ "../views/pages/reset-pwd.vue"
      ),
  },
  {
    path: "/403",
    meta: {
      title: "没有权限",
      noAuth: true,
    },
    component: () =>
      import(/* webpackChunkName: "403" */ "../views/pages/403.vue"),
  },
  {
    path: "/404",
    meta: {
      title: "找不到页面",
      noAuth: true,
    },
    component: () =>
      import(/* webpackChunkName: "404" */ "../views/pages/404.vue"),
  },
  { path: "/:path(.*)", redirect: "/404" },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  NProgress.start();
  const role = localStorage.getItem("vuems_name");
  const permiss = usePermissStore();

  if (!role && to.meta.noAuth !== true) {
    next("/login");
  } else if (
    typeof to.meta.permiss == "string" &&
    !permiss.key.includes(to.meta.permiss)
  ) {
    // 如果没有权限，则进入403
    next("/403");
  } else {
    next();
  }
});

router.afterEach(() => {
  NProgress.done();
});

export default router;
