<template>
  <div class="guide-container">
    <!-- 顶部横幅 -->
    <div class="guide-banner">
      <div class="banner-content">
        <h1>智评奖学金管理系统</h1>
        <p class="subtitle">管理员端操作指南</p>
      </div>
    </div>

    <div class="guide-content">
      <!-- 系统特点介绍 -->
      <div class="section system-features">
        <div class="section-header">
          <h2>系统特点</h2>
          <div class="divider">
            <span class="line"></span>
            <el-icon><Star /></el-icon>
            <span class="line"></span>
          </div>
        </div>
        <el-row :gutter="30">
          <el-col
            :span="8"
            v-for="feature in systemFeatures"
            :key="feature.title"
          >
            <div class="feature-card" :class="feature.className">
              <div class="feature-icon">
                <el-icon :size="32">
                  <component :is="feature.icon" />
                </el-icon>
              </div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 功能模块指南 -->
      <div class="section function-guide">
        <div class="section-header">
          <h2>功能模块指南</h2>
          <div class="divider">
            <span class="line"></span>
            <el-icon><Menu /></el-icon>
            <span class="line"></span>
          </div>
        </div>
        <el-row :gutter="30">
          <el-col :span="12" v-for="guide in functionGuides" :key="guide.title">
            <div
              class="guide-card"
              :class="guide.className"
              @click="navigateTo(guide.path)"
              @mouseenter="guide.isHovered = true"
              @mouseleave="guide.isHovered = false"
            >
              <div
                class="guide-icon"
                :style="{ backgroundColor: guide.iconColor + '15' }"
              >
                <el-icon :size="32" :color="guide.iconColor">
                  <component :is="guide.icon" />
                </el-icon>
              </div>
              <div class="guide-info">
                <h3>{{ guide.title }}</h3>
                <p>{{ guide.description }}</p>
                <ul class="guide-features">
                  <li v-for="feature in guide.features" :key="feature">
                    {{ feature }}
                  </li>
                </ul>
                <el-button
                  class="guide-btn"
                  :type="guide.isHovered ? 'primary' : 'text'"
                  size="small"
                >
                  进入模块
                  <el-icon class="el-icon--right">
                    <ArrowRight />
                  </el-icon>
                </el-button>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { Star, Menu, ArrowRight } from "@element-plus/icons-vue";

const router = useRouter();

// 系统特点数据
const systemFeatures = [
  {
    icon: "User",
    iconColor: "#409EFF",
    title: "用户管理",
    description: "提供完整的用户管理功能，包括角色管理、学生管理和教师管理。",
    className: "feature-blue",
  },
  {
    icon: "Bell",
    iconColor: "#67C23A",
    title: "公告管理",
    description: "支持多类型公告发布，包括活动公告、奖学金公告和学校公告。",
    className: "feature-green",
  },
  {
    icon: "Document",
    iconColor: "#E6A23C",
    title: "课程管理",
    description: "提供课程导入和管理功能，支持灵活的课程设置。",
    className: "feature-orange",
  },
];

// 功能模块指南数据
const functionGuides = [
  {
    title: "系统管理",
    icon: "Setting",
    iconColor: "#409EFF",
    path: "/management-allUsers",
    description: "管理系统用户和权限",
    features: [
      "角色管理 - 分配不同角色的权限",
      "学生管理 - 管理学生用户信息",
      "教师管理 - 管理教师用户信息",
    ],
    className: "guide-blue",
    isHovered: ref(false),
  },
  {
    title: "公告管理",
    icon: "Bell",
    iconColor: "#67C23A",
    path: "/announcement/activity",
    description: "管理系统各类公告信息",
    features: [
      "活动公告 - 发布和管理活动相关公告",
      "奖学金公告 - 发布奖学金相关信息",
      "学校公告 - 发布学校重要通知",
    ],
    className: "guide-green",
    isHovered: ref(false),
  },
  {
    title: "学院管理",
    icon: "School",
    iconColor: "#E6A23C",
    path: "/college/collegeMajor",
    description: "管理学院相关信息",
    features: ["学院信息管理", "专业信息管理", "院系数据维护"],
    className: "guide-orange",
    isHovered: ref(false),
  },
  {
    title: "课程管理",
    icon: "List",
    iconColor: "#F56C6C",
    path: "/importSession",
    description: "管理课程相关信息",
    features: ["导入课程", "课程信息管理", "课程数据维护"],
    className: "guide-red",
    isHovered: ref(false),
  },
];

// 页面导航
const navigateTo = (path: string) => {
  console.log(path, "222222222222222");

  router.push(path);
};
</script>

<style scoped>
.guide-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.guide-banner {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  padding: 60px 20px;
  color: white;
  text-align: center;
  margin-bottom: 40px;
}

.banner-content {
  max-width: 1200px;
  margin: 0 auto;
}

.banner-content h1 {
  font-size: 42px;
  margin-bottom: 20px;
  font-weight: 600;
}

.banner-content .subtitle {
  font-size: 20px;
  opacity: 0.9;
}

.guide-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.section {
  margin-bottom: 60px;
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-header h2 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 15px;
}

.divider {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.divider .line {
  width: 50px;
  height: 2px;
  background-color: #dcdfe6;
}

.feature-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  height: 100%;
  transition: all 0.3s;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-icon {
  margin-bottom: 20px;
  display: inline-flex;
  padding: 20px;
  border-radius: 50%;
  background: #f5f7fa;
}

.feature-blue .feature-icon {
  background-color: #409eff15;
}
.feature-green .feature-icon {
  background-color: #67c23a15;
}
.feature-orange .feature-icon {
  background-color: #e6a23c15;
}

.guide-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 30px;
  transition: all 0.3s;
  display: flex;
  gap: 25px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.guide-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.guide-icon {
  padding: 20px;
  border-radius: 12px;
  height: fit-content;
}

.guide-info h3 {
  font-size: 20px;
  margin-bottom: 10px;
  color: #303133;
}

.guide-info p {
  color: #606266;
  margin-bottom: 15px;
  line-height: 1.6;
}

.guide-features {
  list-style: none;
  padding: 0;
  margin: 0 0 20px 0;
}

.guide-features li {
  position: relative;
  padding-left: 20px;
  margin-bottom: 8px;
  color: #909399;
}

.guide-features li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #67c23a;
}

.guide-btn {
  transition: all 0.3s;
}

/* 响应式布局优化 */
@media (max-width: 768px) {
  .guide-banner {
    padding: 40px 20px;
  }

  .banner-content h1 {
    font-size: 32px;
  }

  .banner-content .subtitle {
    font-size: 18px;
  }

  .guide-card {
    flex-direction: column;
    text-align: center;
  }

  .guide-icon {
    margin: 0 auto;
  }

  .guide-features li {
    text-align: left;
  }
}

/* 增加功能模块指南的上边距 */
.function-guide {
  margin-top: 80px; /* 增加上边距 */
}
</style>
