import time
import psycopg2
import subprocess

# Step 1: Start Docker containers
print("Starting Docker containers...")
subprocess.run(["docker-compose", "up", "-d"], check=True)

# Step 2: Wait for databases to be ready
print("Waiting for databases to be ready...")
time.sleep(10)  # basic wait, could be replaced with actual health checks

def connect_db(port):
    return psycopg2.connect(
        host="localhost",
        port=port,
        database="customers",
        user="postgres",
        password="postgres"
    )

def setup_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)
        conn.commit()

def insert_rows(conn):
    with conn.cursor() as cur:
        cur.executemany("INSERT INTO items (name) VALUES (%s);", [(f"Item {i}",) for i in range(1, 101)])
        conn.commit()

def verify_sync(conn1, conn2):
    with conn1.cursor() as cur1, conn2.cursor() as cur2:
        cur1.execute("SELECT COUNT(*) FROM items;")
        cur2.execute("SELECT COUNT(*) FROM items;")
        count1 = cur1.fetchone()[0]
        count2 = cur2.fetchone()[0]
        assert count1 == count2 == 100, f"Sync failed: DB1={count1}, DB2={count2}"
        print("✅ Sync verified: 100 rows in both databases.")

try:
    conn1 = connect_db(5433)
    conn2 = connect_db(5434)

    setup_tables(conn1)

    print("Inserting rows into DB1...")
    insert_rows(conn1)

    print("Verifying sync...")
    verify_sync(conn1, conn2)

finally:
    print("Closing connections...")
    conn1.close()
    conn2.close()

    print("Tearing down containers...")
    subprocess.run(["docker-compose", "down"], check=True)

