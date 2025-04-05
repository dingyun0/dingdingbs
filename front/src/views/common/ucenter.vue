<template>
  <div class="container">
    <div class="container-box">
      <el-card class="user-card">
        <el-tabs tab-position="left" v-model="activeName">
          <el-tab-pane name="label2" label="我的头像" class="user-tabpane">
            <div class="crop-wrap" v-if="activeName === 'label2'">
              <vueCropper
                ref="cropper"
                :img="imgSrc"
                :autoCrop="true"
                :centerBox="true"
                :full="true"
                :fixedBox="true"
                :canScale="true"
                :autoCropWidth="200"
                :autoCropHeight="200"
                mode="contain"
              >
              </vueCropper>
            </div>
            <div class="button-group">
              <el-button class="crop-demo-btn" type="primary">
                选择图片
                <input
                  class="crop-input"
                  type="file"
                  name="image"
                  accept="image/*"
                  @change="setImage"
                />
              </el-button>
              <el-button type="success" @click="saveAvatar" :loading="uploading"
                >上传并保存</el-button
              >
            </div>
            <div class="tips">
              <p>支持 jpg、png 格式，文件小于 2M</p>
              <p>建议尺寸 200x200 像素</p>
            </div>
          </el-tab-pane>
          <el-tab-pane name="label3" label="修改密码" class="user-tabpane">
            <el-form class="w500" label-position="top">
              <el-form-item label="旧密码：">
                <el-input type="password" v-model="form.old"></el-input>
              </el-form-item>
              <el-form-item label="新密码：">
                <el-input type="password" v-model="form.new"></el-input>
              </el-form-item>
              <el-form-item label="确认新密码：">
                <el-input type="password" v-model="form.new1"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="onSubmit">保存</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts" name="ucenter">
import { reactive, ref, onMounted } from "vue";
import { VueCropper } from "vue-cropper";
import "vue-cropper/dist/index.css";
import avatar from "@/assets/img/img.jpg";
import TabsComp from "../element/tabs.vue";
import { ElMessage } from "element-plus";
import { useUserStore } from "@/store/user";

const userStore = useUserStore();
const name = localStorage.getItem("vuems_name");
const form = reactive({
  new1: "",
  new: "",
  old: "",
});
const onSubmit = async () => {
  if (form.new !== form.new1) {
    ElMessage.error("两次输入的新密码不一致");
    return;
  }
  if (form.old === form.new) {
    ElMessage.error("新密码不能与旧密码相同");
    return;
  }
  try {
    const res = await fetch("/api/users/password/reset", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({
        old: form.old,
        new: form.new,
      }),
    }).then((res) => res.json());

    if (res.code === 200) {
      ElMessage.success("密码修改成功");
      // 清空表单
      form.old = "";
      form.new = "";
      form.new1 = "";
    } else {
      ElMessage.error(res.message || "密码修改失败");
    }
  } catch (error) {
    console.error("密码修改失败:", error);
    ElMessage.error("密码修改失败，请重试");
  }
};

const activeName = ref("label2");

const avatarImg = ref(avatar);
const imgSrc = ref(avatar);
const cropImg = ref("");
const cropper: any = ref();
const uploading = ref(false);

const setImage = (e: any) => {
  const file = e.target.files[0];
  if (!file) return;

  // 验证文件类型
  const isJpgOrPng = file.type === "image/jpeg" || file.type === "image/png";
  if (!isJpgOrPng) {
    ElMessage.error("只能上传 JPG/PNG 格式的图片！");
    return;
  }

  // 验证文件大小
  const isLt2M = file.size / 1024 / 1024 < 2;
  if (!isLt2M) {
    ElMessage.error("图片大小不能超过 2MB！");
    return;
  }

  const reader = new FileReader();
  reader.onload = (e: ProgressEvent<FileReader>) => {
    if (e.target?.result) {
      imgSrc.value = e.target.result as string;
    }
  };
  reader.readAsDataURL(file);
};

const cropImage = () => {
  cropImg.value = cropper.value?.getCroppedCanvas().toDataURL();
};

const saveAvatar = async () => {
  if (!cropper.value) {
    ElMessage.warning("请先选择图片");
    return;
  }

  try {
    uploading.value = true;
    // 获取裁剪后的图片数据
    const canvas = await cropper.value.getCropData();

    // 将 base64 转换为 Blob
    const base64Data = canvas.split(",")[1];
    const blob = await fetch(`data:image/png;base64,${base64Data}`).then(
      (res) => res.blob()
    );

    // 创建 FormData
    const formData = new FormData();
    formData.append("avatar", blob, "avatar.png");

    // 调用上传接口
    const response = await fetch("/api/user/upload-avatar", {
      method: "POST",
      body: formData,
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    }).then((res) => res.json());

    if (response.code === 200) {
      ElMessage.success("头像上传成功");
      // 更新头像显示
      imgSrc.value = response.data.url;
      avatarImg.value = response.data.url;
    } else {
      ElMessage.error(response.message || "上传失败");
    }
  } catch (error) {
    console.error("头像上传失败:", error);
    ElMessage.error("头像上传失败，请重试");
  } finally {
    uploading.value = false;
  }
};

onMounted(() => {
  // 如果用户已有头像，使用当前头像
  const currentAvatar = avatarImg.value;
  if (currentAvatar && currentAvatar !== avatar) {
    imgSrc.value = currentAvatar;
  }
});
</script>

<style scoped>
.container {
  padding: 20px;
}

.container-box {
  max-width: 1000px;
  margin: 0 auto;
}

.user-card {
  min-height: 500px;
}

.user-tabpane {
  padding: 20px;
}

.crop-wrap {
  width: 100%;
  height: 400px;
  margin-bottom: 20px;
  background-color: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.button-group {
  margin: 20px 0;
}

.crop-demo-btn {
  position: relative;
  margin-right: 10px;
}

.crop-input {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.tips {
  color: #909399;
  font-size: 14px;
  line-height: 1.5;
}

.tips p {
  margin: 5px 0;
}

.w500 {
  width: 500px;
}

.user-footer {
  display: flex;
  border-top: 1px solid rgba(83, 70, 134, 0.1);
}

.user-footer-item {
  padding: 20px 0;
  width: 33.3333333333%;
  text-align: center;
}

.user-footer > div + div {
  border-left: 1px solid rgba(83, 70, 134, 0.1);
}
</style>

<style>
.el-tabs.el-tabs--left {
  height: 100%;
}
</style>
