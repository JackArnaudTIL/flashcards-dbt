"""
Data Engineering Concepts deck overhaul:
1. Remove irrelevant / too-basic cards
2. Remove duplicate cards
3. Merge / rename categories (22 → 18 + 3 new = ~18 total)
4. Add new cards for identified gaps
5. Assign module field and modules_ordered
"""
import json

with open('frontend/cards.json', encoding='utf-8') as f:
    data = json.load(f)

de = data['decks']['Data Engineering Concepts']
cards = de['cards']
original_count = len(cards)

# ── 1. REMOVE — irrelevant / too basic ───────────────────────────────────────
REMOVE_FRAGMENTS = [
    # Low-level CS fundamentals — not DE
    'What is Binary (Base-2)',
    'What is a Bit?',
    'What is a Byte?',
    'What is Hexadecimal (Base-16)',
    "What is 'Endianness'",
    # OS internals — too low-level for DE role
    'What is the Kernel?',
    'What is a Daemon?',
    'What is a System Call (syscall)',
    'SIGTERM vs. SIGKILL',
    "What is 'User Space' vs. 'Kernel Space'",
    "What is a 'Zombie' or 'Orphan' Process",
    # Not a DE language
    'What is R primarily used for',
    # Too niche
    "What is an 'AI Shell Alias'",
]

# ── 2. REMOVE — duplicates (keep the better copy) ────────────────────────────
REMOVE_DUPLICATES = [
    # Keep "What is 'Data Downtime'?" in Observability
    ("Data Engineering-Specific Tools", "What is 'Data Downtime'?"),
    # Keep "What is 'Backpressure' in a streaming system?" in Event-Driven
    ("General Computing Concepts", "What is 'Backpressure' in a data stream?"),
    # Keep "What is HDFS (Hadoop Distributed File System)?" in Storage
    ("Big Data Technologies", "What is HDFS?"),
    # Keep "What is 'Idempotency' in a DAG task?" in DE-Specific Tools
    ("Advanced Scripting and Automation", "What is 'Idempotency' in Automation?"),
    # Keep "What is 'Data Diffing'..." in Debugging
    ("Data Engineering-Specific Tools", "What is 'Data Diffing' (e.g., Datafold)?"),
    # Keep "What is 'Resource Contention' in a compute cluster?" in Computation
    ("General Computing Concepts", "What is 'Resource Contention'?"),
    # Keep "What is an Airflow DAG?" in DE-Specific Tools
    ("Programming and Data Processing", "In the context of Apache Airflow, what is a DAG?"),
]

def should_remove(card):
    q = card.get('q', '')
    for frag in REMOVE_FRAGMENTS:
        if frag in q:
            return True
    cat = card.get('category', '')
    for (dup_cat, dup_q) in REMOVE_DUPLICATES:
        if cat == dup_cat and q == dup_q:
            return True
    return False

before = len(cards)
cards = [c for c in cards if not should_remove(c)]
removed = before - len(cards)
print(f'Removed {removed} cards ({before} -> {len(cards)})')

# ── 3. RENAME / MERGE categories ─────────────────────────────────────────────
CATEGORY_MAP = {
    # Merge Computation + General Computing + surviving System-Level → Computing Concepts
    'Computation Concepts':       'Computing Concepts',
    'General Computing Concepts': 'Computing Concepts',
    'System-Level Concepts':      'Computing Concepts',
    # Merge Programming + Scripting + Software Engineering
    'Programming and Data Processing':  'Programming & Automation',
    'Advanced Scripting and Automation':'Programming & Automation',
    'Software Engineering Basics':      'Programming & Automation',
    # Merge Observability + Debugging
    'Data Observability and Quality':   'Observability & Debugging',
    'Debugging and Auditing':           'Observability & Debugging',
    # Merge Storage + File Management + surviving Low-Level Data
    'Storage and Memory Concepts':      'Storage & Data Formats',
    'File Management and Optimization': 'Storage & Data Formats',
    'Low-Level Data Concepts':          'Storage & Data Formats',
    # Rename DE-Specific Tools
    'Data Engineering-Specific Tools':  'Data Engineering Tools',
}

renamed = 0
for card in cards:
    old = card.get('category', '')
    new = CATEGORY_MAP.get(old)
    if new:
        card['category'] = new
        renamed += 1

print(f'Renamed category on {renamed} cards')

# ── 4. ADD new cards ──────────────────────────────────────────────────────────
NEW_CARDS = [
    # ── Open Table Formats ────────────────────────────────────────────────────
    {
        'q': 'What is an Open Table Format?',
        'a': 'A specification that adds database-like features — ACID transactions, schema evolution, time travel, and partition pruning — on top of raw files in object storage (S3, GCS, ADLS). The three main formats are Apache Iceberg, Delta Lake, and Apache Hudi. They enable the Lakehouse pattern: a data lake queryable like a warehouse without moving data.',
        'category': 'Open Table Formats', 'group': ['Storage', 'Lakehouse'], 'difficulty': 'Easy',
    },
    {
        'q': 'What is Apache Iceberg?',
        'a': 'An open table format for large analytic datasets. Key features: ACID transactions, hidden partitioning (no partition column in queries), schema evolution, time travel via snapshots, and engine-agnostic design (Spark, Trino, Flink, Snowflake, BigQuery). Governed by the Apache Software Foundation — the most widely adopted open table format for multi-engine environments.',
        'category': 'Open Table Formats', 'group': ['Storage', 'Lakehouse'], 'difficulty': 'Medium',
    },
    {
        'q': 'What is Delta Lake?',
        'a': 'An open-source storage layer from Databricks adding ACID transactions, time travel, schema enforcement, and Z-ordering to Apache Spark workloads. Uses a transaction log (`_delta_log`) stored alongside data files. Tightly integrated with Databricks but also open-source. The default table format in the Databricks Lakehouse Platform.',
        'category': 'Open Table Formats', 'group': ['Storage', 'Lakehouse'], 'difficulty': 'Medium',
    },
    {
        'q': 'What is Apache Hudi?',
        'a': 'An open table format from Uber optimised for high-frequency upserts and CDC workloads. Two table types: Copy-on-Write (COW — optimised for reads) and Merge-on-Read (MOR — optimised for write speed). Preferred when writing CDC streams from Kafka into a lake. Native support on AWS EMR.',
        'category': 'Open Table Formats', 'group': ['Storage', 'Lakehouse'], 'difficulty': 'Medium',
    },
    {
        'q': 'Comparison: Apache Iceberg vs. Delta Lake vs. Apache Hudi?',
        'a': 'All three provide ACID transactions and time travel on object storage. **Iceberg**: best engine interoperability, hidden partitioning, strongest open governance — prefer for multi-engine shops. **Delta Lake**: deepest Databricks/Spark integration, easiest on Databricks stacks. **Hudi**: best for high-frequency upserts and CDC from Kafka — prefer when writes dominate. Iceberg is the emerging default for new multi-engine builds.',
        'category': 'Open Table Formats', 'group': ['Storage', 'Lakehouse'], 'difficulty': 'Hard',
    },
    {
        'q': "What is 'Time Travel' in an open table format?",
        'a': 'The ability to query a table as it existed at a past snapshot or timestamp. Each write creates a new immutable snapshot; the format retains metadata pointing to old data files. Example: `SELECT * FROM orders VERSION AS OF 5` (Delta) or `FOR SYSTEM_TIME AS OF \'2024-01-01\'` (Iceberg/Snowflake). Used for debugging, auditing, and incremental pipeline restarts.',
        'category': 'Open Table Formats', 'group': ['Storage', 'Time Travel'], 'difficulty': 'Medium',
    },
    {
        'q': 'What is a Table Catalog in the context of open table formats?',
        'a': 'A central metadata service tracking table locations, schemas, and snapshot history — required for query engines to find and read open-format tables. Examples: AWS Glue Catalog, Apache Polaris (open-source REST catalog donated by Snowflake), Databricks Unity Catalog, Project Nessie. Without a catalog each engine must be manually pointed to the metadata location.',
        'category': 'Open Table Formats', 'group': ['Storage', 'Metadata'], 'difficulty': 'Medium',
    },

    # ── Data Integration & Ingestion Tools ────────────────────────────────────
    {
        'q': 'What is Fivetran?',
        'a': 'A fully managed ELT connector platform replicating data from 500+ sources (SaaS apps, databases, files) into a data warehouse. Connectors are maintained by Fivetran — zero maintenance overhead for your team. Handles schema drift automatically. Pricing is based on Monthly Active Rows (MAR). Best when reliability and time-to-value outweigh cost.',
        'category': 'Data Integration & Ingestion Tools', 'group': ['Ingestion', 'ELT'], 'difficulty': 'Easy',
    },
    {
        'q': 'What is Airbyte?',
        'a': 'An open-source ELT connector platform and alternative to Fivetran. 350+ connectors, self-hostable (Airbyte OSS) or fully managed (Airbyte Cloud). Uses a Connector Development Kit (CDK) for custom sources in any language. Preferred when you need unusual sources, cost control, or self-hosted infrastructure. Trades zero-ops convenience for flexibility.',
        'category': 'Data Integration & Ingestion Tools', 'group': ['Ingestion', 'ELT'], 'difficulty': 'Easy',
    },
    {
        'q': 'What is Debezium?',
        'a': 'An open-source CDC platform built on Kafka Connect. Reads database transaction logs and streams row-level changes (INSERT/UPDATE/DELETE) as events to Kafka topics. Supports PostgreSQL (WAL), MySQL (binlog), MongoDB, SQL Server, and Oracle. The standard tool for event-driven, real-time database-to-lake replication.',
        'category': 'Data Integration & Ingestion Tools', 'group': ['CDC', 'Streaming'], 'difficulty': 'Medium',
    },
    {
        'q': 'What is Reverse ETL?',
        'a': 'Moving data from a data warehouse back into operational tools (CRM, marketing platforms, support tools) — the reverse of traditional ETL direction. Tools: Census, Hightouch, Omnata. Example: syncing a churn-risk score from BigQuery back into Salesforce so sales reps can act on it directly. Bridges the gap between analytics and business operations.',
        'category': 'Data Integration & Ingestion Tools', 'group': ['Ingestion', 'ELT'], 'difficulty': 'Medium',
    },
    {
        'q': 'Comparison: Fivetran vs. Airbyte?',
        'a': '**Fivetran**: fully managed, 500+ vendor-maintained connectors, automatic schema migration, pricing by MAR — choose for reliability and minimal engineering overhead. **Airbyte**: open-source, self-hostable, CDK for custom sources, lower cost — choose for unusual sources, cost sensitivity, or self-hosted requirements. Both use an ELT pattern; Fivetran wins on ops ease, Airbyte wins on flexibility.',
        'category': 'Data Integration & Ingestion Tools', 'group': ['Ingestion', 'ELT'], 'difficulty': 'Medium',
    },

    # ── Networking & APIs ─────────────────────────────────────────────────────
    {
        'q': 'What is a REST API in a Data Engineering context?',
        'a': 'REST (Representational State Transfer) is the dominant pattern for web APIs. In DE, REST APIs are used to ingest data from SaaS sources (Stripe, Salesforce, HubSpot), interact with cloud services, and trigger pipeline runs. Key concepts: HTTP verbs (GET/POST/PUT/DELETE), status codes (200/404/429), authentication (API keys, OAuth 2.0), pagination, and rate limiting.',
        'category': 'Networking & APIs', 'group': ['APIs', 'Integration'], 'difficulty': 'Easy',
    },
    {
        'q': 'What is an API Rate Limit and how do you handle it in a pipeline?',
        'a': 'A cap on how many API requests a client can make per time window (e.g., 100 req/min). Exceeding it returns HTTP 429. Handling strategies: exponential backoff with jitter, respecting the `Retry-After` header, caching responses, batching requests, and efficient cursor-based pagination. Critical for reliable SaaS data ingestion at scale.',
        'category': 'Networking & APIs', 'group': ['APIs', 'Reliability'], 'difficulty': 'Medium',
    },
    {
        'q': 'What is gRPC and how does it compare to REST?',
        'a': 'A high-performance RPC framework from Google using Protocol Buffers (binary serialisation) instead of JSON. Much faster and lower-bandwidth than REST for service-to-service calls. In DE, used under the hood by Pub/Sub, BigQuery Storage API, and Kafka clients. Downside: not human-readable — harder to debug than REST/JSON. Prefer REST for external APIs; gRPC for high-throughput internal services.',
        'category': 'Networking & APIs', 'group': ['APIs', 'Protocols'], 'difficulty': 'Medium',
    },
    {
        'q': 'What is a Webhook?',
        'a': 'A push-based integration where a source system sends an HTTP POST to your endpoint when an event occurs, instead of you polling. Common in DE for event-driven pipeline triggers — e.g., Stripe sends a webhook on payment completion. Requires a publicly reachable endpoint and idempotent handling (webhooks may be delivered more than once due to retries).',
        'category': 'Networking & APIs', 'group': ['APIs', 'Integration'], 'difficulty': 'Easy',
    },

    # ── Databases (new types) ─────────────────────────────────────────────────
    {
        'q': 'What is a Time-Series Database?',
        'a': 'A database optimised for time-stamped, append-mostly data. Features: built-in compression for sequential numeric values, automatic downsampling (rollups), and fast time-range queries. Examples: InfluxDB, TimescaleDB (PostgreSQL extension), QuestDB. Use for IoT sensor data, application metrics, financial tick data — any dataset where time is always the primary query dimension.',
        'category': 'Databases', 'group': ['Databases', 'NoSQL'], 'difficulty': 'Medium',
    },
    {
        'q': 'What is Elasticsearch (and OpenSearch)?',
        'a': 'A distributed search and analytics engine built on Apache Lucene. Uses an inverted index for near-instant full-text search. AWS OpenSearch is the open-source fork. In DE: the \'E\' in the ELK Stack (Elasticsearch, Logstash, Kibana). Use for log ingestion/search, product search APIs, and operational analytics — not a replacement for a data warehouse for BI workloads.',
        'category': 'Databases', 'group': ['Databases', 'Search'], 'difficulty': 'Medium',
    },
    {
        'q': 'What is database replication?',
        'a': 'Copying data from a primary node to one or more replica nodes for redundancy and read scaling. **Primary-replica (async)**: writes to primary, replicas catch up — most common, risk of replica lag. **Synchronous**: replica confirms before primary returns — strong consistency, higher latency. **Multi-primary**: any node accepts writes, conflicts resolved — for geo-distributed writes. Foundational to RDS, PostgreSQL, MySQL, and cloud data warehouses.',
        'category': 'Databases', 'group': ['Databases', 'Architecture'], 'difficulty': 'Medium',
    },

    # ── Security & Privacy (modern auth) ──────────────────────────────────────
    {
        'q': 'What is OAuth 2.0 in a Data Engineering context?',
        'a': 'An authorisation framework letting applications access APIs on behalf of a user without storing their password. In DE, used by connectors (Fivetran, Airbyte) to access SaaS APIs (Salesforce, Google). Flow: app redirects to identity provider → user grants permission → provider issues short-lived access token + long-lived refresh token. Token sent as `Authorization: Bearer <token>` header.',
        'category': 'Security and Privacy', 'group': ['Security', 'Auth'], 'difficulty': 'Medium',
    },
    {
        'q': 'What is Row-Level Security (RLS) in a data warehouse?',
        'a': 'A feature restricting which rows a user can see in a table, enforced by the database engine rather than application code. Example: a sales rep queries `orders` but only sees rows for their region. Implemented via row access policies (Snowflake), row-level security (BigQuery), or row filters (Databricks Unity Catalog). Avoids maintaining separate tables or views per team.',
        'category': 'Security and Privacy', 'group': ['Security', 'Access Control'], 'difficulty': 'Medium',
    },
    {
        'q': 'What is data tokenization and how does it differ from masking?',
        'a': '**Tokenization**: replaces a sensitive value (e.g., card number) with a random token; the original is retrievable via a secure vault by authorised systems — referential integrity is preserved. **Masking**: replaces with a fake value (e.g., `****-1234`) — irreversible, used for dev/test environments. Use tokenization in production systems that process but must not expose PII; masking for non-production copies.',
        'category': 'Security and Privacy', 'group': ['Security', 'PII'], 'difficulty': 'Medium',
    },

    # ── Observability & Debugging (testing) ───────────────────────────────────
    {
        'q': 'What is integration testing in a data pipeline?',
        'a': 'Tests that verify multiple pipeline components work correctly together against real (or realistic) infrastructure — e.g., running a transformation against a staging database with representative data and asserting output values. Distinct from unit tests (isolated/mocked) and production (real scale). The most valuable layer for catching schema mismatches and cross-component logic errors.',
        'category': 'Observability & Debugging', 'group': ['Testing', 'Quality'], 'difficulty': 'Medium',
    },
    {
        'q': 'What is end-to-end (E2E) testing for data pipelines?',
        'a': 'A test validating the full pipeline — from source ingestion through transformation to final output — in a controlled environment with sample data. Slower than unit/integration tests but catches failures they miss (e.g., a schema change in the source breaking the final mart). Usually run against a full staging environment refresh before promoting changes to production.',
        'category': 'Observability & Debugging', 'group': ['Testing', 'Quality'], 'difficulty': 'Medium',
    },

    # ── Data Engineering Tools (orchestration depth) ──────────────────────────
    {
        'q': 'What is Prefect?',
        'a': 'A Python-native orchestration framework. Differentiators from Airflow: native async, first-class dynamic workflows (no static DAG required at import time), decorator-based API (`@flow`, `@task`), and a hybrid model where your code runs in your own infrastructure while Prefect Cloud handles only scheduling and observability metadata. Lower ops burden than self-hosted Airflow.',
        'category': 'Data Engineering Tools', 'group': ['Orchestration', 'Tools'], 'difficulty': 'Medium',
    },
    {
        'q': 'What is Dagster?',
        'a': 'A data orchestration platform built around software-defined assets — you declare what data assets your pipeline produces, not just what tasks run. Provides built-in lineage, a strongly-typed I/O model, and a unified asset catalog. Preferred when you want pipeline code and the data catalog to be a single system with tight observability. Strong typing catches errors at definition time.',
        'category': 'Data Engineering Tools', 'group': ['Orchestration', 'Tools'], 'difficulty': 'Medium',
    },
    {
        'q': 'Comparison: Airflow vs. Prefect vs. Dagster?',
        'a': '**Airflow**: task-centric DAGs, massive ecosystem, complex setup — the industry standard. **Prefect**: simpler Python API, dynamic workflows, hybrid cloud — best for Airflow migrations wanting less ops overhead. **Dagster**: asset-centric model, built-in lineage and observability — best when data catalog and pipeline must be unified. All are production-grade; the choice is philosophical (tasks vs. flows vs. assets).',
        'category': 'Data Engineering Tools', 'group': ['Orchestration', 'Tools'], 'difficulty': 'Hard',
    },
]

cards.extend(NEW_CARDS)
print(f'Added {len(NEW_CARDS)} new cards')

# ── 5. Assign module field ────────────────────────────────────────────────────
CATEGORY_TO_MODULE = {
    'Data Engineering Fundamentals':    'Foundations',
    'Data Modelling':                   'Foundations',
    'Analytics and Visualization':      'Foundations',
    'Databases':                        'Databases & Storage',
    'Open Table Formats':               'Databases & Storage',
    'Storage & Data Formats':           'Databases & Storage',
    'Big Data Technologies':            'Processing & Architecture',
    'Event-Driven Architectures':       'Processing & Architecture',
    'Computing Concepts':               'Processing & Architecture',
    'Cloud Computing and Platforms':    'Cloud & DevOps',
    'DevOps for Data Engineering':      'Cloud & DevOps',
    'Data Engineering Tools':           'Tools & Integration',
    'Data Integration & Ingestion Tools':'Tools & Integration',
    'Networking & APIs':                'Tools & Integration',
    'Observability & Debugging':        'Tools & Integration',
    'Programming & Automation':         'Programming & Security',
    'Security and Privacy':             'Programming & Security',
    'Emerging Topics':                  'Programming & Security',
}

unmatched = set()
for card in cards:
    cat = card.get('category', '')
    mod = CATEGORY_TO_MODULE.get(cat)
    if mod:
        card['module'] = mod
    else:
        unmatched.add(cat)

if unmatched:
    print(f'WARNING — no module for categories: {unmatched}')

de['modules_ordered'] = [
    'Foundations',
    'Databases & Storage',
    'Processing & Architecture',
    'Cloud & DevOps',
    'Tools & Integration',
    'Programming & Security',
]

# ── 6. Verify ─────────────────────────────────────────────────────────────────
de['cards'] = cards
final = len(cards)
print(f'\nFinal card count: {original_count} -> {final} ({final - original_count:+d})')

mods = {}
for c in cards:
    m = c.get('module', '(none)')
    mods[m] = mods.get(m, 0) + 1
print('\nCards per module:')
for m in de['modules_ordered']:
    print(f'  {mods.get(m,0):4d}  {m}')

cats = {}
for c in cards:
    cat = c.get('category', '(none)')
    cats[cat] = cats.get(cat, 0) + 1
print('\nCards per category:')
for cat, n in sorted(cats.items(), key=lambda x: -x[1]):
    print(f'  {n:4d}  {cat}')

with open('frontend/cards.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('\nDone.')
