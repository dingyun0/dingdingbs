from tortoise import fields, Model

class Teacher(Model):
    """教师表"""
    id = fields.BigIntField(pk=True, index=True, description='主键id')
    name=fields.CharField(max_length=50,description="姓名")
    department = fields.CharField(max_length=50, description="学院")
    major = fields.CharField(max_length=50, description="专业") 
    title = fields.CharField(max_length=20, description="职称")  # 新增职称字段
    joined_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    user_id = fields.BigIntField(unique=True, description="关联用户ID")  # 关联用户表

    class Meta:
        table = "teacher"
        table_description = "教师信息表"

    def __str__(self):
        return (
            f"Teacher("
            f"id={self.id}, "
            f"department='{self.department}', "
            f"major='{self.major}', "
            f"title='{self.title}'"
            f")"
        ) 