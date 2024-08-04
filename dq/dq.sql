
drop table if exists report.kotov_t1;
create table default.dq_kotov_t1 engine MergeTree() order by dt_hour as
select toDate(dt_last) dt_date
    , count(shk_id) qty_shk
    , uniq(shk_id) uniq_shk_id
    , countIf(shk_id, shk_id < 1) qty_null_shk_id

    , count(wbsticker_id) qty_wbsticker_id
    , uniq(wbsticker_id) uniq_wbsticker_id
    , countIf(wbsticker_id, wbsticker_id < 1) qty_null_wbsticker_id

    , count(employee_id) qty_employee_id
    , uniq(employee_id) uniq_employee_id
    , countIf(employee_id, employee_id < 1) qty_null_employee_id

    , count(state_id) qty_state_id
    , uniq(state_id) uniq_state_id
    , countIf(state_id, state_id='') qty_none_state_id

    , count(place_cod) qty_place_cod
    , uniq(place_cod) uniq_place_cod
    , countIf(place_cod, place_cod< 1) qty_null_place_cod

    , count(wh_id) qty_wh_id
    , uniq(wh_id) uniq_wh_id
    , countIf(wh_id, wh_id< 1) qty_null_wh_id

    , count(tare_id) qty_tare_id
    , uniq(tare_id) uniq_tare_id
    , countIf(tare_id, tare_id< 1) qty_null_tare_id

    , count(employee_id_writeoff) qty_employee_id_writeoff
    , uniq(employee_id_writeoff) uniq_employee_id_writeoff
    , countIf(employee_id_writeoff, employee_id_writeoff< 1) qty_null_employee_id_writeoff

    , count(wh_id_writeoff) qty_wh_id_writeoff
    , uniq(wh_id_writeoff) uniq_wh_id_writeoff
    , countIf(wh_id_writeoff, wh_id_writeoff< 1) qty_null_wh_id_writeoff

    , countIf(lostreason_id, lostreason_id = 0) qty_none_lostreason_id
    , countIf(employee_name, employee_name = '') qty_none_employee_name
    , countIf(place_name, place_name = '') qty_none_place_name
    , countIf(wh_name, wh_name = '') qty_none_wh_name
    , countIf(employee_name_writeoff, employee_name_writeoff = '') qty_none_employee_name_writeoff
    , countIf(wh_name_writeoff, wh_name_writeoff = '') qty_none_wh_name_writeoff
from default.kotov_t20
where dt_date >= '2024-06-01'
    and dt_date < '2024-07-01' --датасет получился большой, при конфигурации чарта падает вкладка в браузере, добавил ограничение по дате и в чарт закинул не все поля)
group by dt_date;
