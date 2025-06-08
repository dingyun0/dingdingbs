from tortoise import fields, Model

class College(Model):
    id = fields.IntField(pk=True, description="ID")
    department = fields.CharField(max_length=100, description="学院名称")
    major = fields.CharField(max_length=100, description="专业名称")
    grade = fields.CharField(max_length=50, description="年级")
    department_code = fields.CharField(max_length=50, null=True, description="学院代码")
    major_code = fields.CharField(max_length=50, null=True, description="专业代码")
    grade_code = fields.CharField(max_length=50, null=True, description="年级代码")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
    
    class Meta:
        table = "college"
        table_description = "学院专业年级信息"