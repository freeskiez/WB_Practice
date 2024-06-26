
-- Создание ридонли роли
create role readonly_role;
grant select on *.* to readonly_role;

-- Создание юзера с ридонли правами
create user readonly_user identified with sha256_password by 'readonly_pass';
grant readonly_role to readonly_user;



-- Создание стейдж роли
create role stage_role;
grant create on stage.* to stage_role;
grant insert on stage.* to stage_role;

-- Создание юзера с правами на создание и вставку только в stage бд
create user stage_user identified with sha256_password by 'stage_pass';
grant stage_role to stage_user;