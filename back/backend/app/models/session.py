from tortoise import fields, Model

class Session(Model):
    id = fields.IntField(pk=True, description="ID")
    course_id = fields.CharField(max_length=50, unique=True, description="课程ID")
    course_name = fields.CharField(max_length=100, description="课程名")
    credit = fields.CharField(max_length=20, description="学分")
    hours = fields.CharField(max_length=20, description="学时")
    nature = fields.CharField(max_length=50, description="课程性质")
    department = fields.CharField(max_length=100, description="开课院系")

    class Meta:
        table = "sessions"
        table_description = "课程表" 