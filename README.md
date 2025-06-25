## Problem
•  Spins up two relational database instances using docker-compose. 

• Inserts 100 new rows into the first database. 

• Syncs the 100 new rows to the second database. 

• Verifies the sync. 

• Tears down the database instances.

## Solution

### Setup docker-compose primary and replica postgres in docker containers

* Bring up docker containers
`cd exercise_june_2025`
`./docker-compose up --build`

* Test connection

`psql -h localhost -p 5434 -U postgres -d customers`

* Verfify replication

```
customers=# SELECT * FROM pg_stat_wal_receiver;
-[ RECORD 1 ]---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
pid                   | 31
status                | streaming
receive_start_lsn     | 0/3000000
receive_start_tli     | 1
written_lsn           | 0/303DDD8
flushed_lsn           | 0/303DDD8
received_tli          | 1
last_msg_send_time    | 2025-06-25 13:32:53.955363+00
last_msg_receipt_time | 2025-06-25 13:32:53.955458+00
latest_end_lsn        | 0/303DDD8
latest_end_time       | 2025-06-25 13:32:53.955363+00
slot_name             |
sender_host           | pg-primary
sender_port           | 5432
conninfo              | user=replicator password=******** channel_binding=prefer dbname=replication host=pg-primary port=5432 fallback_application_name=walreceiver sslmode=prefer sslnegotiation=postgres sslcompression=0 sslcertmode=allow sslsni=1 ssl_min_protocol_version=TLSv1.2 gssencmode=prefer krbsrvname=postgres gssdelegation=0 target_session_attrs=any load_balance_hosts=disable
```

### Destroy/Cleanup Docker containers
`./docker-cleanup.sh`


# Run full solution application

The below script will perform following operations
  + Spins up two relational database instances using docker-compose. 
  + Inserts 100 new rows into items table in the first database. 
  + Syncs the 100 new rows to the second/replica database using pg native streaming replication . 
  + Verifies the sync. 
  + Tears down the database instances.

` pip install psycopg2-binary `

` python sync_script.py `


### Assumptions

  + docker and docker-compose is installed
  + python3 is already installed
