from tortoise import BaseDBAsyncClient

async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `announcements` (
            `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            `uuid` VARCHAR(36) NOT NULL UNIQUE,
            `title` VARCHAR(255) NOT NULL,
            `content` TEXT NOT NULL,
            `publish_date` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
            `update_date` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
            `publisher` VARCHAR(255) NOT NULL,
            `type` VARCHAR(50) NOT NULL,
            `status` VARCHAR(50) NOT NULL DEFAULT 'active',
            INDEX `idx_announcement_title_type` (`title`, `type`)
        ) CHARACTER SET utf8mb4;
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `announcements`;
    """ 