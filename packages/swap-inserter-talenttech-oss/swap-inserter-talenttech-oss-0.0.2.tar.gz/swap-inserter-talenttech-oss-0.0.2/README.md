Библиотека для вставки в таблицы, используя промежуточную
========================================================


Типы СУБД для вставки:
-------------
* clickhouse
* vertica 


Аргументы :
-------------
1. script - код для вставки, тип: string
2. sql_credentials - sql-креды для вставки, тип: json
3. insert_table -  имя таблицы, в которую идет вставка, тип: string
4. add_args - аргументы для замены переменных в скрипте, тип: json


Usage
```sh
pip3 install swap-inserter-talenttech-oss
```

SQL CREDENTIALS:
-------------
```python
sql_credentials = {
            "vertica": {
                "database": <VERTICA_DATABASE>,
                "schema": <VERTICA_SCHEMA>,
                "staging_schema": <VERTICA_STAGING_SCHEMA>,
                "user": <VERTICA_WRITE_USER>,
                "host": <VERTICA_HOST>,
                "port": <VERTICA_PORT>,
                "password": <VERTICA_WRITE_PASSWORD>,
                "vertica_configs": {"host": <VERTICA_HOST>,
                                    "port": <VERTICA_PORT>,
                                    "backup_server_node": [<SERVER_NODE_1>, <SERVER_NODE_2>, <SERVER_NODE_3>},
            },
            "ch": {
                "database": <CH_DATABASE>,
                "user": <CH_WRITE_USER>,
                "host": <CH_HOST_A>,
                "port": <CH_PORT_TCP>,
                "password": <CH_WRITE_PASSWORD>,
                "alt_hosts": "{},{}:{}".format(
                    <CH_HOST_B>,
                    <CH_HOST_C>,
                    <CH_PORT_TCP>,
                ),
            },
        }
```      

ПРИМЕР ИСПОЛЬЗОВАНИЯ VERTICA:
-------------
```python
from inserter.vertica_swap_inserter import VerticaSwapInserter

script = "SELECT <FIELDS> FROM {schema}.{from_table}"
inserter = VerticaSwapInserter(
            script=script,
            sql_credentials=sql_credentials["vertica"],
            insert_table=<TABLE_INSERT>,
            add_args={
                "schema": sql_credentials["vertica"]["schema"],
                "from_table": <FROM_TABLE>
            }
        )
        inserter.run()
```  

ПРИМЕР ИСПОЛЬЗОВАНИЯ CH:
-------------
```python
from inserter.ch_swap_inserter import CHSwapInserter

script = "SELECT <FIELDS> FROM {schema}.{from_table}"
inserter = CHSwapInserter(
            script=script,
            sql_credentials=sql_credentials["ch"],
            insert_table=<TABLE_INSERT>,
            add_args={
                "database": sql_credential["ch"]["database"],
                "from_table": <FROM_TABLE>
            },
        )
        inserter.run()
```    

