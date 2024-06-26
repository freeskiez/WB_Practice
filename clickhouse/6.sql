-- Создание матвью
create materialized view stage.shkonplace_current to current.shkonplace as
select shk_id, dt, state_id
from stage.shkonplace_log;

show view stage.shkonplace_current;