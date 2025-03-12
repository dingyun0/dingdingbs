from tortoise import fields, Model

class Student(Model):
    """学生表"""
    id = fields.BigIntField(pk=True, index=True, description='主键id')
    sno = fields.CharField(max_length=20, unique=True, description="学号")
    name = fields.CharField(max_length=50, description="姓名")
    department = fields.CharField(max_length=50, description="学院")
    major = fields.CharField(max_length=50, description="专业") 
    grade = fields.CharField(max_length=10, description="年级")
    class_name = fields.CharField(max_length=50, description="班级")
    joined_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    user_id = fields.BigIntField(description="关联用户ID")  # 直接存储用户ID

    class Meta:
        table = "student"
        table_description = "学生信息表"

    def __str__(self):
        return (
            f"Student("
            f"id={self.id}, "
            f"sno='{self.sno}', "
            f"name='{self.name}', "
            f"department='{self.department}', "
            f"major='{self.major}', "
            f"grade='{self.grade}'"
            f")"
        ) 