SET @schema := DATABASE();

SET @sql := (
    SELECT IF(
        EXISTS(
            SELECT 1
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = @schema
              AND TABLE_NAME = 'usuarios'
              AND COLUMN_NAME = 'perfil'
        ),
        'SELECT 1',
        'ALTER TABLE usuarios ADD COLUMN perfil VARCHAR(20) NOT NULL DEFAULT ''USUARIO'' AFTER senha_hash'
    )
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql := (
    SELECT IF(
        EXISTS(
            SELECT 1
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = @schema
              AND TABLE_NAME = 'usuarios'
              AND COLUMN_NAME = 'ativo'
        ),
        'SELECT 1',
        'ALTER TABLE usuarios ADD COLUMN ativo TINYINT(1) NOT NULL DEFAULT 1 AFTER perfil'
    )
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql := (
    SELECT IF(
        EXISTS(
            SELECT 1
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = @schema
              AND TABLE_NAME = 'usuarios'
              AND COLUMN_NAME = 'ultimo_login'
        ),
        'SELECT 1',
        'ALTER TABLE usuarios ADD COLUMN ultimo_login DATETIME NULL AFTER ativo'
    )
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql := (
    SELECT IF(
        EXISTS(
            SELECT 1
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = @schema
              AND TABLE_NAME = 'usuarios'
              AND COLUMN_NAME = 'bloqueado_ate'
        ),
        'SELECT 1',
        'ALTER TABLE usuarios ADD COLUMN bloqueado_ate DATETIME NULL AFTER ultimo_login'
    )
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql := (
    SELECT IF(
        EXISTS(
            SELECT 1
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = @schema
              AND TABLE_NAME = 'usuarios'
              AND COLUMN_NAME = 'atualizado_em'
        ),
        'ALTER TABLE usuarios MODIFY COLUMN atualizado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
        'ALTER TABLE usuarios ADD COLUMN atualizado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    )
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;