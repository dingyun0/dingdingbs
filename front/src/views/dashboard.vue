<template>
  <div class="dashboard">
    <!-- 顶部欢迎区域 -->
    <div class="welcome-section">
      <el-card shadow="hover" class="welcome-card">
        <div class="welcome-content">
          <h1>欢迎使用综合教务管理系统</h1>
          <p>高效、便捷的一站式教学管理平台</p>
          <div class="welcome-bg">
            <div class="circle circle1"></div>
            <div class="circle circle2"></div>
            <div class="circle circle3"></div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 核心功能展示 -->
    <div class="feature-section">
      <el-row :gutter="20">
        <el-col :span="6" v-for="(item, index) in features" :key="index">
          <el-card
            shadow="hover"
            class="feature-card"
            :class="'feature-' + (index + 1)"
          >
            <div class="feature-icon-wrapper" :class="'bg' + (index + 1)">
              <el-icon class="feature-icon">
                <component :is="item.icon" />
              </el-icon>
            </div>
            <div class="feature-content">
              <h3 :class="'color' + (index + 1)">{{ item.title }}</h3>
              <p>{{ item.desc }}</p>
            </div>
            <div class="feature-wave"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 系统介绍区域 -->
    <div class="info-section">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card shadow="hover" class="info-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">系统特点</span>
              </div>
            </template>
            <div class="info-list">
              <div
                class="info-item"
                v-for="(feature, idx) in systemFeatures"
                :key="idx"
                :style="{ animationDelay: idx * 0.2 + 's' }"
              >
                <el-icon class="info-icon"><Check /></el-icon>
                <span>{{ feature }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="hover" class="info-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">使用指南</span>
              </div>
            </template>
            <div class="guide-list">
              <div
                class="guide-item"
                v-for="(guide, idx) in guides"
                :key="idx"
                :style="{ animationDelay: idx * 0.2 + 's' }"
              >
                <div class="guide-step">
                  {{ String(idx + 1).padStart(2, "0") }}
                </div>
                <div class="guide-content">
                  <h3>{{ guide.title }}</h3>
                  <p>{{ guide.desc }}</p>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 底部区域 -->
    <div class="footer-section">
      <el-card shadow="hover" class="footer-card">
        <div class="footer-content">
          <h2>开始使用</h2>
          <p>选择左侧菜单中的功能模块，开始您的教务管理之旅</p>
          <p>如有问题，请联系系统管理员获取帮助</p>
          <div class="footer-decoration">
            <div class="deco-line"></div>
            <div class="deco-dot"></div>
            <div class="deco-line"></div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts" name="dashboard">
import {
  Document,
  Medal,
  Bell,
  Calendar,
  Check,
} from "@element-plus/icons-vue";

const features = [
  { icon: "Document", title: "成绩管理", desc: "便捷的成绩录入与查询" },
  { icon: "Medal", title: "综合测评", desc: "科学的学生评价体系" },
  { icon: "Bell", title: "通知公告", desc: "及时的信息发布平台" },
  { icon: "Calendar", title: "活动管理", desc: "丰富的校园活动系统" },
];

const systemFeatures = [
  "智能化的成绩管理，支持多维度分析",
  "完善的权限控制，确保数据安全",
  "灵活的活动管理，促进校园文化建设",
  "科学的综合测评，全面评估学生发展",
];

const guides = [
  { title: "账号管理", desc: "使用工号/学号登录，首次登录请修改密码" },
  { title: "权限分配", desc: "根据身份自动分配相应的系统权限" },
  { title: "功能使用", desc: "点击左侧菜单，开始使用相应功能" },
];
</script>

<style scoped>
.dashboard {
  padding: 24px;
  background: #f0f2f5;
  min-height: calc(100vh - 48px);
}

/* 欢迎区域样式 */
.welcome-section {
  margin-bottom: 24px;
}

.welcome-card {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  z-index: 100;
}

.welcome-content {
  position: relative;
  z-index: 100;
  text-align: center;
  padding: 48px 24px;
  background: linear-gradient(135deg, #1890ff 0%, #36cfc9 100%);
}

.welcome-content h1 {
  font-size: 32px;
  font-weight: 600;
  color: white;
  margin-bottom: 16px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.welcome-content p {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.9);
}

/* 浮动圆圈动画 */
.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.circle1 {
  width: 120px;
  height: 120px;
  top: -30px;
  left: 10%;
}

.circle2 {
  width: 160px;
  height: 160px;
  top: 20px;
  right: 15%;
  animation-delay: 2s;
}

.circle3 {
  width: 80px;
  height: 80px;
  bottom: -20px;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
  100% {
    transform: translateY(0) rotate(360deg);
  }
}

/* 功能卡片样式 */
.feature-section {
  margin-bottom: 24px;
}

.feature-card {
  position: relative;
  height: 180px;
  overflow: hidden;
  border-radius: 8px;
  transform: translateY(20px);
  opacity: 0;
  animation: slideUp 0.6s ease forwards;
}

.feature-icon-wrapper {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px 8px 0 0;
}

.feature-icon {
  font-size: 32px;
  color: white;
}

.feature-content {
  padding: 16px;
  text-align: center;
}

.feature-content h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
}

.feature-content p {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.feature-wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 200%;
  height: 6px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card:hover .feature-wave {
  transform: translateX(0);
}

/* 渐变背景色 */
.bg1 {
  background: linear-gradient(135deg, #1890ff 0%, #36cfc9 100%);
}
.bg2 {
  background: linear-gradient(135deg, #52c41a 0%, #87d068 100%);
}
.bg3 {
  background: linear-gradient(135deg, #722ed1 0%, #b37feb 100%);
}
.bg4 {
  background: linear-gradient(135deg, #faad14 0%, #ffd666 100%);
}

.color1 {
  color: #1890ff;
}
.color2 {
  color: #52c41a;
}
.color3 {
  color: #722ed1;
}
.color4 {
  color: #faad14;
}

/* 信息卡片样式 */
.info-section {
  margin-bottom: 24px;
}

.info-card {
  height: 100%;
  border-radius: 8px;
}

.card-header {
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.info-list {
  padding: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  transform: translateX(-20px);
  opacity: 0;
  animation: slideIn 0.6s ease forwards;
}

.info-icon {
  color: #52c41a;
  font-size: 20px;
  margin-right: 12px;
}

/* 使用指南样式 */
.guide-list {
  padding: 16px;
}

.guide-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  transform: translateX(20px);
  opacity: 0;
  animation: slideIn 0.6s ease forwards;
}

.guide-step {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1890ff 0%, #36cfc9 100%);
  color: white;
  text-align: center;
  line-height: 36px;
  font-weight: 600;
  margin-right: 16px;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.2);
}

.guide-content {
  flex: 1;
}

.guide-content h3 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.guide-content p {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

/* 底部区域样式 */
.footer-section {
  margin-bottom: 24px;
}

.footer-card {
  border-radius: 8px;
  transform: translateY(20px);
  opacity: 0;
  animation: slideUp 0.6s ease forwards 0.5s;
}

.footer-content {
  text-align: center;
  padding: 32px 24px;
}

.footer-content h2 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.footer-content p {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin-bottom: 8px;
}

.footer-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 24px;
}

.deco-line {
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, transparent, #1890ff, transparent);
}

.deco-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #1890ff;
  margin: 0 12px;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes slideUp {
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideIn {
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}

/* 卡片通用样式 */
.el-card {
  transition: all 0.3s;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
}

.el-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08) !important;
}

.feature-1 {
  animation-delay: 0.1s;
}
.feature-2 {
  animation-delay: 0.2s;
}
.feature-3 {
  animation-delay: 0.3s;
}
.feature-4 {
  animation-delay: 0.4s;
}
</style>
