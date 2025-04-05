from backend.app.models.user import User
from typing import Optional

class UserDao:
    @staticmethod
    async def update_password(user_id: int, hashed_password: str) -> None:
        """
        更新用户密码
        :param user_id: 用户ID
        :param hashed_password: 哈希后的新密码
        """
        await User.filter(id=user_id).update(hashed_password=hashed_password)
        
    @staticmethod
    async def get_by_id(user_id: int) -> Optional[User]:
        """
        根据ID获取用户
        :param user_id: 用户ID
        :return: 用户对象，如果不存在则返回None
        """
        return await User.get_or_none(id=user_id) 