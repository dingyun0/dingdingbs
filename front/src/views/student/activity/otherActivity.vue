<template>
  <div class="container">
    <div class="header">
      <h2>其他活动加分申请</h2>
      <p>请填写活动信息并上传相关证明材料</p>
    </div>

    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="120px"
      class="application-form"
    >
      <el-form-item label="活动名称" prop="activityName">
        <el-input
          v-model="formData.activityName"
          placeholder="请输入活动名称"
        ></el-input>
      </el-form-item>

      <el-form-item label="活动类型" prop="activityType">
        <el-select
          v-model="formData.activityType"
          placeholder="请选择活动类型"
          style="width: 100%"
        >
          <el-option
            v-for="item in activityTypes"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="审核老师" prop="teacherId">
        <el-select
          v-model="formData.teacherId"
          placeholder="请选择审核老师"
          style="width: 100%"
          :loading="teachersLoading"
        >
          <el-option
            v-for="teacher in teachers"
            :key="teacher.id"
            :label="teacher.name"
            :value="teacher.id"
          ></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="申请学分" prop="credits">
        <el-input-number
          v-model="formData.credits"
          :min="0.5"
          :max="10"
          :step="0.5"
          :precision="1"
          style="width: 100%"
        ></el-input-number>
      </el-form-item>

      <el-form-item label="活动日期" prop="activityDate">
        <el-date-picker
          v-model="formData.activityDate"
          type="date"
          placeholder="选择活动日期"
          style="width: 100%"
        ></el-date-picker>
      </el-form-item>

      <el-form-item label="活动描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="4"
          placeholder="请简要描述活动内容及您的参与情况"
        ></el-input>
      </el-form-item>

      <el-form-item label="证明材料" prop="proofFiles">
        <el-upload
          class="upload-demo"
          action="#"
          :http-request="uploadFile"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :before-upload="beforeUpload"
          :file-list="fileList"
          multiple
          :limit="5"
          list-type="picture"
        >
          <el-button type="primary">点击上传</el-button>
          <template #tip>
            <div class="el-upload__tip">
              请上传活动证明材料，如证书、奖状、活动照片等（JPG/PNG格式，不超过5MB）
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm(formRef)"
          >提交申请</el-button
        >
        <el-button @click="resetForm(formRef)">重置</el-button>
      </el-form-item>
    </el-form>

    <el-dialog v-model="previewVisible" title="图片预览">
      <img :src="previewUrl" alt="Preview" style="width: 100%" />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import type {
  FormInstance,
  FormRules,
  UploadProps,
  UploadUserFile,
} from "element-plus";
import { ElMessage, ElMessageBox } from "element-plus";
import { useUserStore } from "@/store/user";
import { getTeacherNameReq } from "@/api/index";
import { applyActivityReq } from "@/api/activity";
import { getImageUrl } from "@/api/image";

// 表单引用
const formRef = ref<FormInstance>();

// 用户信息
const userStore = useUserStore();

// 活动类型选项
const activityTypes = ref([
  { label: "学业", value: "学业" },
  { label: "文体", value: "文体" },
  { label: "创新", value: "创新" },
  { label: "劳动", value: "劳动" },
]);

// 老师列表
const teachers = ref<Array<{ id: number; name: string }>>([]);
const teachersLoading = ref(false);

// 获取老师列表
const fetchTeachers = async () => {
  teachersLoading.value = true;
  try {
    const res = await getTeacherNameReq();
    if (res.data.code === 200) {
      teachers.value = res.data.data;
    } else {
      ElMessage.warning(res.data.msg || "获取老师列表失败");
    }
  } catch (error) {
    console.error("获取老师列表失败:", error);
    ElMessage.error("获取老师列表失败，请刷新页面重试");
  } finally {
    teachersLoading.value = false;
  }
};

// 表单数据
const formData = reactive({
  activityName: "",
  activityType: "",
  teacherId: null as number | null,
  credits: 1,
  activityDate: "",
  description: "",
  proofFiles: [] as string[],
});

// 表单验证规则
const rules = reactive<FormRules>({
  activityName: [
    { required: true, message: "请输入活动名称", trigger: "blur" },
    { min: 2, max: 50, message: "长度应为2到50个字符", trigger: "blur" },
  ],
  activityType: [
    { required: true, message: "请选择活动类型", trigger: "change" },
  ],
  teacherId: [{ required: true, message: "请选择审核老师", trigger: "change" }],
  credits: [{ required: true, message: "请输入申请学分", trigger: "blur" }],
  activityDate: [
    { required: true, message: "请选择活动日期", trigger: "change" },
  ],
  description: [
    { required: true, message: "请输入活动描述", trigger: "blur" },
    {
      min: 10,
      max: 500,
      message: "描述长度应为10到500个字符",
      trigger: "blur",
    },
  ],
  proofFiles: [
    { required: true, message: "请上传证明材料", trigger: "change" },
  ],
});

// 文件列表
const fileList = ref<UploadUserFile[]>([]);
const previewVisible = ref(false);
const previewUrl = ref("");

// 文件上传前的验证
const beforeUpload: UploadProps["beforeUpload"] = (file) => {
  const isJPG = file.type === "image/jpeg";
  const isPNG = file.type === "image/png";
  const isLt5M = file.size / 1024 / 1024 < 5;

  if (!isJPG && !isPNG) {
    ElMessage.error("上传图片只能是 JPG 或 PNG 格式!");
    return false;
  }
  if (!isLt5M) {
    ElMessage.error("上传图片大小不能超过 5MB!");
    return false;
  }
  return true;
};

// 自定义上传方法
const uploadFile = async (options: any) => {
  try {
    const uploadFormData = new FormData();
    uploadFormData.append("file", options.file);

    const response = await getImageUrl(uploadFormData);
    if (response.data.code === 200) {
      console.log("1111111111111111", response.data.data.url);

      formData.proofFiles.push(response.data.data.url);

      fileList.value.push({
        name: options.file.name,
        url: response.data.data.url,
      });

      options.onSuccess(response.data);
    } else {
      options.onError("上传失败");
      ElMessage.error(response.data.message || "上传失败");
    }
  } catch (error) {
    options.onError("上传出错");
    ElMessage.error("文件上传失败，请重试");
    console.error("Upload error:", error);
  }
};

// 处理文件预览
const handlePreview = (file: UploadUserFile) => {
  previewUrl.value = file.url || URL.createObjectURL(file.raw!);
  previewVisible.value = true;
};

// 处理文件移除
const handleRemove = (file: UploadUserFile, fileList: UploadUserFile[]) => {
  const index = formData.proofFiles.findIndex((url) => url === file.url);
  if (index !== -1) {
    formData.proofFiles.splice(index, 1);
  }
};

// 提交表单
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;

  await formEl.validate(async (valid) => {
    if (valid) {
      try {
        // 确认提交
        await ElMessageBox.confirm(
          "确认提交活动加分申请吗？提交后将无法修改。",
          "提交确认",
          {
            confirmButtonText: "确认提交",
            cancelButtonText: "取消",
            type: "warning",
          }
        );

        console.log(userStore.sno, "444444444444");

        // 准备提交数据，适配 ActivityReview 模型
        const submitData = {
          activity_id: 1, // 添加activity_id字段，设为0表示自定义活动
          activity_title: formData.activityName,
          activity_category: formData.activityType,
          teacher_id: formData.teacherId,
          credits: String(formData.credits), // 将数字转换为字符串
          student_sno: userStore.sno,
          proof_files: formData.proofFiles.join(","), // 将图片URL数组转换为逗号分隔的字符串
          comment: formData.description,
        };

        // 使用applyActivityReq API提交申请
        const response = await applyActivityReq(submitData);

        if (response.data.code === 200) {
          ElMessage.success("申请提交成功！");
          resetForm(formEl);
        } else {
          ElMessage.error(response.data.msg || "提交失败，请重试");
        }
      } catch (error: any) {
        if (error !== "cancel") {
          ElMessage.error("提交失败: " + (error.message || "未知错误"));
          console.error("Submit error:", error);
        }
      }
    } else {
      ElMessage.warning("请完善表单信息");
    }
  });
};

// 重置表单
const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.resetFields();
  fileList.value = [];
  formData.proofFiles = [];
};

// 页面加载时获取用户信息和老师列表
onMounted(() => {
  console.log(userStore.sno, "22222222222222");

  if (!userStore) {
    ElMessage.warning("请先登录");
    // 可以在这里添加重定向到登录页面的逻辑
  }

  // 获取老师列表
  fetchTeachers();
});
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  margin-bottom: 30px;
  text-align: center;

  h2 {
    font-size: 24px;
    color: #303133;
    margin-bottom: 10px;
  }

  p {
    color: #606266;
    font-size: 14px;
  }
}

.application-form {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-upload__tip {
  line-height: 1.5;
  color: #909399;
  font-size: 12px;
}
</style>
