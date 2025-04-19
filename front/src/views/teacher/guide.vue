<template>
  <div class="guide-container">
    <!-- 顶部横幅 -->
    <div class="guide-banner">
      <div class="banner-content">
        <h1>智评奖学金管理系统</h1>
        <p class="subtitle">教师端操作指南</p>
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
                <el-button class="guide-btn" type="primary" text size="small">
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
import { useRouter } from "vue-router";
import { Star, Menu, ArrowRight } from "@element-plus/icons-vue";

const router = useRouter();

// 系统特点数据
const systemFeatures = [
  {
    icon: "Document",
    iconColor: "#409EFF",
    title: "成绩管理",
    description: "提供完整的成绩管理功能，支持成绩录入、查询和统计分析。",
    className: "feature-blue",
  },
  {
    icon: "Check",
    iconColor: "#67C23A",
    title: "审核管理",
    description: "支持学生活动申请和成绩疑问的审核处理。",
    className: "feature-green",
  },
  {
    icon: "DataLine",
    iconColor: "#E6A23C",
    title: "综测管理",
    description: "提供综合测评成绩的管理和评定功能。",
    className: "feature-orange",
  },
];

// 功能模块指南数据
const functionGuides = [
  {
    title: "成绩管理",
    icon: "Document",
    iconColor: "#409EFF",
    path: "/importSession",
    description: "管理学生成绩信息",
    features: [
      "成绩录入 - 支持单个和批量导入",
      "成绩查询 - 快速查看已录入成绩",
      "成绩统计 - 提供多维度分析",
    ],
    className: "guide-blue",
  },
  {
    title: "审核管理",
    icon: "Check",
    iconColor: "#67C23A",
    path: "/activity/reviewActivity",
    description: "处理学生申请和疑问",
    features: [
      "活动申请审核 - 审核学生活动申请",
      "成绩疑问处理 - 处理学生成绩疑问",
    ],
    className: "guide-green",
  },
  {
    title: "综测管理",
    icon: "DataLine",
    iconColor: "#E6A23C",
    path: "/exportComprehensive",
    description: "管理综合测评成绩",
    features: ["综测成绩录入", "综测成绩查询", "综测成绩评定"],
    className: "guide-orange",
  },
];

// 页面导航
const navigateTo = (path: string) => {
  router.push(path);
};
</script>

<style scoped>
/* 复用管理员指南的样式 */
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
