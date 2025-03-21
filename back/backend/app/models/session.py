from tortoise import fields, Model

class Session(Model):
    id = fields.IntField(pk=True)
    course_id = fields.CharField(max_length=50, description="课程ID")
    course_name = fields.CharField(max_length=100, description="课程名称")
    credit = fields.CharField(max_length=10, description="学分")
    hours = fields.CharField(max_length=10, description="学时")
    nature = fields.CharField(max_length=50, description="课程性质")
    college = fields.CharField(max_length=50, description="所属学院")
    major = fields.CharField(max_length=50, description="所属专业")
    grade = fields.CharField(max_length=10, description="适用年级")
    
    class Meta:
        table = "sessions"
        table_description = "课程信息表"