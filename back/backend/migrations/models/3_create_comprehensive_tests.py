from tortoise import BaseDBAsyncClient

async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `comprehensive_tests` (
            `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            `sno` VARCHAR(50) NOT NULL UNIQUE COMMENT '学号',
            `name` VARCHAR(50) NOT NULL COMMENT '姓名',
            `class_name` VARCHAR(50) NOT NULL COMMENT '班级',
            `操作系统课程设计成绩` VARCHAR(50) NULL COMMENT '操作系统课程设计成绩',
            `无线网络技术成绩` VARCHAR(50) NULL COMMENT '无线网络技术成绩',
            `计算机网络课程设计` VARCHAR(50) NULL COMMENT '计算机网络课程设计',
            `操作系统` VARCHAR(50) NULL COMMENT '操作系统',
            `人工智能与网络技术学科前沿` VARCHAR(50) NULL COMMENT '人工智能与网络技术学科前沿',
            `信息安全原理及应用` VARCHAR(50) NULL COMMENT '信息安全原理及应用',
            `Linux操作系统` VARCHAR(50) NULL COMMENT 'Linux操作系统',
            `Java程序设计` VARCHAR(50) NULL COMMENT 'Java程序设计',
            `credit_gpa` DECIMAL(10,2) NOT NULL COMMENT '学分绩点',
            `year_gpa` DECIMAL(10,2) NOT NULL COMMENT '学年绩点',
            `comprehensive_score` DECIMAL(10,2) NOT NULL COMMENT '综测成绩'
        ) CHARACTER SET utf8mb4 COMMENT '综合测评表';
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `comprehensive_tests`;
    """