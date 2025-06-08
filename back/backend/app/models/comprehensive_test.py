from tortoise import fields, Model

class ComprehensiveTest(Model):
    id = fields.IntField(pk=True, description="ID")
    sno = fields.CharField(max_length=50, unique=True, description="学号")
    name = fields.CharField(max_length=50, description="姓名")
    department = fields.CharField(max_length=50, description="学院")
    major = fields.CharField(max_length=50, description="专业")
    grade = fields.CharField(max_length=50, description="年级")
   # 计算机科学与技术
    程序设计基础 = fields.CharField(max_length=50, null=True, description="程序设计基础")
    数据结构与算法 = fields.CharField(max_length=50, null=True, description="数据结构与算法")
    操作系统 = fields.CharField(max_length=50, null=True, description="操作系统")
    数据库原理 = fields.CharField(max_length=50, null=True, description="数据库原理")
    计算机网络 = fields.CharField(max_length=50, null=True, description="计算机网络")
    软件工程 = fields.CharField(max_length=50, null=True, description="软件工程")
    人工智能 = fields.CharField(max_length=50, null=True, description="人工智能")
    计算机组成原理 = fields.CharField(max_length=50, null=True, description="计算机组成原理")
    Web开发技术 = fields.CharField(max_length=50, null=True, description="Web开发技术")
    计算机图形学 = fields.CharField(max_length=50, null=True, description="计算机图形学")
    心理学基础 = fields.CharField(max_length=50, null=True, description="心理学基础")
    # 网络工程
    创业与创新 = fields.CharField(max_length=50, null=True, description="创业与创新")
    网络程控 = fields.CharField(max_length=50, null=True, description="网络程控")
    网络协议与架构 = fields.CharField(max_length=50, null=True, description="网络协议与架构")
    网络安全 = fields.CharField(max_length=50, null=True, description="网络安全")
    无线网络技术 = fields.CharField(max_length=50, null=True, description="无线网络技术")
    网络管理与监控 = fields.CharField(max_length=50, null=True, description="网络管理与监控")
    交换与路由技术 = fields.CharField(max_length=50, null=True, description="交换与路由技术")
    网络编程 = fields.CharField(max_length=50, null=True, description="网络编程")
    互联网技术 = fields.CharField(max_length=50, null=True, description="互联网技术")
    数据中心网络 = fields.CharField(max_length=50, null=True, description="数据中心网络")
    VoIP技术 = fields.CharField(max_length=50, null=True, description="VoIP技术")
    # 历史学
    世界历史 = fields.CharField(max_length=50, null=True, description="世界历史")
    中国历史 = fields.CharField(max_length=50, null=True, description="中国历史")
    史学理论 = fields.CharField(max_length=50, null=True, description="史学理论")
    考古学基础 = fields.CharField(max_length=50, null=True, description="考古学基础")
    文化史 = fields.CharField(max_length=50, null=True, description="文化史")
    近现代史 = fields.CharField(max_length=50, null=True, description="近现代史")
    历史文献学 = fields.CharField(max_length=50, null=True, description="历史文献学")
    社会经济史 = fields.CharField(max_length=50, null=True, description="社会经济史")
    历史研究方法 = fields.CharField(max_length=50, null=True, description="历史研究方法")
    历史与文化遗产保护 = fields.CharField(max_length=50, null=True, description="历史与文化遗产保护")

    # 视觉传达设计
    设计基础 = fields.CharField(max_length=50, null=True, description="设计基础")
    色彩理论 = fields.CharField(max_length=50, null=True, description="色彩理论")
    平面设计 = fields.CharField(max_length=50, null=True, description="平面设计")
    排版设计 = fields.CharField(max_length=50, null=True, description="排版设计")
    包装设计 = fields.CharField(max_length=50, null=True, description="包装设计")
    广告设计 = fields.CharField(max_length=50, null=True, description="广告设计")
    用户体验设计 = fields.CharField(max_length=50, null=True, description="用户体验设计")
    设计软件应用 = fields.CharField(max_length=50, null=True, description="设计软件应用")
    视觉设计历史 = fields.CharField(max_length=50, null=True, description="视觉设计历史")
    设计调研方法 = fields.CharField(max_length=50, null=True, description="设计调研方法")
    艺术处理学 = fields.CharField(max_length=50, null=True, description="艺术处理学")
    # 自动化
    控制理论基础 = fields.CharField(max_length=50, null=True, description="控制理论基础")
    自动控制系统 = fields.CharField(max_length=50, null=True, description="自动控制系统")
    传感器与执行器 = fields.CharField(max_length=50, null=True, description="传感器与执行器")
    嵌入式系统 = fields.CharField(max_length=50, null=True, description="嵌入式系统")
    PLC编程 = fields.CharField(max_length=50, null=True, description="PLC编程")
    过程控制 = fields.CharField(max_length=50, null=True, description="过程控制")
    工业自动化 = fields.CharField(max_length=50, null=True, description="工业自动化")
    机器人学 = fields.CharField(max_length=50, null=True, description="机器人学")
    信号与系统 = fields.CharField(max_length=50, null=True, description="信号与系统")
    控制系统设计 = fields.CharField(max_length=50, null=True, description="控制系统设计")
    工程管理 = fields.CharField(max_length=50, null=True, description="工程管理")
    项目管理 = fields.CharField(max_length=50, null=True, description="项目管理")

    credit_gpa = fields.DecimalField(max_digits=10, decimal_places=2, description="学分绩点")
    year_gpa = fields.DecimalField(max_digits=10, decimal_places=2, description="学年绩点")
    comprehensive = fields.DecimalField(max_digits=10, decimal_places=2, description="学业分")

    academic = fields.DecimalField(max_digits=10, decimal_places=2, description="学业分加分")
    labor = fields.DecimalField(max_digits=10, decimal_places=2, description="劳动分加分")
    sports = fields.DecimalField(max_digits=10, decimal_places=2, description="文体分加分")
    innovation = fields.DecimalField(max_digits=10, decimal_places=2, description="思想分加分")

    zongce = fields.DecimalField(max_digits=10, decimal_places=2, description="综测")
    
    排名 = fields.IntField(max_digits=10, decimal_places=0, description="排名")
    获奖情况=fields.CharField(max_length=50, description="获奖情况")
    
    class Meta:
        table = "comprehensive_tests"
        table_description = "学业分计算"