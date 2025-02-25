from typing import List
from tortoise.transactions import atomic
import json

from backend.app.dao.base import DaoBase
from backend.app.models.comprehensive_test import ComprehensiveTest
from backend.app.schemas.comprehensive_test import ComprehensiveTestBase

class ComprehensiveTestDao(DaoBase):
    """综合测评数据访问对象"""

    @atomic()
    async def save_tests(self, tests: List[ComprehensiveTestBase]):
        """批量保存综合测评"""
        try:
            success_count = 0
            for test in tests:
                test_dict = test.model_dump()
                print("处理综合测评:", json.dumps(test_dict, ensure_ascii=False))
                existing = await self.model.filter(sno=test.sno).first()
                if existing:
                    await self.model.filter(sno=test.sno).update(**test_dict)
                else:
                    await self.model.create(**test_dict)
                success_count += 1
            return success_count
        except Exception as e:
            print("DAO层错误:", str(e))
            raise

# 创建全局实例
comprehensive_test_dao = ComprehensiveTestDao(ComprehensiveTest) 