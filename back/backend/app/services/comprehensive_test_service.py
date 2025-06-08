from backend.app.models.comprehensive_test import ComprehensiveTest
from backend.app.dao.comprehensive_test_dao import comprehensive_test_dao
from backend.app.schemas.comprehensive_test import SaveComprehensiveTest
from backend.app.common.exception.errors import CustomError
import logging
import json
from decimal import Decimal

class ComprehensiveTestService:
    @staticmethod
    async def save_tests(tests: SaveComprehensiveTest):
        try:
            print(f"Service层接收到 {len(tests.tests)} 条数据")
            count = await comprehensive_test_dao.save_tests(tests.tests)
            return {
                "code": 200,
                "message": "保存成功",
                "data": {
                    "total": len(tests.tests),
                    "success": count
                }
            }
        except Exception as e:
            logging.error(f"保存综合测评失败: {str(e)}", exc_info=True)
            raise CustomError(message=f"保存综合测评失败: {str(e)}")
    
    @staticmethod
    async def get_all_tests():
        try:
            tests = await ComprehensiveTest.all()
            return {
                "code": 200,
                "message": "获取成功",
                "data": [
                    {
                        "id": test.id,
                        "sno": test.sno,
                        "name": test.name,
                        "class_name": test.class_name,
                        "操作系统课程设计": test.操作系统课程设计,
                        "无线网络技术": test.无线网络技术,
                        "计算机网络课程设计": test.计算机网络课程设计,
                        "操作系统": test.操作系统,
                        "人工智能与网络技术学科前沿": test.人工智能与网络技术学科前沿,
                        "信息安全原理及应用": test.信息安全原理及应用,
                        "Linux操作系统": test.Linux操作系统,
                        "Java程序设计": test.Java程序设计,
                        "数据结构":test.数据结构,
                        "credit_gpa": float(test.credit_gpa),
                        "year_gpa": float(test.year_gpa),
                        "comprehensive": float(test.comprehensive)
                    } for test in tests
                ]
            }
        except Exception as e:
            logging.error(f"获取综合测评失败: {str(e)}", exc_info=True)
            raise CustomError(message=f"获取综合测评失败: {str(e)}")

    @staticmethod
    async def get_test_by_sno(sno: str):
        try:
            test = await ComprehensiveTest.filter(sno=sno).first()
            if not test:
                return {
                    "code": 404,
                    "message": "未找到该学生的综合测评信息",
                    "data": None
                }
            
            # 获取所有字段值
            test_dict = dict(test)
            
            # 过滤掉空值字段，保留所有有值的字段
            result_data = {
                key: (float(value) if isinstance(value, Decimal) else value)
                for key, value in test_dict.items()
                if value is not None
            }
            
            return {
                "code": 200,
                "message": "获取成功",
                "data": result_data
            }
        except Exception as e:
            logging.error(f"获取综合测评信息失败: {str(e)}", exc_info=True)
            raise CustomError(message=f"获取综合测评信息失败: {str(e)}") 