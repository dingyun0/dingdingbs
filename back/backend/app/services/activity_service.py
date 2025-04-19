from datetime import datetime
from backend.app.dao.activity_dao import ActivityDAO
from backend.app.schemas.activity import ActivityApply, CreateActivity, UpdateActivity, ActivityInfo
from tortoise import timezone

class ActivityService:
    @staticmethod
    async def add_activity(activity: CreateActivity):
        """添加活动"""
        try:
            # 打印接收到的数据
            print("Received activity data:", activity)
            print("Activity type:", type(activity))
            
            # 调用DAO层创建活动
            result = await ActivityDAO.create(activity)
            return {"code": 200, "msg": "添加成功", "data": result}
        except Exception as e:
            print("Error details:", str(e))
            return {"code": 500, "msg": f"添加失败: {str(e)}", "data": None}

    @staticmethod
    async def update_activity(activity: UpdateActivity):
        """更新活动"""
        try:
            # 检查活动是否存在
            existing_activity = await ActivityDAO.get_by_id(activity.id)
            if not existing_activity:
                return {"code": 404, "msg": "活动不存在", "data": None}
            
            # 调用DAO层更新活动
            result = await ActivityDAO.update(activity)
            return {"code": 200, "msg": "更新成功", "data": result}
        except Exception as e:
            return {"code": 500, "msg": f"更新失败: {str(e)}", "data": None}

    @staticmethod
    async def delete_activity(activity_id: int):
        """删除活动"""
        try:
            # 检查活动是否存在
            existing_activity = await ActivityDAO.get_by_id(activity_id)
            if not existing_activity:
                return {"code": 404, "msg": "活动不存在", "data": None}
            
            # 调用DAO层删除活动
            await ActivityDAO.delete(activity_id)
            return {"code": 200, "msg": "删除成功", "data": None}
        except Exception as e:
            return {"code": 500, "msg": f"删除失败: {str(e)}", "data": None}

    @staticmethod
    async def get_activity_list():
        """获取活动列表"""
        try:
            # 调用DAO层获取活动列表
            activities = await ActivityDAO.get_all()
            total = await ActivityDAO.get_total()
            
            return {
                "code": 200,
                "msg": "获取成功",
                "data": {
                    "list": activities,
                    "total": total
                }
            }
        except Exception as e:
            return {"code": 500, "msg": f"获取失败: {str(e)}", "data": None}

    @staticmethod
    async def apply_activity(apply_data: ActivityApply):
        """申请活动"""
        try:
            # 检查活动是否存在
            if apply_data.activity_id > 0:
                activity = await ActivityDAO.get_by_id(apply_data.activity_id)
                if not activity:
                    return {"code": 404, "msg": "活动不存在", "data": None}
                
                # 检查活动是否已过期 - 使用timezone.now()替代datetime.now()
                if activity.deadline < timezone.now():
                    return {"code": 400, "msg": "活动已过截止日期", "data": None}
                
                # 检查名额是否已满
                if activity.quota <= 0:
                    return {"code": 400, "msg": "活动名额已满", "data": None}
                
                # 检查是否重复申请
                existing_apply = await ActivityDAO.get_student_apply(
                    apply_data.activity_id, 
                    apply_data.student_sno
                )
                if existing_apply:
                    return {"code": 400, "msg": "已经申请过该活动", "data": None}
            
            # 创建申请记录
            result = await ActivityDAO.create_apply(apply_data)
            
            # 如果是关联到现有活动，更新活动名额
            if apply_data.activity_id > 0:
                await ActivityDAO.update_quota(apply_data.activity_id)
            
            return {"code": 200, "msg": "申请成功", "data": result}
        except Exception as e:
            print("申请活动失败:", str(e))
            return {"code": 500, "msg": f"申请失败: {str(e)}", "data": None}
    
    @staticmethod
    async def get_review_activities(teacher_id: int):
        """获取教师需要审核的活动列表"""
        try:
            # 获取待审核的活动列表
            reviews = await ActivityDAO.get_review_activities(teacher_id)
            
            # 转换为列表格式
            review_list = []
            for review in reviews:
                review_list.append({
                    "id": review.id,
                    "activity_id": review.activity_id,
                    "activity_title": review.activity_title,
                    "student_sno": review.student_sno,
                    "teacher_id": review.teacher_id,
                    "status": review.status,
                    "credits": review.credits,
                    "activity_category": review.activity_category,
                    "apply_time": review.apply_time.isoformat(),
                    "review_time": review.review_time.isoformat() if review.review_time else None,
                    "review_comment": review.review_comment,
                    "proof_files": review.proof_files,
                    "comment": review.comment
                })
            
            return {
                "code": 200,
                "msg": "获取成功",
                "data": review_list
            }
        except Exception as e:
            print("获取审核列表失败:", str(e))
            return {"code": 500, "msg": f"获取失败: {str(e)}", "data": None}


    @staticmethod
    async def handle_review(review_id: int, review_comment: str, comment: str):
        """处理活动审核"""
        try:
            # 检查审核记录是否存在
            review = await ActivityDAO.get_review_by_id(review_id)
            if not review:
                return {"code": 404, "msg": "审核记录不存在", "data": None}
            
            print("当前审核状态:", review.review_comment)  # 添加调试信息
            
            # 检查是否已经审核过
            if review.review_comment != "审核中":
                return {"code": 400, "msg": "该申请已经审核过", "data": None}
            
            # 更新审核状态
            result = await ActivityDAO.update_review_status(review_id, review_comment, comment)
            
            return {
                "code": 200,
                "msg": "审核成功",
                "data": {
                    "id": result.id,
                    "review_comment": result.review_comment,
                    "comment": result.comment,
                    "review_time": result.review_time.isoformat() if result.review_time else None
                }
            }
        except Exception as e:
            print("审核活动失败:", str(e))
            return {"code": 500, "msg": f"审核失败: {str(e)}", "data": None}
        
    @staticmethod
    async def get_review_message(student_sno: str):
        """获取学生的活动审核情况"""
        try:
            # 获取学生的审核记录
            reviews = await ActivityDAO.get_review_message(student_sno)
            
            # 转换为列表格式
            review_list = []
            for review in reviews:
                review_list.append({
                    "id": review.id,
                    "activity_id": review.activity_id,
                    "activity_title": review.activity_title,
                    "student_sno": review.student_sno,
                    "teacher_id": review.teacher_id,
                    "status": review.status,
                    "apply_time": review.apply_time.isoformat(),
                    "review_time": review.review_time.isoformat() if review.review_time else None,
                    "comment": review.comment,
                    "proof_files": review.proof_files
                })
            
            return {
                "code": 200,
                "msg": "获取成功",
                "data": review_list
            }
        except Exception as e:
            print("获取审核消息失败:", str(e))
            return {"code": 500, "msg": f"获取失败: {str(e)}", "data": None}
        
    
    @staticmethod
    async def activity_scores(student_sno: str, activity_category: str = None):
        """
        获取学生的活动分数
        
        Args:
            student_sno: 学生学号
            activity_category: 活动类型（可选）
            
        Returns:
            活动分数列表
        """
        try:
            # 获取活动分数
            activities = await ActivityDAO.activity_scores(student_sno, activity_category)
            
            if not activities:
                return {
                    "code": 200,
                    "msg": "未找到活动记录",
                    "data": []
                }
            
            # 格式化返回数据
            result = []
            for activity in activities:
                result.append({
                    "id": activity["id"],
                    "activity_id": activity["activity_id"],
                    "activity_title": activity["activity_title"],
                    "activity_category": activity["activity_category"],
                    "credits": float(activity["credits"]) if activity["credits"] else 0
                })
            
            return {
                "code": 200,
                "msg": "获取成功",
                "data": result
            }
            
        except Exception as e:
            print("获取活动分数失败:", str(e))
            return {
                "code": 500,
                "msg": f"获取活动分数失败: {str(e)}",
                "data": None
            }