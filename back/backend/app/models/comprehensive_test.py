from tortoise import fields, Model

class ComprehensiveTest(Model):
    id = fields.IntField(pk=True, description="ID")
    sno = fields.CharField(max_length=50, unique=True, description="学号")
    name = fields.CharField(max_length=50, description="姓名")
    class_name = fields.CharField(max_length=50, description="班级")
    操作系统课程设计 = fields.CharField(max_length=50, null=True, description="操作系统课程设计成绩")
    无线网络技术 = fields.CharField(max_length=50, null=True, description="无线网络技术成绩")
    计算机网络课程设计 = fields.CharField(max_length=50, null=True, description="计算机网络课程设计")
    操作系统 = fields.CharField(max_length=50, null=True, description="操作系统")
    人工智能与网络技术学科前沿 = fields.CharField(max_length=50, null=True, description="人工智能与网络技术学科前沿")
    信息安全原理及应用 = fields.CharField(max_length=50, null=True, description="信息安全原理及应用")
    Linux操作系统 = fields.CharField(max_length=50, null=True, description="Linux操作系统")
    Java程序设计 = fields.CharField(max_length=50, null=True, description="Java程序设计")
    数据结构=fields.CharField(max_length=50, null=True, description="数据结构")
    人工智能基础=fields.CharField(max_length=50,null=True,description='人工智能基础')
    credit_gpa = fields.DecimalField(max_digits=10, decimal_places=2, description="学分绩点")
    year_gpa = fields.DecimalField(max_digits=10, decimal_places=2, description="学年绩点")
    comprehensive = fields.DecimalField(max_digits=10, decimal_places=2, description="学业分")
    academic = fields.DecimalField(max_digits=10, decimal_places=2, description="学业分加分")
    labor = fields.DecimalField(max_digits=10, decimal_places=2, description="劳动分加分")
    sports = fields.DecimalField(max_digits=10, decimal_places=2, description="文体分加分")
    innovation = fields.DecimalField(max_digits=10, decimal_places=2, description="思想分加分")
    zongce = fields.DecimalField(max_digits=10, decimal_places=2, description="综测")
    
    
    class Meta:
        table = "comprehensive_tests"
        table_description = "学业分计算"