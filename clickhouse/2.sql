
-- Создание юзера-админа с sha256 паролем
create user freeskiez_admin identified with sha256_password by 'admin_pass';

-- Выдача прав юзеру
grant current grants on *.* to freeskiez_admin with grant option;
