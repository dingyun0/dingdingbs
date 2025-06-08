from typing import List, Optional
from pydantic import BaseModel
from backend.app.schemas.base import SchemaBase

class ComprehensiveTestBase(SchemaBase):
    sno: str
    name: str
    department: str
    major: str
    grade: str
    # 计算机科学与技术
    程序设计基础: Optional[str] = None
    数据结构与算法: Optional[str] = None
    操作系统: Optional[str] = None
    数据库原理: Optional[str] = None
    计算机网络: Optional[str] = None
    软件工程: Optional[str] = None
    人工智能: Optional[str] = None
    计算机组成原理: Optional[str] = None
    Web开发技术: Optional[str] = None
    计算机图形学: Optional[str] = None
    心理学基础: Optional[str] = None
    

    # 网络工程
    创业与创新: Optional[str] = None
    网络程控: Optional[str] = None
    网络协议与架构: Optional[str] = None
    网络安全: Optional[str] = None
    无线网络技术: Optional[str] = None
    网络管理与监控: Optional[str] = None
    交换与路由技术: Optional[str] = None
    网络编程: Optional[str] = None
    互联网技术: Optional[str] = None
    数据中心网络: Optional[str] = None
    VoIP技术: Optional[str] = None

    # 历史学
    世界历史: Optional[str] = None
    中国历史: Optional[str] = None
    史学理论: Optional[str] = None
    考古学基础: Optional[str] = None
    文化史: Optional[str] = None
    近现代史: Optional[str] = None
    历史文献学: Optional[str] = None
    社会经济史: Optional[str] = None
    历史研究方法: Optional[str] = None
    历史与文化遗产保护: Optional[str] = None

    # 视觉传达设计
    设计基础: Optional[str] = None
    色彩理论: Optional[str] = None
    平面设计: Optional[str] = None
    排版设计: Optional[str] = None
    包装设计: Optional[str] = None
    广告设计: Optional[str] = None
    用户体验设计: Optional[str] = None
    设计软件应用: Optional[str] = None
    视觉设计历史: Optional[str] = None
    设计调研方法: Optional[str] = None
    艺术处理学: Optional[str] = None

    # 自动化
    控制理论基础: Optional[str] = None
    自动控制系统: Optional[str] = None
    传感器与执行器: Optional[str] = None
    嵌入式系统: Optional[str] = None
    PLC编程: Optional[str] = None
    过程控制: Optional[str] = None
    工业自动化: Optional[str] = None
    机器人学: Optional[str] = None
    信号与系统: Optional[str] = None
    控制系统设计: Optional[str] = None
    工程管理: Optional[str] = None
    项目管理: Optional[str] = None

    credit_gpa: float
    year_gpa: float
    comprehensive: float
    academic:float
    labor:float
    sports:float
    innovation:float
    zongce:float

    排名: int
    获奖情况: Optional[str] = None


class SaveComprehensiveTest(BaseModel):
    tests: List[ComprehensiveTestBase]