from tortoise import BaseDBAsyncClient

async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `student` (
            `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            `sno` VARCHAR(20) NOT NULL UNIQUE COMMENT '学号',
            `name` VARCHAR(50) NOT NULL COMMENT '姓名',
            `department` VARCHAR(50) NOT NULL COMMENT '学院',
            `major` VARCHAR(50) NOT NULL COMMENT '专业',
            `grade` VARCHAR(10) NOT NULL COMMENT '年级',
            `class_name` VARCHAR(50) NOT NULL COMMENT '班级',
            `joined_time` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
            `user_id` BIGINT NOT NULL UNIQUE COMMENT '关联用户ID',
            FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
        ) CHARACTER SET utf8mb4 COMMENT '学生信息表';
        
        CREATE INDEX `idx_student_sno` ON `student` (`sno`);
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `student`;
    """ 