from tortoise import BaseDBAsyncClient

async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `teacher` (
            `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            `department` VARCHAR(50) NOT NULL COMMENT '学院',
            `major` VARCHAR(50) NOT NULL COMMENT '专业',
            `title` VARCHAR(20) NOT NULL COMMENT '职称',
            `joined_time` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
            `user_id` BIGINT NOT NULL UNIQUE COMMENT '关联用户ID',
            FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
        ) CHARACTER SET utf8mb4 COMMENT '教师信息表';
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `teacher`;
    """ 