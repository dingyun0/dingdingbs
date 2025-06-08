from tortoise import BaseDBAsyncClient

async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `sessions` (
            `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            `course_id` VARCHAR(50) NOT NULL UNIQUE COMMENT '课程ID',
            `course_name` VARCHAR(100) NOT NULL COMMENT '课程名',
            `credit` VARCHAR(20) NOT NULL COMMENT '学分',
            `hours` VARCHAR(20) NOT NULL COMMENT '学时',
            `nature` VARCHAR(50) NOT NULL COMMENT '课程性质',
            `department` VARCHAR(100) NOT NULL COMMENT '开课院系'
        ) CHARACTER SET utf8mb4 COMMENT '课程表';
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `sessions`;
    """ 