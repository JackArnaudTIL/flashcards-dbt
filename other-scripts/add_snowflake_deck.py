import json

with open('frontend/cards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def c(q, a, group, difficulty, category, module, cert=None, requires_code=False):
    card = {"q": q, "a": a, "group": group, "difficulty": difficulty,
            "category": category, "module": module}
    if cert:
        card["certification"] = cert
    if requires_code:
        card["group"] = group if isinstance(group, list) else [group]
        card["requires_code"] = True
        card["explanation"] = ""
    return card

cards = []

# ════════════════════════════════════════════════════════
# MODULE 1 – SNOWFLAKE 101
# ════════════════════════════════════════════════════════
M = "Snowflake 101"

# Core Concepts
cards += [
c("What is Snowflake?",
  "A cloud-native SQL data platform delivered entirely as a service. It runs on AWS, Azure, and GCP and separates storage, compute, and cloud services into three independent layers so each can scale on its own.",
  "Core Concepts","easy","Core Concepts",M),

c("What problem does Snowflake solve compared with traditional data warehouses?",
  "Traditional warehouses tightly couple storage and compute, so you must over-provision both even when only one is the bottleneck. Snowflake separates them: you scale storage by adding data and scale compute by resizing or adding virtual warehouses, independently and on demand.",
  "Core Concepts","easy","Core Concepts",M),

c("What are the three layers of Snowflake's architecture?",
  "1. Cloud Services Layer — authentication, metadata, query optimisation, transaction management. 2. Query Processing Layer — virtual warehouses (MPP compute clusters) that execute queries. 3. Database Storage Layer — compressed, columnar, micro-partitioned data stored on cloud object storage (S3/GCS/Azure Blob).",
  "Core Concepts","easy","Core Concepts",M),

c("What cloud providers does Snowflake support?",
  "Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP). Your Snowflake account is deployed to a specific cloud/region, and data stays within that region unless you explicitly configure replication.",
  "Core Concepts","easy","Core Concepts",M),

c("What are the four Snowflake account editions?",
  "Standard — core features. Enterprise — adds multi-cluster warehouses, 90-day Time Travel, column-level security, materialized views. Business Critical — adds HIPAA/PCI/SOC 2 compliance, enhanced encryption, private connectivity. Virtual Private Snowflake (VPS) — fully isolated, dedicated infrastructure.",
  "Core Concepts","medium","Core Concepts",M),
]

# Architecture
cards += [
c("What is a Snowflake Virtual Warehouse?",
  "An independently scalable MPP (Massively Parallel Processing) compute cluster. It has its own CPU, memory, and local SSD cache. Queries are submitted to a warehouse, which runs them against data in the storage layer.",
  "Architecture","easy","Architecture",M),

c("What is auto-suspend on a Virtual Warehouse?",
  "After a configurable idle period (default 10 minutes, minimum 1 minute on some editions), the warehouse automatically suspends — stopping all credit consumption. The local disk cache is lost on suspension.",
  "Architecture","easy","Architecture",M),

c("What is auto-resume on a Virtual Warehouse?",
  "When a query is submitted to a suspended warehouse, it automatically resumes before running the query. The delay is typically a few seconds. Auto-resume is enabled by default.",
  "Architecture","easy","Architecture",M),

c("What is a Snowflake credit?",
  "The billing unit for Snowflake compute. Virtual warehouses consume credits while running; the rate depends on size (XS = 1 credit/hour, S = 2, M = 4, L = 8, XL = 16, 2XL = 32, and so on, doubling each tier). There is a 60-second minimum charge per start.",
  "Architecture","medium","Architecture",M),

c("What is the minimum billing period when a Snowflake warehouse starts?",
  "60 seconds. If a query finishes in 10 seconds, you are still charged for a full 60 seconds. After the first minute, billing is per-second. This makes auto-suspend important for avoiding unnecessary charges on short-lived queries.",
  "Architecture","medium","Architecture",M),

c("What is multi-cluster warehousing in Snowflake?",
  "An Enterprise-edition feature that lets a single virtual warehouse scale out by spinning up additional clusters when concurrency demand exceeds a single cluster's capacity. Clusters are added automatically and removed when load drops.",
  "Architecture","medium","Architecture",M),

c("What is the difference between scaling UP and scaling OUT in Snowflake?",
  "Scaling up = increasing the warehouse size (e.g., M → L) to give complex, single queries more CPU/memory. Scaling out = multi-cluster (more clusters) to handle more concurrent users without slowing individual queries.",
  "Architecture","medium","Architecture",M),

c("What are the three types of caching in Snowflake?",
  "1. Metadata Cache (Cloud Services Layer) — stores table stats, partition metadata; can answer some COUNT/MIN/MAX queries without a warehouse. 2. Result Cache — stores query results for 24 hours; exact same SQL against unchanged data reuses the result for free. 3. Local Disk Cache (per warehouse) — caches raw column data read from storage; shared across queries on the same warehouse.",
  "Architecture","medium","Architecture",M),

c("What is a micro-partition in Snowflake?",
  "The fundamental storage unit. Data is automatically divided into immutable, compressed, columnar files of 50–500 MB (uncompressed). Each micro-partition stores min/max statistics per column, enabling Snowflake to prune (skip) partitions that can't satisfy a query's predicates.",
  "Architecture","medium","Architecture",M),
]

# Tables and Objects
cards += [
c("What are the four table types in Snowflake?",
  "Permanent (default) — full Time Travel + 7-day Fail-Safe. Temporary — session-scoped, auto-dropped; 0 or 1-day Time Travel, no Fail-Safe. Transient — survives sessions but 0-day Fail-Safe; lower storage cost. External — references files in cloud storage; read-only, no Time Travel.",
  "Tables & Objects","easy","Tables & Objects",M),

c("What is a Snowflake Temporary table?",
  "A table that exists only for the current session. It is automatically dropped when the session ends. Temporary tables are invisible to other sessions and have 0 or 1-day Time Travel but no Fail-Safe period.",
  "Tables & Objects","easy","Tables & Objects",M),

c("What is a Snowflake Transient table and when would you use one?",
  "A table with no Fail-Safe (0-day) and 0–1 day Time Travel. Use it for staging or intermediary data that doesn't need long-term protection — it reduces storage costs compared with permanent tables.",
  "Tables & Objects","medium","Tables & Objects",M),

c("What is a Snowflake External Table?",
  "A read-only table that queries files stored in an external stage (S3/GCS/Azure Blob) without ingesting the data into Snowflake. Useful for querying data-lake files in-place. No Time Travel or Fail-Safe.",
  "Tables & Objects","medium","Tables & Objects",M),

c("What is a Snowflake Materialized View?",
  "A pre-computed view whose results are stored physically and refreshed automatically by Snowflake when the underlying base table changes. Faster to query than a standard view because data is pre-aggregated, but incurs storage and maintenance compute cost.",
  "Tables & Objects","medium","Tables & Objects",M),

c("What is a Snowflake Sequence?",
  "An object that generates unique, monotonically increasing integer values. Used to create surrogate keys: NEXTVAL for the sequence is called in INSERT statements. Note: values are guaranteed unique but NOT guaranteed to be gap-free.",
  "Tables & Objects","medium","Tables & Objects",M),

c("What is a Snowflake Stage?",
  "A named location that holds data files before loading (or after unloading). Internal stages are managed by Snowflake (user stage @~, table stage @%table, named stage). External stages point to cloud object storage (S3, GCS, Azure Blob).",
  "Tables & Objects","easy","Tables & Objects",M),
]

# Time Travel / Fail-Safe / Clone
cards += [
c("What is Snowflake Time Travel?",
  "A feature that lets you query, clone, or restore data from a past point in time — using AT(TIMESTAMP), AT(OFFSET), or AT(STATEMENT). Retention is 0–1 day for Standard edition and 0–90 days for Enterprise edition.",
  "Time Travel & Cloning","easy","Time Travel & Cloning",M),

c("What is Snowflake Fail-Safe?",
  "A 7-day non-configurable recovery window that begins after the Time Travel retention period expires. It is a Snowflake-managed disaster recovery mechanism — users cannot query or restore data themselves; only Snowflake support can recover it.",
  "Time Travel & Cloning","medium","Time Travel & Cloning",M),

c("What is Zero-Copy Cloning?",
  "Instantly creates a copy of a table, schema, or database by pointing to the same underlying micro-partitions — no data is physically duplicated at clone time. The clone and original diverge as changes are made, sharing only unchanged micro-partitions.",
  "Time Travel & Cloning","easy","Time Travel & Cloning",M),

c("Can you clone a table at a historical point in time?",
  "Yes. CREATE TABLE my_clone CLONE my_table AT(TIMESTAMP => '2024-01-01 00:00:00'::TIMESTAMP_LTZ); The clone reflects the state of the table at that past moment (within the Time Travel window).",
  "Time Travel & Cloning","medium","Time Travel & Cloning",M),
]

# Security Basics
cards += [
c("What is RBAC in Snowflake?",
  "Role-Based Access Control — privileges are granted to roles (not directly to users), and roles are granted to users. A user can hold multiple roles and switches between them. All objects are owned by a role.",
  "Security","easy","Security",M),

c("What are the five built-in Snowflake system roles?",
  "ACCOUNTADMIN — top-level, full control. SYSADMIN — creates and manages warehouses/databases/objects. SECURITYADMIN — manages users, roles, and grants. USERADMIN — creates and manages users and roles. PUBLIC — automatically granted to every user; minimal privileges.",
  "Security","easy","Security",M),

c("What does the ACCOUNTADMIN role do?",
  "The most powerful role. It can manage all account-level settings, billing, resource monitors, and can GRANT any privilege. Should be granted to as few users as possible. Snowflake best practice: never use it for day-to-day work.",
  "Security","easy","Security",M),

c("What is a Snowflake Resource Monitor?",
  "An object that tracks credit consumption by virtual warehouses. You set thresholds (e.g., 80%, 100%) and choose actions: notify, notify and suspend, or notify and suspend immediately. Prevents runaway warehouse spend.",
  "Security","medium","Security",M),

c("What is a Snowflake Network Policy?",
  "A policy that restricts Snowflake account or user access based on IP address. You define an ALLOWED_IP_LIST (and optionally BLOCKED_IP_LIST). Can be applied at account or user level.",
  "Security","medium","Security",M),
]

# Data Loading Basics
cards += [
c("What is the COPY INTO <table> command?",
  "The primary bulk-loading command. It copies data from a stage into a Snowflake table. Supports CSV, JSON, Avro, ORC, Parquet, and XML. Options include ON_ERROR (continue/skip_file/abort_statement), PURGE, and VALIDATION_MODE.",
  "Data Loading","easy","Data Loading",M),

c("What is Snowpipe?",
  "Snowflake's continuous, serverless data ingestion service. When new files land in a cloud storage location (triggered via SQS/event notification or a REST API call), Snowpipe automatically loads them into the target table — typically within minutes.",
  "Data Loading","easy","Data Loading",M),

c("What is the difference between bulk loading (COPY INTO) and Snowpipe?",
  "Bulk loading uses a customer-managed virtual warehouse and is best for large, scheduled batch loads. Snowpipe is serverless (Snowflake-managed compute) and triggers on file arrival — best for continuous, low-latency micro-batch ingestion.",
  "Data Loading","medium","Data Loading",M),

c("What is the PUT command in Snowflake?",
  "Uploads files from a local file system to a Snowflake internal stage. Only available via the SnowSQL CLI or drivers — not in the Snowsight web UI. Usage: PUT file:///path/to/file @my_stage;",
  "Data Loading","medium","Data Loading",M),

c("What is the GET command in Snowflake?",
  "Downloads files from a Snowflake internal stage to a local file system. Like PUT, only available via SnowSQL or drivers. Usage: GET @my_stage/file.csv file:///local/path/;",
  "Data Loading","medium","Data Loading",M),
]

# Semi-structured basics
cards += [
c("What data type does Snowflake use to store semi-structured data?",
  "VARIANT — a flexible, self-describing column that can hold any JSON, XML, Avro, ORC, or Parquet value up to 16 MB. Snowflake automatically extracts and stores typed columns internally for efficient querying.",
  "Semi-Structured Data","easy","Semi-Structured Data",M),

c("How do you access a nested JSON key in a Snowflake VARIANT column?",
  "Using colon notation: column:key or column:key:nested_key. For example: SELECT src:address:city FROM my_table; Arrays use bracket notation: src:items[0]:price. Column names in the path are case-sensitive.",
  "Semi-Structured Data","easy","Semi-Structured Data",M),

c("What does PARSE_JSON() do in Snowflake?",
  "Converts a VARCHAR string containing a JSON document into a VARIANT value so you can traverse it with colon notation. Example: SELECT PARSE_JSON('{\"id\": 1}'):id::INT;",
  "Semi-Structured Data","medium","Semi-Structured Data",M),

c("What is FLATTEN in Snowflake?",
  "A table function that explodes arrays or objects in a VARIANT column into one row per element. Use it with LATERAL to join the expanded rows back to the outer query. Commonly used for processing JSON arrays.",
  "Semi-Structured Data","medium","Semi-Structured Data",M),
]

# Data Sharing
cards += [
c("What is Snowflake Secure Data Sharing?",
  "Lets you share live, read-only access to Snowflake objects (tables, views, UDFs) with other Snowflake accounts without copying or moving data. Sharing works at the micro-partition level — consumers always see up-to-date data.",
  "Data Sharing","easy","Data Sharing",M),

c("What is the Snowflake Marketplace?",
  "A platform built on Secure Data Sharing where data providers publish live datasets and consumers discover and access them — free or paid. Consumers access data directly in their own Snowflake account with no ETL.",
  "Data Sharing","easy","Data Sharing",M),

c("What is a Snowflake Reader Account?",
  "A Snowflake-managed account created by a data provider for a consumer who doesn't have their own Snowflake account. The provider pays for the Reader Account's compute. The consumer can only access data shared by that provider.",
  "Data Sharing","medium","Data Sharing",M),
]


# ════════════════════════════════════════════════════════
# MODULE 2 – SNOWFLAKE CORE
# ════════════════════════════════════════════════════════
M = "Snowflake Core"

# Architecture deep-dive
cards += [
c("What is query pruning in Snowflake?",
  "Before scanning data, Snowflake uses the min/max column statistics stored per micro-partition to skip partitions that cannot satisfy the query's WHERE predicates. The fewer micro-partitions scanned, the faster and cheaper the query.",
  "Architecture","medium","Architecture",M),

c("What is spilling to disk and why is it a performance problem?",
  "When an operation (sort, join, aggregation) requires more memory than the warehouse has available, Snowflake spills intermediate results to local SSD, then to remote cloud storage if SSD is also exhausted. Remote spill is very slow — it indicates the warehouse needs to be sized up.",
  "Architecture","medium","Architecture",M),

c("What is the result cache and when does it NOT apply?",
  "The result cache stores query results for 24 hours in the Cloud Services Layer. It does NOT apply when: the underlying table data has changed, the query uses non-deterministic functions (CURRENT_TIMESTAMP, RANDOM, SEQ), or the query uses columns with row access policies.",
  "Architecture","medium","Architecture",M),

c("What is the local disk cache (data cache) in Snowflake?",
  "Each virtual warehouse maintains an SSD cache of column data it has read from cloud storage during the current session. Subsequent queries on the same warehouse that access the same data can read from this cache instead of cloud storage — much faster. Cleared when the warehouse suspends.",
  "Architecture","hard","Architecture",M),

c("What is the Snowflake Cloud Services Layer responsible for?",
  "Authentication and authorisation, metadata management (table definitions, statistics, micro-partition maps), query parsing and optimisation (producing the query plan), and transaction management (ACID guarantees). It runs continuously — no warehouse is needed for its operations.",
  "Architecture","hard","Architecture",M),

c("How does Snowflake achieve ACID transactions?",
  "Through the Cloud Services Layer, which manages multi-version concurrency control (MVCC). Writers create new micro-partitions (old ones are immutable); readers see a consistent snapshot. This allows concurrent reads and writes without blocking.",
  "Architecture","hard","Architecture",M),
]

# Clustering
cards += [
c("What is a Clustering Key in Snowflake?",
  "One or more columns (or expressions) declared on a table that Snowflake uses to co-locate related data in the same micro-partitions. Well-chosen clustering keys improve pruning for queries that filter on those columns, reducing scan size and cost.",
  "Clustering","medium","Clustering",M),

c("What is Automatic Clustering in Snowflake?",
  "A Snowflake-managed background service that continuously reorganises the data in a clustered table so it remains well-clustered over time — especially after heavy DML. It consumes compute credits and is billed separately from virtual warehouses.",
  "Clustering","medium","Clustering",M),

c("How do you choose a good clustering key?",
  "Choose columns that are: (1) frequently used in WHERE / JOIN predicates, (2) high-cardinality but with locality (dates, region codes), (3) not too many — 1-3 columns is typical. Avoid high-cardinality columns like UUIDs or columns never filtered on.",
  "Clustering","hard","Clustering",M),

c("What are SYSTEM$CLUSTERING_INFORMATION() and SYSTEM$CLUSTERING_DEPTH()?",
  "System functions that report clustering quality. CLUSTERING_DEPTH returns the average depth of overlapping micro-partitions on a key — lower is better (1.0 = perfectly clustered). CLUSTERING_INFORMATION gives a JSON breakdown of the distribution.",
  "Clustering","hard","Clustering",M),
]

# Streams & Tasks
cards += [
c("What is a Snowflake Stream?",
  "A Change Data Capture (CDC) object that records INSERT, UPDATE, and DELETE operations made to a source table since the last time the stream was consumed. Reading the stream (via DML) advances its offset.",
  "Streams & Tasks","medium","Streams & Tasks",M),

c("What columns does a Snowflake Stream add to each row?",
  "METADATA$ACTION — INSERT or DELETE. METADATA$ISUPDATE — TRUE if the row is part of an UPDATE (updates appear as a DELETE + INSERT pair). METADATA$ROW_ID — a unique row identifier for the source row.",
  "Streams & Tasks","medium","Streams & Tasks",M),

c("What are the three types of Snowflake Streams?",
  "Standard — captures all DML (insert/update/delete) on a table. Append-only — captures only INSERTs; more efficient for insert-only sources (e.g., event logs). Insert-only (on external tables) — tracks new files added to an external stage.",
  "Streams & Tasks","hard","Streams & Tasks",M),

c("What is a Snowflake Task?",
  "A scheduled object that executes a single SQL statement or a call to a stored procedure. Tasks can be chained into DAGs using the AFTER clause. A root task has a CRON schedule; child tasks trigger when their parent succeeds.",
  "Streams & Tasks","medium","Streams & Tasks",M),

c("What is the relationship between Streams and Tasks in Snowflake?",
  "A common pattern: a Task checks SYSTEM$STREAM_HAS_DATA('my_stream') and runs a MERGE or INSERT from the stream into a target table. The Task consumes the stream, advancing its offset. This creates a lightweight incremental pipeline without external orchestration.",
  "Streams & Tasks","medium","Streams & Tasks",M),

c("What is a Snowflake Dynamic Table?",
  "A table whose contents are automatically refreshed by Snowflake based on a declarative query (like a materialised view). Unlike tasks+streams, you write the transformation logic once; Snowflake determines what changed and refreshes incrementally. Introduced as a simpler alternative to task DAGs.",
  "Streams & Tasks","hard","Streams & Tasks",M),
]

# Semi-structured (deeper)
cards += [
c("What is LATERAL FLATTEN and how is it different from plain FLATTEN?",
  "LATERAL FLATTEN joins the output of the FLATTEN table function back to each outer row. Without LATERAL, you'd write: FROM my_table, LATERAL FLATTEN(input => my_table.data:items). With LATERAL it's implicit: SELECT f.value FROM my_table, LATERAL FLATTEN(input => data:items) f. The LATERAL keyword is often optional in Snowflake syntax.",
  "Semi-Structured Data","hard","Semi-Structured Data",M),

c("What is OBJECT_CONSTRUCT() in Snowflake?",
  "Builds a VARIANT object from key-value pairs at query time: OBJECT_CONSTRUCT('id', 1, 'name', 'Alice'). Useful for assembling JSON output in SELECT statements or for feeding downstream VARIANT columns.",
  "Semi-Structured Data","medium","Semi-Structured Data",M),

c("What is ARRAY_AGG() in Snowflake?",
  "An aggregate function that collects column values into a VARIANT ARRAY. Often combined with OBJECT_CONSTRUCT to produce nested JSON output: SELECT ARRAY_AGG(OBJECT_CONSTRUCT('id', id, 'name', name)) FROM my_table;",
  "Semi-Structured Data","medium","Semi-Structured Data",M),

c("What does the :: operator do in Snowflake?",
  "Casts a VARIANT value to a SQL type: src:price::FLOAT, src:created_at::TIMESTAMP_NTZ. Without casting, Snowflake keeps the value as VARIANT, which may cause unexpected comparison behaviour.",
  "Semi-Structured Data","easy","Semi-Structured Data",M),

c("What file formats can Snowflake ingest natively into VARIANT columns?",
  "JSON, XML, Avro, ORC, and Parquet. COPY INTO automatically stores each top-level record as one VARIANT row when the file format is set to JSON/Avro/etc. CSV is not semi-structured and loads into individual typed columns.",
  "Semi-Structured Data","medium","Semi-Structured Data",M),
]

# Security (advanced)
cards += [
c("What is Dynamic Data Masking in Snowflake?",
  "A column-level security feature that applies a masking policy to a column. Users with privileged roles see real data; others see masked data (e.g., NULL, a fixed string, or a partially masked value). The masking is applied at query time — data on disk is unchanged.",
  "Security","medium","Security",M),

c("What is a Row Access Policy in Snowflake?",
  "Attaches a policy function to a table or view that filters rows returned to a user based on their role or session context. The filter is transparent — users with restricted access see fewer rows but aren't aware of the filtering.",
  "Security","medium","Security",M),

c("What is Snowflake's approach to encryption?",
  "All data at rest is encrypted with AES-256. All data in transit uses TLS. Snowflake manages encryption keys automatically (Snowflake-managed keys). Business Critical and VPS editions support customer-managed keys via Tri-Secret Secure (a key held jointly by Snowflake and the customer).",
  "Security","hard","Security",M),

c("What is Tri-Secret Secure in Snowflake?",
  "A Business Critical/VPS feature that combines a Snowflake-managed key with a customer-managed key (held in AWS KMS/Azure Key Vault/GCP KMS). Both keys are required to decrypt data — Snowflake alone cannot access it without the customer's key.",
  "Security","hard","Security",M),

c("What is column-level security in Snowflake?",
  "The ability to restrict access to specific columns using Dynamic Data Masking policies or by granting SELECT on individual columns (not the whole table). Privilege: GRANT SELECT (col1, col2) ON TABLE my_table TO ROLE analyst;",
  "Security","medium","Security",M),
]

# Performance
cards += [
c("What is the Search Optimization Service in Snowflake?",
  "An optional, paid table-level service that builds a search access path for selective equality and range queries on high-cardinality columns. Particularly useful for queries like WHERE id = 'some-uuid' that would otherwise scan many micro-partitions.",
  "Performance","hard","Performance",M),

c("What is a Query Profile in Snowflake?",
  "A graphical execution plan available in Snowsight showing each operator in the query, how long it took, rows processed, and bytes scanned. Key things to look for: spill to disk, large CartesianJoin, exploding joins, and which step is the bottleneck.",
  "Performance","medium","Performance",M),

c("When should you increase Virtual Warehouse size vs. add more clusters?",
  "Increase size (scale up) when individual queries are slow — they need more CPU/memory per query. Add clusters (scale out) when many users are queued and individual query speed is fine — they need more concurrent capacity.",
  "Performance","medium","Performance",M),

c("What is warehouse query queuing in Snowflake?",
  "When a single-cluster warehouse is at full concurrency, incoming queries queue. In Snowsight you can see queue time in the query history. Solutions: scale up the warehouse, enable multi-cluster, or route query types to separate warehouses.",
  "Performance","medium","Performance",M),

c("What is a Snowflake Resource Monitor and how does it help cost control?",
  "A Resource Monitor tracks credit usage by one or more virtual warehouses against a quota. When the quota reaches a threshold (e.g., 90%), it can notify, suspend, or immediately suspend the warehouse. Prevents unexpected runaway costs.",
  "Performance","medium","Performance",M),
]

# Replication
cards += [
c("What is database replication in Snowflake?",
  "A feature that replicates a database (or account objects) from a primary account to one or more secondary accounts in different regions or cloud providers. Used for read-scale, disaster recovery, and cross-region data sharing.",
  "Replication & DR","hard","Replication & DR",M),

c("What is a Snowflake Failover Group?",
  "A group of account objects (databases, integrations, warehouses) that can be failed over together from a primary to a secondary account. On failover, the secondary becomes the new primary and handles reads and writes.",
  "Replication & DR","hard","Replication & DR",M),
]


# ════════════════════════════════════════════════════════
# MODULE 3 – SNOWFLAKE SQL (code cards)
# ════════════════════════════════════════════════════════
M = "Snowflake SQL"

sql_cards = [
("Write a COPY INTO statement that loads all CSV files from the named internal stage @my_stage into the table 'raw_events'. Use the file format 'my_csv_format' and skip the first header row.",
 "```sql\nCOPY INTO raw_events\nFROM @my_stage\nFILE_FORMAT = (FORMAT_NAME = 'my_csv_format')\nON_ERROR = 'CONTINUE';\n```",
 "Loading"),

("Create a named internal stage called 'events_stage' with a CSV file format that uses comma delimiter, double-quote string delimiter, and skips one header line.",
 "```sql\nCREATE STAGE events_stage\n  FILE_FORMAT = (\n    TYPE = 'CSV'\n    FIELD_DELIMITER = ','\n    FIELD_OPTIONALLY_ENCLOSED_BY = '\"'\n    SKIP_HEADER = 1\n  );\n```",
 "Loading"),

("Create an external stage called 's3_stage' pointing to an S3 bucket, using a storage integration called 'my_s3_integration'.",
 "```sql\nCREATE STAGE s3_stage\n  URL = 's3://my-bucket/data/'\n  STORAGE_INTEGRATION = my_s3_integration\n  FILE_FORMAT = (TYPE = 'JSON');\n```",
 "Loading"),

("Write a query that reads the 'user_id' (integer) and 'event_name' (string) fields from a VARIANT column called 'raw' in the table 'events'.",
 "```sql\nSELECT\n    raw:user_id::INT        AS user_id,\n    raw:event_name::VARCHAR AS event_name\nFROM events;\n```",
 "Semi-Structured"),

("Use LATERAL FLATTEN to explode a JSON array at src:items into one row per item, selecting item:product_id and item:quantity from the 'orders' table.",
 "```sql\nSELECT\n    o.order_id,\n    f.value:product_id::INT      AS product_id,\n    f.value:quantity::INT        AS quantity\nFROM orders o,\n     LATERAL FLATTEN(input => o.src:items) f;\n```",
 "Semi-Structured"),

("Write a Time Travel query that shows what the 'customers' table looked like 2 hours ago.",
 "```sql\nSELECT *\nFROM customers\nAT (OFFSET => -60 * 60 * 2);\n```",
 "Time Travel"),

("Write a Time Travel query that restores the 'orders' table to its state before a specific statement ran (using the query ID).",
 "```sql\nCREATE OR REPLACE TABLE orders\n  CLONE orders\n  BEFORE (STATEMENT => '01ab2cd3-0004-5678-0000-000000000000');\n```",
 "Time Travel"),

("Create a zero-copy clone of the 'production' database named 'dev'.",
 "```sql\nCREATE DATABASE dev CLONE production;\n```",
 "Time Travel"),

("Create a stream called 'orders_stream' on the 'orders' table that captures all changes (standard stream).",
 "```sql\nCREATE STREAM orders_stream ON TABLE orders;\n```",
 "Streams & Tasks"),

("Write a MERGE statement that reads from 'orders_stream' and upserts into 'orders_target': insert new rows (METADATA$ACTION = 'INSERT') and delete removed rows.",
 "```sql\nMERGE INTO orders_target t\nUSING (\n    SELECT * FROM orders_stream\n    WHERE METADATA$ACTION = 'INSERT' OR METADATA$ISUPDATE\n) s ON t.order_id = s.order_id\nWHEN MATCHED THEN UPDATE SET t.status = s.status\nWHEN NOT MATCHED THEN INSERT (order_id, status) VALUES (s.order_id, s.status);\n```",
 "Streams & Tasks"),

("Create a Task that runs every hour, checks if orders_stream has data, and calls a stored procedure to process it.",
 "```sql\nCREATE TASK process_orders\n  WAREHOUSE = my_wh\n  SCHEDULE = 'USING CRON 0 * * * * UTC'\n  WHEN SYSTEM$STREAM_HAS_DATA('orders_stream')\nAS\n  CALL process_new_orders();\n\nALTER TASK process_orders RESUME;\n```",
 "Streams & Tasks"),

("Write a query using the QUALIFY clause to return only the most recent order per customer (using ROW_NUMBER).",
 "```sql\nSELECT\n    customer_id,\n    order_id,\n    order_date\nFROM orders\nQUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) = 1;\n```",
 "Snowflake SQL"),

("Write a query using SAMPLE to return approximately 10% of rows from 'events' (Bernoulli sampling).",
 "```sql\nSELECT *\nFROM events\nSAMPLE BERNOULLI (10);\n```",
 "Snowflake SQL"),

("Create a simple JavaScript UDF called 'add_tax' that takes a price FLOAT and returns price * 1.2.",
 "```sql\nCREATE OR REPLACE FUNCTION add_tax(price FLOAT)\nRETURNS FLOAT\nLANGUAGE JAVASCRIPT\nAS $$\n  return PRICE * 1.2;\n$$;\n```",
 "UDFs"),

("Create a masking policy called 'mask_email' that shows the real email to users with the ANALYST role, and returns '***' to everyone else. Then apply it to the 'email' column on 'customers'.",
 "```sql\nCREATE MASKING POLICY mask_email AS (val STRING)\nRETURNS STRING ->\n  CASE\n    WHEN CURRENT_ROLE() = 'ANALYST' THEN val\n    ELSE '***'\n  END;\n\nALTER TABLE customers\n  MODIFY COLUMN email SET MASKING POLICY mask_email;\n```",
 "Security"),

("Create a Resource Monitor called 'monthly_cap' with a 1000-credit monthly quota that suspends all warehouses at 100% and sends a notification at 80%.",
 "```sql\nCREATE RESOURCE MONITOR monthly_cap\n  WITH CREDIT_QUOTA = 1000\n       FREQUENCY = MONTHLY\n       START_TIMESTAMP = IMMEDIATELY\n  TRIGGERS\n    ON 80  PERCENT DO NOTIFY\n    ON 100 PERCENT DO SUSPEND;\n```",
 "Security"),

("Write a Snowpipe definition (CREATE PIPE) that auto-ingest files from an S3 stage into the 'events' table.",
 "```sql\nCREATE PIPE events_pipe\n  AUTO_INGEST = TRUE\nAS\n  COPY INTO events\n  FROM @s3_stage\n  FILE_FORMAT = (TYPE = 'JSON');\n```",
 "Loading"),

("Write a PIVOT query that turns status values ('placed','shipped','returned') into columns, counting orders per customer.",
 "```sql\nSELECT *\nFROM (\n    SELECT customer_id, status FROM orders\n)\nPIVOT (COUNT(*) FOR status IN ('placed', 'shipped', 'returned'))\n  AS p (customer_id, placed, shipped, returned);\n```",
 "Snowflake SQL"),

("Use OBJECT_CONSTRUCT and ARRAY_AGG to build a JSON array of {order_id, amount} objects grouped by customer_id.",
 "```sql\nSELECT\n    customer_id,\n    ARRAY_AGG(\n        OBJECT_CONSTRUCT('order_id', order_id, 'amount', amount)\n    ) AS orders_json\nFROM orders\nGROUP BY customer_id;\n```",
 "Semi-Structured"),

("Write a Dynamic Table definition that materialises a daily summary of revenue by product, refreshing when data is at most 1 hour stale.",
 "```sql\nCREATE DYNAMIC TABLE product_revenue_daily\n  TARGET_LAG = '1 hour'\n  WAREHOUSE = my_wh\nAS\n  SELECT\n      product_id,\n      DATE_TRUNC('day', order_date) AS order_day,\n      SUM(amount)                  AS daily_revenue\n  FROM orders\n  GROUP BY 1, 2;\n```",
 "Streams & Tasks"),
]

for q, a, group in sql_cards:
    cards.append(c(q, a, [group], "Medium", group, M, requires_code=True))


# ════════════════════════════════════════════════════════
# MODULE 4 – SNOWPRO CORE EXAM PREP
# ════════════════════════════════════════════════════════
M = "SnowPro Core"
CERT = "snowpro core"

cards += [
# Domain 1: Architecture (25%)
c("What separates Snowflake's architecture from shared-disk and shared-nothing architectures?",
  "Snowflake uses a hybrid: storage is shared (centralised cloud object storage accessed by all compute) like shared-disk, but compute nodes (virtual warehouses) are independent MPP clusters that don't share memory or CPU, like shared-nothing. This gives both storage elasticity and compute isolation.",
  "Domain 1: Architecture","medium","Domain 1: Architecture",M,CERT),

c("Can multiple virtual warehouses access the same data simultaneously in Snowflake?",
  "Yes. Because storage and compute are decoupled, any number of virtual warehouses can read from the same tables concurrently without contention. Each warehouse has its own local disk cache, but underlying storage is shared.",
  "Domain 1: Architecture","medium","Domain 1: Architecture",M,CERT),

c("What happens to the local disk (data) cache when a virtual warehouse is suspended?",
  "It is lost. The cache is stored on the warehouse's local SSDs; suspension deallocates those resources. When the warehouse resumes, the cache starts empty and is rebuilt as queries are executed.",
  "Domain 1: Architecture","medium","Domain 1: Architecture",M,CERT),

c("What is the maximum Time Travel retention for Enterprise edition?",
  "90 days for permanent tables. Standard edition is limited to 1 day. Temporary and transient tables are limited to 0 or 1 day regardless of edition.",
  "Domain 1: Architecture","medium","Domain 1: Architecture",M,CERT),

c("What is the Fail-Safe period and who can access data during it?",
  "7 days, non-configurable, beginning after the Time Travel window closes. Only Snowflake Support can recover data during Fail-Safe — it is not user-accessible. It exists as an emergency recovery measure, not a routine tool.",
  "Domain 1: Architecture","medium","Domain 1: Architecture",M,CERT),

c("What is the purpose of the 60-second minimum warehouse billing?",
  "Warehouses are billed for at least 60 seconds each time they start (resume or initial start). After the first 60 seconds, billing is per-second. This means very short queries benefit from keeping warehouses running (or using Snowpark-optimised warehouses with different billing).",
  "Domain 1: Architecture","hard","Domain 1: Architecture",M,CERT),

c("What are the scaling modes for a multi-cluster warehouse?",
  "Auto-scale mode — clusters spin up when queries queue and shut down when load drops (recommended for variable concurrency). Maximised mode — all clusters run at all times (for consistently high concurrency). You set min and max cluster counts.",
  "Domain 1: Architecture","hard","Domain 1: Architecture",M,CERT),

c("Which Snowflake edition supports multi-cluster virtual warehouses?",
  "Enterprise edition and above (Enterprise, Business Critical, VPS). Standard edition supports only single-cluster warehouses.",
  "Domain 1: Architecture","medium","Domain 1: Architecture",M,CERT),

c("What is a Snowflake account and how does it differ from a database?",
  "An account is the top-level entity — it represents a Snowflake subscription tied to a cloud provider and region. It contains all databases, warehouses, users, roles, and other objects. A database is an object within an account that organises schemas and their tables.",
  "Domain 1: Architecture","easy","Domain 1: Architecture",M,CERT),

# Domain 2: Security (20%)
c("How does Snowflake combine RBAC and DAC?",
  "Snowflake uses RBAC as the primary model (privileges granted to roles, roles granted to users). DAC is layered on top: every object has an owner role, and that role can grant privileges on the object to other roles. The combination is called DAC + RBAC.",
  "Domain 2: Security","medium","Domain 2: Security",M,CERT),

c("What is the difference between SECURITYADMIN and USERADMIN?",
  "USERADMIN creates and manages users and roles only. SECURITYADMIN inherits USERADMIN's privileges AND can GRANT/REVOKE any privilege on any object in the account — making it effectively a security superuser.",
  "Domain 2: Security","medium","Domain 2: Security",M,CERT),

c("What is Federated Authentication / SSO in Snowflake?",
  "Allows users to log in to Snowflake using an external Identity Provider (e.g., Okta, Azure AD) via SAML 2.0. Snowflake validates the SAML assertion rather than an internal password. MFA can be enforced by the IdP.",
  "Domain 2: Security","medium","Domain 2: Security",M,CERT),

c("What is key-pair authentication in Snowflake?",
  "An alternative to password-based authentication where the user authenticates with a private RSA key. Used with programmatic clients (Python, JDBC, ODBC). The public key is registered with the user in Snowflake; the private key stays client-side.",
  "Domain 2: Security","hard","Domain 2: Security",M,CERT),

c("What encryption does Snowflake apply by default?",
  "AES-256 for data at rest, TLS 1.2+ for data in transit. Encryption is automatic and transparent — all data in Snowflake's storage layer is encrypted using a hierarchy of keys managed by Snowflake.",
  "Domain 2: Security","medium","Domain 2: Security",M,CERT),

c("What are Object Tags in Snowflake and how do they relate to governance?",
  "String key-value pairs that can be attached to Snowflake objects (tables, columns, warehouses). Used for data classification (e.g., sensitivity: 'PII'), cost tracking, and as selectors for masking policies or row access policies.",
  "Domain 2: Security","hard","Domain 2: Security",M,CERT),

# Domain 3: Performance (15%)
c("In what order does Snowflake check caches before going to cloud storage?",
  "1. Result cache (Cloud Services Layer) — if the exact same query was run recently and data hasn't changed, return the cached result immediately. 2. Local disk cache (warehouse SSD) — if the required micro-partitions are already in the warehouse's cache. 3. Cloud storage — fetch the micro-partitions from S3/GCS/Azure.",
  "Domain 3: Performance","hard","Domain 3: Performance",M,CERT),

c("What metrics in a Query Profile indicate that a warehouse is undersized?",
  "Spill to local storage and spill to remote storage — these appear as distinct operations in the profile. Remote spill is the worst indicator. Also watch for long Sort or Aggregate steps with high bytes spilled.",
  "Domain 3: Performance","hard","Domain 3: Performance",M,CERT),

c("What is the Search Optimization Service and what types of queries benefit most?",
  "A paid table service that builds a secondary search access path for point lookups on high-cardinality columns (e.g., WHERE id = 'uuid'). Queries with highly selective equality/range predicates on non-clustered columns benefit most. Analytic queries with range scans on clustered keys generally don't need it.",
  "Domain 3: Performance","hard","Domain 3: Performance",M,CERT),

c("How does warehouse size affect performance for a complex GROUP BY query?",
  "A larger warehouse has more CPU cores and more memory per node. For a memory-intensive GROUP BY on a large dataset, a larger size prevents spilling and completes the aggregation faster. However, for small queries the query may already be fast at XS — upgrading doesn't help.",
  "Domain 3: Performance","medium","Domain 3: Performance",M,CERT),

# Domain 4: Data Loading (15%)
c("What file formats can COPY INTO load natively?",
  "CSV, JSON, Avro, ORC, Parquet, and XML. Snowflake also supports gzip, Bzip2, Brotli, Zstandard, Deflate, and Raw Deflate compression on most formats.",
  "Domain 4: Data Loading","medium","Domain 4: Data Loading",M,CERT),

c("What does VALIDATION_MODE in COPY INTO do?",
  "Validates the files without loading them. RETURN_ERRORS returns all rows that would fail. RETURN_N_ROWS returns the first N rows that would be loaded. Useful for checking file format issues before committing a load.",
  "Domain 4: Data Loading","medium","Domain 4: Data Loading",M,CERT),

c("What does ON_ERROR = 'SKIP_FILE' do in COPY INTO?",
  "If any row in a file causes an error, the entire file is skipped (not loaded). Other files in the COPY operation continue. Compare with CONTINUE (skip only the bad row) and ABORT_STATEMENT (stop the whole COPY).",
  "Domain 4: Data Loading","hard","Domain 4: Data Loading",M,CERT),

c("What is the PURGE option in COPY INTO?",
  "When PURGE = TRUE, Snowflake automatically removes the source files from the stage after a successful load. Reduces storage cost and simplifies pipeline cleanup.",
  "Domain 4: Data Loading","medium","Domain 4: Data Loading",M,CERT),

c("What is a file format object in Snowflake?",
  "A named, reusable object (CREATE FILE FORMAT) that stores file format settings (type, delimiter, null string, skip_header, etc.). Referenced in COPY INTO and stage definitions by name — avoids repeating settings in every COPY statement.",
  "Domain 4: Data Loading","easy","Domain 4: Data Loading",M,CERT),

c("What triggers Snowpipe to load a new file?",
  "Either: (1) an event notification from cloud storage (SQS for S3, Azure Event Grid, GCS Pub/Sub) configured to fire when a file lands — AUTO_INGEST=TRUE; or (2) a REST API call to Snowpipe's insertFiles endpoint that explicitly notifies Snowpipe of new files.",
  "Domain 4: Data Loading","hard","Domain 4: Data Loading",M,CERT),

# Domain 5: Data Transformation (15%)
c("What SQL languages/constructs can Snowflake UDFs be written in?",
  "JavaScript, Python, Java, Scala, and SQL. Table UDFs (UDTFs) return a table instead of a scalar. UDFs are called in SQL like built-in functions.",
  "Domain 5: Transformations","medium","Domain 5: Transformations",M,CERT),

c("What is a Snowflake Stored Procedure and how does it differ from a UDF?",
  "A stored procedure encapsulates procedural logic (loops, conditionals, DDL, DML). Unlike UDFs, stored procedures are called with CALL (not in SELECT), can return a single value or nothing, and can run DDL statements. Written in JavaScript, Python, Java, Scala, or Snowflake Scripting (SQL).",
  "Domain 5: Transformations","medium","Domain 5: Transformations",M,CERT),

c("What does the QUALIFY clause do in Snowflake SQL?",
  "Filters rows after window functions are evaluated — analogous to HAVING for aggregates. Eliminates the need for a wrapping subquery: SELECT ..., ROW_NUMBER() OVER (...) AS rn FROM t QUALIFY rn = 1;",
  "Domain 5: Transformations","medium","Domain 5: Transformations",M,CERT),

c("How do you query a specific index in a JSON array stored in a VARIANT column?",
  "Use bracket notation: column:array[0] for the first element, column:array[1] for the second, etc. You can chain: src:items[0]:product_id::INT to get the product_id of the first item and cast it to INT.",
  "Domain 5: Transformations","medium","Domain 5: Transformations",M,CERT),

# Domain 6: Data Protection & Sharing (10%)
c("What objects can be included in a Snowflake Share?",
  "Tables, external tables, secure views, secure materialised views, and secure UDFs. Standard (non-secure) views are not shareable. The consumer mounts the share as a read-only database in their account.",
  "Domain 6: Data Sharing","medium","Domain 6: Data Sharing",M,CERT),

c("What is the difference between a Data Exchange and the Snowflake Marketplace?",
  "The Snowflake Marketplace is a public, global listing where any Snowflake account can publish or discover data products. A Data Exchange is a private, invitation-only sharing hub — organisations create their own exchange for a defined group of partners or internal business units.",
  "Domain 6: Data Sharing","hard","Domain 6: Data Sharing",M,CERT),

c("Does data sharing in Snowflake involve copying data between accounts?",
  "No. Secure Data Sharing is a live pointer to the provider's data stored in their account. The consumer's virtual warehouse queries the provider's micro-partitions directly — there is no ETL or duplication. Data is always current.",
  "Domain 6: Data Sharing","medium","Domain 6: Data Sharing",M,CERT),

c("What is database replication in Snowflake used for?",
  "Replicating a Snowflake database to a secondary account in a different region or cloud provider. Used for: disaster recovery / failover, read-scale distribution, and moving data closer to users in other geographies.",
  "Domain 6: Data Sharing","hard","Domain 6: Data Sharing",M,CERT),
]


# ════════════════════════════════════════════════════════
# MODULE 5 – SNOWPRO ADVANCED: DATA ENGINEER
# ════════════════════════════════════════════════════════
M = "SnowPro Data Engineer"
CERT = "snowpro advanced data engineer"

cards += [
c("What is the difference between Snowpipe and COPY INTO for continuous ingestion?",
  "COPY INTO runs in a user-managed warehouse on demand or on schedule — suited for large, batch loads. Snowpipe uses Snowflake-managed (serverless) compute and triggers automatically when files arrive — suited for near-real-time micro-batch ingestion with low operational overhead.",
  "Data Ingestion","medium","Data Ingestion",M,CERT),

c("How does Snowpipe handle duplicate files?",
  "Snowpipe tracks file metadata (path + ETag) and skips files that were already loaded within the past 64 days. To force reload a file, you must either rename it, change its content (changing ETag), or use the COPY INTO command with FORCE=TRUE.",
  "Data Ingestion","hard","Data Ingestion",M,CERT),

c("What is the Kafka Connector for Snowflake and how does it ingest data?",
  "A Kafka Connect plugin that continuously reads messages from Kafka topics and writes them to Snowflake tables (via Snowpipe or INSERT). Each Kafka record becomes a VARIANT row in a Snowflake table. Supports exactly-once delivery using offset tracking.",
  "Data Ingestion","hard","Data Ingestion",M,CERT),

c("What is an append-only stream and when should you use it?",
  "A stream type that only captures INSERT operations — it ignores UPDATEs and DELETEs. More storage-efficient than a standard stream because the change tracking overhead is lower. Use it on insert-only source tables such as event logs, audit tables, or Snowpipe landing tables.",
  "Streams & Tasks","medium","Streams & Tasks",M,CERT),

c("How do you build a task DAG in Snowflake?",
  "Create a root task with a CRON schedule and child tasks with AFTER <parent_task>. Child tasks run when their parent succeeds. Use ALTER TASK ... RESUME to activate each task (root last). The DAG is visualised in Snowsight under the task definition.",
  "Streams & Tasks","medium","Streams & Tasks",M,CERT),

c("What is the maximum number of child tasks per root task (task DAG) in Snowflake?",
  "1,000 tasks in a single DAG (as of current limits). Root task can have multiple direct children, each of which can have their own children.",
  "Streams & Tasks","hard","Streams & Tasks",M,CERT),

c("What is a Snowflake Dynamic Table and how does it differ from a stream+task pipeline?",
  "A Dynamic Table is a declarative, automatically refreshed materialisation: you write the transformation SQL; Snowflake tracks dependencies, determines changed data, and refreshes it. A stream+task pipeline is imperative: you write the CDC logic yourself. Dynamic Tables simplify pipeline code but offer less control over exactly when/how changes are applied.",
  "Streams & Tasks","hard","Streams & Tasks",M,CERT),

c("What is TARGET_LAG in a Dynamic Table?",
  "Specifies the acceptable freshness lag: how far behind the Dynamic Table can be relative to its source data. Snowflake refreshes the table at a rate needed to stay within this lag. Setting 'DOWNSTREAM' means the lag is inherited from downstream Dynamic Tables.",
  "Streams & Tasks","hard","Streams & Tasks",M,CERT),

c("What is the difference between a Standard stream and an Insert-only stream on an external table?",
  "Standard streams on regular tables capture INSERT/UPDATE/DELETE. External table streams are insert-only by nature (external files are immutable) — they track which new files have been added to the external stage, enabling incremental processing of data-lake files.",
  "Streams & Tasks","hard","Streams & Tasks",M,CERT),

c("How do you implement idempotent incremental loads in Snowflake using streams?",
  "Use MERGE (not INSERT) when consuming the stream: match on a primary key, update matched rows, insert new rows. Because MERGE is atomic and streams track consumed changes, re-running the task will not double-insert — the stream will be empty unless new changes have arrived.",
  "Streams & Tasks","hard","Streams & Tasks",M,CERT),

c("What is COPY INTO <location> (unloading) and what formats does it support?",
  "Exports query results or table data to a Snowflake internal stage or external cloud storage. Supports CSV, JSON, Parquet. Options include HEADER (add column names), PARTITION BY (create sub-folders), MAX_FILE_SIZE, and compression.",
  "Data Loading","medium","Data Loading",M,CERT),

c("What is the Semi-structured schema detection feature in Snowflake?",
  "INFER_SCHEMA() and the related column definitions in COPY INTO auto-detect column names and types from staged Parquet, Avro, or ORC files. You can use CREATE TABLE ... USING TEMPLATE (SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*)) FROM TABLE(INFER_SCHEMA(...))) to auto-create a matching table.",
  "Semi-Structured","hard","Semi-Structured",M,CERT),

c("What is schema evolution in Snowflake COPY INTO?",
  "When ENABLE_SCHEMA_EVOLUTION = TRUE on a table, COPY INTO will automatically add new columns found in the source files (for semi-structured data) rather than failing. This allows the table schema to evolve as the source adds new fields without manual ALTER TABLE.",
  "Data Loading","hard","Data Loading",M,CERT),

c("What is a Snowflake Directory Table?",
  "Automatically maintained metadata about the files in a stage: file path, size, ETag, last modified time. Accessed via TABLE(@stage). Used in pipeline code to discover and process files efficiently — for example, to find all files added after a given timestamp.",
  "Data Ingestion","hard","Data Ingestion",M,CERT),

c("How can you monitor Snowpipe ingestion lag and errors?",
  "Use SYSTEM$PIPE_STATUS() to check pipe state, pending file count, and last loaded time. Query LOAD_HISTORY (information schema) or COPY_HISTORY (account_usage) for per-file load status and error details.",
  "Data Ingestion","hard","Data Ingestion",M,CERT),

c("What is the role of a Storage Integration in Snowflake?",
  "A Snowflake object that stores credentials (IAM role ARN for AWS, service account for GCP, service principal for Azure) for accessing external cloud storage. Stages reference the integration instead of hardcoding access keys — centralising credential management and enabling key rotation without updating every stage.",
  "Data Ingestion","medium","Data Ingestion",M,CERT),

c("What is Snowpark and how does it relate to data engineering in Snowflake?",
  "Snowpark is a developer framework that lets you write data transformation logic in Python, Java, or Scala using a DataFrame API that executes natively inside Snowflake. Data engineers use it to write complex pipeline code that pushes compute to Snowflake, replacing Spark for many use cases.",
  "Snowpark","hard","Snowpark",M,CERT),

c("What is a Snowpark Optimised Warehouse?",
  "A special warehouse type with 16x more memory per node than a standard warehouse, designed for memory-intensive ML workloads and large Snowpark (Python/Java) operations. Billed at a higher credit rate. Not recommended for standard SQL analytics.",
  "Snowpark","hard","Snowpark",M,CERT),
]


# ════════════════════════════════════════════════════════
# MODULE 6 – SNOWPRO ADVANCED: ARCHITECT
# ════════════════════════════════════════════════════════
M = "SnowPro Architect"
CERT = "snowpro advanced architect"

cards += [
c("What considerations drive the choice of Snowflake cloud provider and region?",
  "Data residency and compliance requirements (GDPR, data sovereignty), latency to existing systems and users, colocation with other cloud services (e.g., Kafka on AWS → Snowflake on AWS), pricing differences, and supported features (some features are region-specific).",
  "Account Design","medium","Account Design",M,CERT),

c("When would you use multiple Snowflake accounts vs. multiple databases within one account?",
  "Multiple accounts for: hard isolation (different organisations, strict compliance boundaries, separate billing), cross-cloud deployments, or production/non-production separation with no risk of cross-environment access. Multiple databases within one account for: cost consolidation, shared governance, simpler cross-database queries (no replication needed).",
  "Account Design","hard","Account Design",M,CERT),

c("What is a Snowflake Organisation and what does it enable?",
  "An overarching entity that links multiple Snowflake accounts under a single organisation name. Enables: account-level replication, cross-account cost visibility in ORGANISATION_USAGE, and Snowflake Marketplace publisher identity that spans accounts.",
  "Account Design","hard","Account Design",M,CERT),

c("How should you design the role hierarchy for a large enterprise Snowflake deployment?",
  "Custom functional roles (ANALYST, DATA_ENGINEER, REPORTER) grant object-level privileges. Custom access roles (DB_PROD_READ, DB_PROD_WRITE) own and grant access to specific databases. Functional roles inherit access roles. SYSADMIN sits above custom roles. Never grant ACCOUNTADMIN to functional users.",
  "Governance","hard","Governance",M,CERT),

c("What is the Snowflake Data Governance suite and what features does it include?",
  "A set of Enterprise+ features: Dynamic Data Masking (column-level obfuscation), Row Access Policies (row-level filtering), Object Tags (classification labels), Tag-Based Masking (apply masking via tags), Data Classification (auto-suggest tags for PII), Access History (query-level column-read audit log), and Policy Management (centralised policy objects).",
  "Governance","hard","Governance",M,CERT),

c("What is Access History in Snowflake and why is it important for architects?",
  "A feature (Enterprise+) that records which columns each query read or modified, who ran the query, and when. Stored in SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY. Used for data lineage audits, PII access monitoring, and compliance reporting.",
  "Governance","hard","Governance",M,CERT),

c("What is Private Connectivity in Snowflake (AWS PrivateLink / Azure Private Link / GCP Private Service Connect)?",
  "Routes Snowflake traffic over the cloud provider's private backbone instead of the public internet. Traffic never leaves the provider's network — reducing exposure and satisfying compliance requirements that prohibit public internet data transfer. Requires Business Critical or higher edition.",
  "Security Architecture","hard","Security Architecture",M,CERT),

c("What is a Snowflake Data Clean Room?",
  "A pattern (using Secure Data Sharing and Secure Views) that lets two parties run joint analyses on combined data without either party seeing the other's raw data. Neither side can extract the other's rows — they can only see aggregated or pre-defined query results.",
  "Data Sharing","hard","Data Sharing",M,CERT),

c("How do you architect cross-region disaster recovery in Snowflake?",
  "Use Replication Groups (or Business Critical Failover Groups) to asynchronously replicate specified databases and account objects to a secondary account in a different region. Define an RPO (acceptable data loss) matching your replication schedule, and test failover regularly. Point DNS/connections at the primary account; redirect to secondary on failover.",
  "Replication & DR","hard","Replication & DR",M,CERT),

c("What is the difference between database replication and a Failover Group?",
  "Database replication replicates data only. A Failover Group replicates both data AND account objects (users, roles, resource monitors, warehouses, integrations) needed to run a full Snowflake environment on the secondary account. Failover Groups support full account-level DR.",
  "Replication & DR","hard","Replication & DR",M,CERT),

c("What are the RPO and RTO considerations when designing Snowflake HA?",
  "RPO (Recovery Point Objective) — time between the last replication sync and a failure. Governed by the replication schedule (minimum ~1 minute for some features). RTO (Recovery Time Objective) — time to promote the secondary and redirect connections. Promotion is near-instant in Snowflake; the bottleneck is usually DNS/connection-string updates.",
  "Replication & DR","hard","Replication & DR",M,CERT),

c("How would you design a cost allocation model across business units sharing one Snowflake account?",
  "Create one virtual warehouse per business unit (or one per workload type). Apply Resource Monitors per warehouse with per-BU quotas. Tag warehouses with the business unit using Object Tags. Report on usage via ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY filtered by warehouse name or tag. Optionally use separate accounts with cross-account cost reporting via ORGANISATION_USAGE.",
  "Cost Architecture","hard","Cost Architecture",M,CERT),

c("What is a Snowflake Marketplace listing and what can be listed?",
  "A published data product on the Snowflake Marketplace. Listings can contain: databases shared via Secure Data Sharing (live data), or Native Apps (applications built on the Snowflake Native App Framework). Listings can be free, paid (via Snowflake billing), or request-only.",
  "Data Sharing","hard","Data Sharing",M,CERT),

c("What is the Snowflake Native App Framework?",
  "Allows ISVs and data providers to build applications that run inside a consumer's Snowflake account — not just data shares. Native Apps can include Streamlit UIs, stored procedures, Python UDFs, and reference data. The provider's code runs in the consumer's account but the provider controls what it can access.",
  "Data Sharing","hard","Data Sharing",M,CERT),

c("How does Snowflake handle data lineage at the platform level?",
  "Snowflake provides: (1) Access History (column-level read/write tracking). (2) Object Dependencies (SNOWFLAKE.ACCOUNT_USAGE.OBJECT_DEPENDENCIES shows how views/tasks/pipes reference tables). (3) Dynamic Tables have built-in lineage visualisation in Snowsight. For end-to-end data lineage across tools, integrate with a third-party catalog (e.g., Atlan, Alation, OpenMetadata).",
  "Governance","hard","Governance",M,CERT),

c("What performance patterns should a Snowflake architect consider for a mixed workload (OLAP + ad-hoc + ETL)?",
  "Separate virtual warehouses by workload type: large ETL warehouse (L/XL, auto-suspend 5 min), medium analytics warehouse (M, multi-cluster for concurrency), small ad-hoc/BI warehouse (S/XS, auto-suspend 1 min). Use resource monitors per warehouse. Consider a Snowpark-optimised warehouse for ML workloads. Route by application/role using connection strings.",
  "Performance Architecture","hard","Performance Architecture",M,CERT),
]


# ══ Build and write the deck ══════════════════════════════
MODULES_ORDERED = [
    "Snowflake 101",
    "Snowflake Core",
    "Snowflake SQL",
    "SnowPro Core",
    "SnowPro Data Engineer",
    "SnowPro Architect",
]

data['decks']['Snowflake'] = {
    "section": "Professional Development",
    "modules_ordered": MODULES_ORDERED,
    "cards": cards,
}

with open('frontend/cards.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

from collections import Counter
mods = Counter(c['module'] for c in cards)
code = sum(1 for c in cards if c.get('requires_code'))
print(f"Total: {len(cards)} cards  ({code} code cards)\n")
for m in MODULES_ORDERED:
    print(f"  {mods[m]:3}  {m}")
