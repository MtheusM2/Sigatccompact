SET @schema := DATABASE();

SET @sql := (
    SELECT IF(
        EXISTS(
            SELECT 1
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = @schema
              AND TABLE_NAME = 'ativos'
              AND COLUMN_NAME = 'email_responsavel'
        ),
        'SELECT 1',
        'ALTER TABLE ativos ADD COLUMN email_responsavel VARCHAR(255) NULL AFTER modelo'
    )
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql := (
    SELECT IF(
        EXISTS(
            SELECT 1
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE TABLE_SCHEMA = @schema
              AND TABLE_NAME = 'ativos'
              AND INDEX_NAME = 'idx_ativos_email_responsavel'
        ),
        'SELECT 1',
        'ALTER TABLE ativos ADD KEY idx_ativos_email_responsavel (email_responsavel)'
    )
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;