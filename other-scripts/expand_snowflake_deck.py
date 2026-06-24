import json

with open('frontend/cards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def c(q, a, group, difficulty, module, cert=None):
    card = {"q": q, "a": a, "group": group, "difficulty": difficulty,
            "category": group, "module": module}
    if cert:
        card["certification"] = cert
    return card

new_cards = []

# ════════════════════════════════════════════════════════
# SNOWFLAKE 101 – extra cards
# ════════════════════════════════════════════════════════
M = "Snowflake 101"

new_cards += [
c("What is Snowsight?",
  "Snowflake's modern web-based UI (the successor to the Classic Console). It provides SQL worksheets, a query history viewer, database object explorer, dashboards, and admin screens for users, warehouses, and billing — all in the browser.",
  "Core Concepts","easy",M),

c("What is SnowSQL?",
  "The official command-line client for Snowflake. It connects to Snowflake over TLS, lets you run SQL interactively or in batch mode, and is the only client that supports the PUT and GET commands for transferring files to/from internal stages.",
  "Core Concepts","easy",M),

c("What are Snowflake worksheets?",
  "Named, saved SQL editing contexts in Snowsight. Each worksheet has its own role, warehouse, database, and schema context. Multiple worksheets can run independently in parallel. Worksheets can be organised into folders and shared with other users.",
  "Core Concepts","easy",M),

c("How does Snowflake handle SQL identifier case sensitivity?",
  "Unquoted identifiers are stored and compared in UPPERCASE. Double-quoted identifiers preserve exact case and are case-sensitive. Best practice: use unquoted (uppercase) identifiers unless you specifically need mixed-case names.",
  "Core Concepts","medium",M),

c("What is AUTOCOMMIT in Snowflake?",
  "Snowflake runs with AUTOCOMMIT = TRUE by default — every DML statement is automatically committed unless you explicitly start a transaction with BEGIN. You can disable AUTOCOMMIT at the session level to group statements into manual transactions.",
  "Core Concepts","medium",M),

c("What is the Information Schema in Snowflake?",
  "An ANSI-standard set of views inside every Snowflake database (INFORMATION_SCHEMA schema) that shows metadata about the objects in that database — tables, columns, views, stages, file formats, etc. Data reflects the current state of that database only.",
  "Core Concepts","medium",M),

c("What is ACCOUNT_USAGE in Snowflake and how does it differ from INFORMATION_SCHEMA?",
  "ACCOUNT_USAGE is a shared database (SNOWFLAKE.ACCOUNT_USAGE) with views covering the entire account — all databases, all warehouses, query history, login history, storage usage, etc. It has a latency of 45 minutes to 3 hours. INFORMATION_SCHEMA is per-database and near real-time but limited to that database's objects.",
  "Core Concepts","medium",M),

c("What does the SHOW command do in Snowflake?",
  "Lists objects of a given type visible to the current role: SHOW TABLES, SHOW WAREHOUSES, SHOW USERS, SHOW GRANTS TO ROLE my_role, etc. More convenient than querying INFORMATION_SCHEMA for a quick inventory; output can be queried with SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())).",
  "Core Concepts","easy",M),

c("What are constraints in Snowflake and are they enforced?",
  "Snowflake supports PRIMARY KEY, UNIQUE, FOREIGN KEY, and NOT NULL constraints in DDL for documentation and tooling compatibility. Only NOT NULL is enforced at runtime. PRIMARY KEY, UNIQUE, and FOREIGN KEY are informational only — Snowflake does not reject violating rows.",
  "Tables & Objects","medium",M),

c("What is the difference between a Secure View and a regular view in Snowflake?",
  "A Secure View hides its underlying definition from users who don't own it — the definition is not visible in SHOW VIEWS or INFORMATION_SCHEMA. Required when sharing views via Secure Data Sharing (regular views expose their SQL to data consumers).",
  "Tables & Objects","medium",M),

c("What is a Snowflake Pipe object?",
  "A named object that encapsulates a COPY INTO statement and a source stage. Snowpipe uses the pipe definition to load files as they arrive. The pipe stores the load history used to deduplicate file loads.",
  "Data Loading","medium",M),

c("What is the user stage vs. named internal stage?",
  "Every user automatically has a personal user stage (@~) — no creation needed, not shareable, tied to the user. A named internal stage (CREATE STAGE) is a standalone object that can be granted to roles and shared across users and processes. Preferred for production pipelines.",
  "Data Loading","medium",M),

c("What Snowflake data types are used for date and time?",
  "DATE (date only), TIME (time only), TIMESTAMP_NTZ (no timezone — stores as-is), TIMESTAMP_LTZ (local timezone — stores UTC, displays in session timezone), TIMESTAMP_TZ (stores offset with the value). TIMESTAMP is an alias for whichever variant the TIMESTAMP_TYPE_MAPPING session parameter specifies (default: NTZ).",
  "Tables & Objects","medium",M),

c("What is the VARIANT size limit in Snowflake?",
  "Each VARIANT value can be up to 16 MB when uncompressed. Individual objects or arrays that exceed this limit cannot be stored in a single VARIANT column — they must be split or truncated before loading.",
  "Semi-Structured Data","medium",M),

c("What is a Snowflake Alert?",
  "A named object that evaluates a condition on a schedule and sends a notification (via a notification integration — email, SNS, PagerDuty, etc.) when the condition is true. Used for data quality monitoring, pipeline failure detection, and threshold alerts.",
  "Core Concepts","medium",M),

c("What is the Snowflake Partner Ecosystem?",
  "A network of certified technology partners — BI tools (Tableau, Looker, Power BI), ETL/ELT tools (dbt, Fivetran, Matillion, Airbyte), data catalogues (Alation, Atlan), and security tools — that have native, certified connectors to Snowflake. Listed on the Snowflake Partner Connect page.",
  "Core Concepts","easy",M),

c("What is a Notification Integration in Snowflake?",
  "A Snowflake object that connects Snowflake to an external messaging service (AWS SNS, Azure Event Grid, GCP Pub/Sub, email). Used by Alerts, Snowpipe error notifications, and Tasks to send messages outside Snowflake.",
  "Core Concepts","medium",M),
]


# ════════════════════════════════════════════════════════
# SNOWFLAKE CORE – extra cards
# ════════════════════════════════════════════════════════
M = "Snowflake Core"

new_cards += [
c("What is an Event Table in Snowflake?",
  "A special table that stores log and trace events emitted from Snowflake handler code (Python UDFs, stored procedures, Snowpark). Replaces the need for external logging — you query the event table with SQL to see errors, log messages, and OpenTelemetry spans from your code.",
  "Architecture","hard",M),

c("What are External Functions in Snowflake?",
  "User-defined functions that call an external HTTPS endpoint (an API Gateway backed by AWS Lambda, Azure Functions, or GCP Cloud Functions). The SQL query passes rows to the external service and receives results back. Useful for enrichment, ML inference, or third-party API calls.",
  "Architecture","hard",M),

c("What is the Query Acceleration Service (QAS) in Snowflake?",
  "A serverless feature that offloads parts of an eligible query (large scans, outlier partitions) to additional serverless compute rather than requiring you to upsize the warehouse. Useful for queries with variable data skew. Enabled per-warehouse with ENABLE_QUERY_ACCELERATION = TRUE.",
  "Performance","hard",M),

c("What is a Snowflake Budget?",
  "A newer (2023+) account-level spending control object that sets a monthly credit spending limit for a group of Snowflake objects or the whole account. More granular than Resource Monitors — Budgets can monitor serverless feature costs (clustering, Tasks, Snowpipe) that Resource Monitors cannot.",
  "Performance","hard",M),

c("What are Future Grants in Snowflake?",
  "A privilege grant applied to all future objects of a type in a schema or database: GRANT SELECT ON FUTURE TABLES IN SCHEMA mydb.myschema TO ROLE analyst. New tables created after the grant automatically receive the privilege — no need to re-grant on each new object.",
  "Security","medium",M),

c("What is GRANT OWNERSHIP in Snowflake and when would you use it?",
  "Transfers ownership of an object from one role to another: GRANT OWNERSHIP ON TABLE orders TO ROLE data_engineer. Needed when migrating objects between teams, or when the creating role should not retain long-term ownership. Only the current owner or ACCOUNTADMIN can transfer ownership.",
  "Security","medium",M),

c("What is External Tokenization in Snowflake?",
  "A column-level security pattern where sensitive values are replaced with tokens by an external vault (e.g., Protegrity, Voltage) before landing in Snowflake. A masking policy calls an External Function to de-tokenize values at query time for authorised users. Data at rest is never in plaintext.",
  "Security","hard",M),

c("What is Data Classification in Snowflake?",
  "A system that automatically scans column values and metadata and suggests privacy tags (e.g., NAME, EMAIL, PHONE, SSN) that can then be applied via Object Tags. Helps teams identify PII/sensitive data without manually reviewing every column.",
  "Security","hard",M),

c("What is a Snowflake Network Rule?",
  "A newer (2023+) object that defines a set of IP ranges or VPC IDs as an allowed or blocked group. Network Rules are referenced by Network Policies, replacing the flat allowed/blocked IP list with reusable, composable rule objects.",
  "Security","hard",M),

c("What are Iceberg Tables in Snowflake?",
  "Tables that store data in the Apache Iceberg open-table format on customer-managed cloud storage, while using Snowflake as the query engine. Enables a data lakehouse pattern: open format data readable by other engines (Spark, Flink), governed and queried through Snowflake.",
  "Architecture","hard",M),

c("What is Snowflake Cortex?",
  "A suite of serverless AI/ML features built into Snowflake: Cortex LLM Functions (COMPLETE, SUMMARIZE, TRANSLATE, SENTIMENT, CLASSIFY_TEXT using hosted LLMs), Cortex ML Functions (FORECAST, ANOMALY_DETECTION using AutoML), and Cortex Search (vector search). Runs entirely within Snowflake — no data leaves the platform.",
  "Architecture","hard",M),

c("What is the RESULT_SCAN function in Snowflake?",
  "Returns the output of a previous query as a table using its query ID: SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())). Useful for processing SHOW command output or inspecting results of VALIDATE statements in subsequent SQL.",
  "Architecture","medium",M),

c("What is the difference between TIMESTAMP_NTZ, TIMESTAMP_LTZ, and TIMESTAMP_TZ?",
  "TIMESTAMP_NTZ — stores date/time with no timezone; displayed exactly as stored. TIMESTAMP_LTZ — stores as UTC; displayed in the session's local timezone (TIMEZONE parameter). TIMESTAMP_TZ — stores the value plus an explicit UTC offset; preserves the original timezone information.",
  "Architecture","medium",M),

c("What is a Stored Procedure owner's rights vs. caller's rights in Snowflake?",
  "Owner's rights (default): the procedure runs with the privileges of the role that owns it, not the caller. The caller only needs EXECUTE PRIVILEGE — they can't see or access objects they don't have direct grants to. Caller's rights: the procedure runs with the caller's role — useful when you want the procedure to respect the caller's access level.",
  "Security","hard",M),

c("What is the difference between a Task with a CRON schedule and a serverless Task?",
  "A warehouse-based Task runs on a specified virtual warehouse (you pay for warehouse time even if the task is fast). A serverless Task (WAREHOUSE = omitted, USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE specified) uses Snowflake-managed compute — you pay per compute-second used, and Snowflake auto-sizes based on prior run history.",
  "Streams & Tasks","hard",M),

c("What is a Snowflake SEQUENCE and what guarantees does it make?",
  "A sequence generates unique integer values with NEXTVAL. Values are guaranteed unique and monotonically increasing, but NOT gap-free — gaps can occur due to rollbacks, multi-session access, or batch allocation. Do not rely on sequences for dense, contiguous numbering.",
  "Architecture","medium",M),

c("What is the difference between a Materialized View and a Dynamic Table in Snowflake?",
  "Materialized Views are automatically refreshed by Snowflake when base data changes, but have significant limitations: no JOINs on non-shared-micropartitions, no subqueries, Enterprise+ only. Dynamic Tables support full SQL (JOINs, CTEs, aggregations), have configurable lag, and can form dependency chains. Dynamic Tables are the recommended modern approach.",
  "Architecture","hard",M),
]


# ════════════════════════════════════════════════════════
# SNOWPRO CORE – expanded
# ════════════════════════════════════════════════════════
M = "SnowPro Core"
CERT = "snowpro core"

new_cards += [
# Domain 1: Architecture
c("What is the difference between an internal named stage and a user/table stage?",
  "User stage (@~) and table stage (@%tablename) are auto-created, not grantable, and tied to a user or table. Named stages (CREATE STAGE) are independent objects, can be granted to roles, support custom file format defaults, and are the recommended approach for production pipelines.",
  "Domain 1: Architecture","medium",M,CERT),

c("What is columnar storage and why does Snowflake use it?",
  "Columnar storage organises data by column rather than by row. This means analytic queries that read only a few columns scan far less data. It also enables much higher compression ratios within a column (similar values together). Snowflake's micro-partitions are stored in a compressed columnar format (based on PAX/hybrid).",
  "Domain 1: Architecture","medium",M,CERT),

c("What happens to old micro-partitions when data is updated or deleted in Snowflake?",
  "Micro-partitions are immutable. An UPDATE or DELETE creates new micro-partitions with the changed/surviving rows and marks the old micro-partitions as deleted. The old partitions are retained for the Time Travel retention period, then moved to Fail-Safe, and eventually purged.",
  "Domain 1: Architecture","hard",M,CERT),

c("What is the Continuous Data Protection (CDP) lifecycle in Snowflake?",
  "The layered protection Snowflake provides automatically: 1. Operational storage (current data). 2. Time Travel (user-accessible historical queries/restores, up to 90 days). 3. Fail-Safe (7-day Snowflake-managed emergency recovery after Time Travel). No additional configuration required.",
  "Domain 1: Architecture","medium",M,CERT),

c("How many databases can a single Snowflake account have?",
  "There is no documented hard limit on the number of databases per account. Snowflake accounts can contain thousands of databases, schemas, and tables. Practical limits are driven by governance and cost, not platform constraints.",
  "Domain 1: Architecture","easy",M,CERT),

c("Can a Snowflake Virtual Warehouse span multiple cloud regions?",
  "No. A virtual warehouse runs entirely within the cloud region of the Snowflake account. Cross-region compute is not possible within a single warehouse. Cross-region data access requires replication.",
  "Domain 1: Architecture","medium",M,CERT),

c("What types of objects can be cloned in Snowflake?",
  "Databases, schemas, tables (permanent, temporary, transient), streams, sequences, file formats, stages (named internal), tasks, and pipes. Cloning a schema or database recursively clones all supported child objects.",
  "Domain 1: Architecture","medium",M,CERT),

c("What is the relationship between a Snowflake account and an organisation?",
  "An Organisation is an optional grouping of multiple Snowflake accounts under one entity. It enables cross-account replication, account-level transfers, and consolidated usage reporting in ORGANISATION_USAGE. A single account can exist without an organisation.",
  "Domain 1: Architecture","medium",M,CERT),

c("What is a Snowflake Worksheet's context and why does it matter?",
  "Each worksheet has a role, warehouse, database, and schema set as its context. SQL runs with that role's privileges, against that database/schema (used as the default for unqualified object names), using that warehouse. Changing context mid-session affects all subsequent statements in that worksheet.",
  "Domain 1: Architecture","easy",M,CERT),

c("What is INFORMATION_SCHEMA.QUERY_HISTORY and what does it contain?",
  "A table function in every database's INFORMATION_SCHEMA that returns query history for the current user (or all users if ACCOUNTADMIN/SYSADMIN). Returns up to 7 days of history. For longer history, use SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY (up to 365 days, ~45 min latency).",
  "Domain 1: Architecture","hard",M,CERT),

# Domain 2: Security
c("What is the ORGADMIN role in Snowflake?",
  "A special account-level role (granted only by Snowflake) that can manage the Organisation — create accounts, view organisation-level usage, and enable cross-account features. It is separate from ACCOUNTADMIN and typically held by only one account per organisation.",
  "Domain 2: Security","hard",M,CERT),

c("What is a Snowflake Session Policy?",
  "An object that controls session timeout behaviour — idle timeout and maximum session duration. Applied at user or account level. Useful for enforcing inactivity-based session termination for compliance.",
  "Domain 2: Security","hard",M,CERT),

c("What is the difference between GRANT PRIVILEGE and GRANT ROLE?",
  "GRANT PRIVILEGE (e.g., GRANT SELECT ON TABLE t TO ROLE r) gives a role the ability to perform a specific action on a specific object. GRANT ROLE (GRANT ROLE analyst TO ROLE manager) adds a role to another role's or user's role hierarchy — the grantee inherits all privileges of the granted role.",
  "Domain 2: Security","medium",M,CERT),

c("What does GRANT ... WITH GRANT OPTION do?",
  "Allows the grantee role to further grant that privilege to other roles. Without WITH GRANT OPTION, a role can use a privilege but cannot re-grant it. Only the object owner or ACCOUNTADMIN can typically re-grant without this option.",
  "Domain 2: Security","hard",M,CERT),

c("What is a Snowflake Password Policy?",
  "An object applied at account or user level that enforces password rules: minimum length, required character types, history (can't reuse last N passwords), lockout after N failures, and expiry. Helps meet compliance requirements without relying on an external IdP.",
  "Domain 2: Security","medium",M,CERT),

c("How do you revoke a privilege in Snowflake?",
  "REVOKE SELECT ON TABLE orders FROM ROLE analyst; If the privilege was granted WITH GRANT OPTION and the role has re-granted it, adding CASCADE revokes downstream: REVOKE SELECT ON TABLE orders FROM ROLE analyst CASCADE;",
  "Domain 2: Security","medium",M,CERT),

c("What is Snowflake's approach to MFA?",
  "Snowflake supports TOTP-based MFA (via Duo Security or compatible apps). Users enrol through their account settings. MFA can be required by an admin via an Authentication Policy. MFA is enforced at login — once authenticated, the session is trusted for its duration.",
  "Domain 2: Security","medium",M,CERT),

c("What is an Authentication Policy in Snowflake?",
  "An object that defines what authentication methods are allowed for users or the account: password only, MFA required, key-pair only, SSO only, or combinations. Applied at account or user level. Overrides individual user settings when applied at account level.",
  "Domain 2: Security","hard",M,CERT),

c("What is OAuth in the context of Snowflake?",
  "Snowflake supports OAuth 2.0 for client authentication via Snowflake OAuth (built-in) or External OAuth (using Okta, Azure AD, or a custom IdP as the authorisation server). Clients obtain an access token and use it instead of a password — enabling SSO for tools like Tableau and Power BI without sharing credentials.",
  "Domain 2: Security","hard",M,CERT),

c("What privileges are required to create a table in Snowflake?",
  "The current role must have: CREATE TABLE privilege on the target schema, and USAGE privilege on the database and schema. Without all three, the CREATE TABLE statement will fail.",
  "Domain 2: Security","medium",M,CERT),

c("What is the purpose of the SECURITYADMIN role vs. creating a custom security admin role?",
  "SECURITYADMIN is a built-in superuser that can manage all grants in the account. For large organisations, it is safer to create custom security roles that can only manage grants on specific databases or schemas — limiting blast radius if a security admin account is compromised.",
  "Domain 2: Security","hard",M,CERT),

c("What is a Snowflake Tag and how is it attached to an object?",
  "CREATE TAG sensitivity; — creates the tag. ALTER TABLE customers MODIFY COLUMN email SET TAG sensitivity = 'PII'; — attaches it. Tags can be applied to accounts, databases, schemas, tables, columns, views, warehouses, and other objects. Query tag assignments via SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES.",
  "Domain 2: Security","medium",M,CERT),

# Domain 3: Performance
c("What is an EXPLAIN plan in Snowflake and how do you generate one?",
  "EXPLAIN <query> returns the logical and physical execution plan as a set of rows without running the query. Also available as JSON with EXPLAIN USING JSON. Use it to understand how Snowflake will execute a query, what joins it will use, and whether partition pruning is expected.",
  "Domain 3: Performance","hard",M,CERT),

c("What causes a CartesianJoin warning in a Snowflake Query Profile?",
  "A JOIN with no ON condition or a condition that never eliminates rows — producing N × M output rows. Typically a mistake. Snowflake flags it in the query profile. Fix by adding the correct join predicate.",
  "Domain 3: Performance","hard",M,CERT),

c("What is 'exploding join' in Snowflake and how do you detect it?",
  "A join where many rows on both sides match, multiplying output rows far beyond the input. Visible in Query Profile as a massive increase in row count between the Join operator's inputs and output. Fix by adding more selective join conditions or filtering before the join.",
  "Domain 3: Performance","hard",M,CERT),

c("How does the result cache save warehouse costs?",
  "If a query hits the result cache, Snowflake returns the cached result without spinning up a warehouse or consuming a single credit. The result cache is checked by the Cloud Services Layer before the query is dispatched to a warehouse. Only the metadata check (a small Cloud Services cost) is incurred.",
  "Domain 3: Performance","medium",M,CERT),

c("When does Cloud Services billing kick in for Snowflake?",
  "Cloud Services usage is free up to 10% of the daily compute credits consumed by virtual warehouses. Usage above that 10% threshold is billed separately. This means accounts that run no (or very few) warehouse queries can incur Cloud Services charges for metadata-heavy operations.",
  "Domain 3: Performance","hard",M,CERT),

c("What is the effect of increasing warehouse size on a query that is already fast?",
  "Usually none — the query may finish slightly faster but is already likely limited by network I/O or the 60-second minimum billing. Upsizing is only beneficial when the query profile shows spilling or a CPU-bound operator consuming most of the time.",
  "Domain 3: Performance","medium",M,CERT),

c("What is the Query Acceleration Service and which queries benefit from it?",
  "A serverless feature that dynamically offloads parts of a query (typically large partition scans with outliers) to additional compute beyond the warehouse. Benefits queries with highly variable partition sizes or data skew. Enabled per warehouse; charged per serverless compute second used.",
  "Domain 3: Performance","hard",M,CERT),

c("What does SHOW WAREHOUSES reveal about warehouse performance?",
  "SHOW WAREHOUSES returns each warehouse's state (STARTED/SUSPENDED), size, auto-suspend setting, running/queued query counts, and cluster count. The QUEUED column indicates concurrency pressure — if queries are queuing, the warehouse may need more clusters or a larger size.",
  "Domain 3: Performance","medium",M,CERT),

# Domain 4: Data Loading
c("What is the recommended file size for bulk loading into Snowflake?",
  "100 MB to 250 MB per file (compressed) is the sweet spot. Files this size allow Snowflake to parallelise loading across warehouse nodes efficiently. Very large single files (GBs) are loaded sequentially; very small files (KBs) incur too much overhead per file.",
  "Domain 4: Data Loading","medium",M,CERT),

c("What is MATCH_BY_COLUMN_NAME in COPY INTO?",
  "An option (MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE or SENSITIVE) for semi-structured file formats (Parquet, Avro, JSON) that maps source file fields to target table columns by name rather than position. Prevents column misalignment when files have a different column order than the table.",
  "Domain 4: Data Loading","hard",M,CERT),

c("How can you apply a transformation to data during COPY INTO?",
  "Include a SELECT statement in the COPY INTO: COPY INTO orders (id, amount) FROM (SELECT $1, $2::FLOAT * 1.1 FROM @my_stage). You can rename columns, apply functions, filter rows, or reorder columns at load time without a separate transformation step.",
  "Domain 4: Data Loading","hard",M,CERT),

c("What is the deduplication window for COPY INTO file metadata?",
  "Snowflake tracks file load metadata (file path + ETag) for 64 days. If COPY INTO encounters a file already loaded within that window, it skips it. After 64 days the metadata expires and the file can be reloaded. Use FORCE = TRUE to override this check.",
  "Domain 4: Data Loading","hard",M,CERT),

c("What does COPY INTO return when VALIDATION_MODE = 'RETURN_ERRORS'?",
  "A result set listing every row in every staged file that would fail to load, including the file name, row number, error message, and rejected line content. No data is actually loaded. Use this to diagnose format issues before committing a production load.",
  "Domain 4: Data Loading","medium",M,CERT),

c("How do you monitor Snowpipe load history?",
  "Query INFORMATION_SCHEMA.LOAD_HISTORY (per-database, 14-day history, near real-time) or SNOWFLAKE.ACCOUNT_USAGE.LOAD_HISTORY (account-wide, 365 days, ~45 min latency). Also use SYSTEM$PIPE_STATUS('pipe_name') for the current queue state and last ingestion timestamp.",
  "Domain 4: Data Loading","hard",M,CERT),

c("What is the difference between a CSV file format with FIELD_OPTIONALLY_ENCLOSED_BY and FIELD_DELIMITER?",
  "FIELD_DELIMITER sets the character separating columns (default: comma). FIELD_OPTIONALLY_ENCLOSED_BY sets the character that optionally wraps field values — commonly a double-quote — so delimiters inside quoted fields are not treated as column boundaries.",
  "Domain 4: Data Loading","medium",M,CERT),

c("What is a Storage Integration and why is it preferred over access key credentials in stages?",
  "A Storage Integration stores the IAM role ARN (AWS), service account (GCP), or service principal (Azure) needed to access cloud storage. It is a Snowflake account-level object — credentials are managed centrally. Stage definitions reference the integration by name; no secret keys are stored in the stage or in SQL. Rotating credentials requires updating only the integration.",
  "Domain 4: Data Loading","medium",M,CERT),

c("What does STRIP_OUTER_ARRAY = TRUE do when loading JSON?",
  "Tells Snowflake to strip the top-level array brackets from the JSON file and load each element of the array as a separate row. Without it, the entire array is loaded as a single VARIANT value in one row. Use it when your JSON file is a JSON array of records rather than one record per line (newline-delimited JSON).",
  "Domain 4: Data Loading","hard",M,CERT),

# Domain 5: Transformations
c("What is a UDTF (User-Defined Table Function) in Snowflake?",
  "A UDF that returns a table instead of a scalar value. Called with TABLE() in a FROM clause: SELECT * FROM TABLE(my_udtf(arg)). Useful for complex transformations that produce multiple output rows per input row (similar to FLATTEN but custom logic).",
  "Domain 5: Transformations","hard",M,CERT),

c("What languages can Snowflake Stored Procedures be written in?",
  "JavaScript, Python, Java, Scala, and Snowflake Scripting (a SQL-based procedural language with BEGIN/END blocks, variables, loops, and conditionals). Snowflake Scripting is the recommended approach for pure SQL/DDL orchestration.",
  "Domain 5: Transformations","medium",M,CERT),

c("What is Snowflake Scripting?",
  "A procedural extension to Snowflake SQL that adds: variable declarations, IF/ELSIF/ELSE, FOR loops, WHILE loops, LOOP with EXIT WHEN, cursors, EXCEPTION handling, and RETURN. Used in stored procedures and anonymous blocks (EXECUTE IMMEDIATE / BEGIN...END).",
  "Domain 5: Transformations","hard",M,CERT),

c("What is a multi-table INSERT in Snowflake?",
  "INSERT ALL / INSERT FIRST — inserts rows from a single SELECT into multiple target tables in one statement. INSERT ALL sends each row to every matching WHEN clause; INSERT FIRST stops at the first matching WHEN clause per row.",
  "Domain 5: Transformations","hard",M,CERT),

c("How do you perform an upsert in Snowflake?",
  "Use MERGE INTO: MERGE INTO target t USING source s ON t.id = s.id WHEN MATCHED THEN UPDATE SET ... WHEN NOT MATCHED THEN INSERT .... Also possible with INSERT OVERWRITE for full-partition replacement patterns, but MERGE is the standard upsert.",
  "Domain 5: Transformations","medium",M,CERT),

c("What is the IFF function in Snowflake?",
  "A shorthand conditional: IFF(condition, true_value, false_value). Equivalent to CASE WHEN condition THEN true_value ELSE false_value END. Cleaner for simple boolean conditions.",
  "Domain 5: Transformations","easy",M,CERT),

c("What is the DECODE function in Snowflake?",
  "DECODE(expr, search1, result1, search2, result2, ..., default) — returns result_N where expr matches search_N; returns default if no match. Equivalent to a CASE equality check. Also handles NULL equality (unlike CASE WHEN expr = NULL).",
  "Domain 5: Transformations","medium",M,CERT),

c("What are the DATEADD and DATEDIFF functions in Snowflake?",
  "DATEADD(unit, amount, date) adds an interval to a date/timestamp. DATEDIFF(unit, date1, date2) returns the difference in the specified unit. Units include year, month, week, day, hour, minute, second, millisecond. DATE_TRUNC(unit, date) truncates to the start of a period.",
  "Domain 5: Transformations","easy",M,CERT),

c("What is a window function and what clauses does it require?",
  "A function that computes a result across a set of rows related to the current row without collapsing them into a single output row. Requires OVER(): OVER(PARTITION BY col ORDER BY col ROWS BETWEEN ...). Examples: ROW_NUMBER(), RANK(), LAG(), LEAD(), SUM() OVER, AVG() OVER.",
  "Domain 5: Transformations","medium",M,CERT),

c("What is the QUALIFY clause and why is it useful?",
  "QUALIFY filters on the result of a window function in the same SELECT, without needing a subquery: SELECT id, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn FROM employees QUALIFY rn = 1; — returns the highest-paid employee per department. Cleaner than wrapping in a subquery.",
  "Domain 5: Transformations","medium",M,CERT),

c("What is a recursive CTE in Snowflake?",
  "A CTE that references itself to process hierarchical or graph data: WITH RECURSIVE cte AS (base_case UNION ALL recursive_step). Snowflake supports recursive CTEs with a default recursion depth limit (configurable). Useful for org charts, product hierarchies, or graph traversals.",
  "Domain 5: Transformations","hard",M,CERT),

c("What is the CONNECT BY clause in Snowflake?",
  "An Oracle-style hierarchical query syntax alternative to recursive CTEs. SELECT ... FROM table CONNECT BY PRIOR id = parent_id START WITH parent_id IS NULL. Snowflake supports it for compatibility, though recursive CTEs are more portable.",
  "Domain 5: Transformations","hard",M,CERT),

# Domain 6: Data Protection and Sharing
c("How much does Time Travel storage cost in Snowflake?",
  "Time Travel data (old micro-partitions retained for historical queries) is charged at the same rate as regular storage. A table with 90-day Time Travel can cost up to 90× more storage than a table with 0-day retention. Transient tables avoid this by having 0-day Fail-Safe and 0–1 day Time Travel.",
  "Domain 6: Data Sharing","medium",M,CERT),

c("Can you query a cloned table's historical data before the clone was created?",
  "Yes, if the clone was created from a specific point in time within the Time Travel window. The clone inherits Time Travel history only back to when it was created (or the point-in-time it was cloned from). It does not inherit the original table's pre-clone history.",
  "Domain 6: Data Sharing","hard",M,CERT),

c("Who pays for compute when a consumer queries a Snowflake data share?",
  "The consumer pays — their own virtual warehouse executes the query against the provider's data. The provider pays only for storage. This is a key advantage of Snowflake sharing: providers bear no compute cost from consumer queries.",
  "Domain 6: Data Sharing","medium",M,CERT),

c("What is a Secure Materialised View and when is it required for sharing?",
  "A materialised view with SECURE keyword that hides the view definition and underlying table structure from the consumer. Required when sharing via a Data Share if you don't want to expose the source tables or view SQL to the consumer.",
  "Domain 6: Data Sharing","hard",M,CERT),

c("What is the UNDROP command in Snowflake?",
  "Restores a dropped object (table, schema, database) within its Time Travel retention window: UNDROP TABLE orders; UNDROP SCHEMA my_schema; If multiple objects with the same name were dropped and re-created, UNDROP restores the most recently dropped one.",
  "Domain 6: Data Sharing","easy",M,CERT),

c("What happens to Time Travel data when you increase a table's DATA_RETENTION_TIME?",
  "The change applies going forward. Historical data already outside the previous retention window has been purged and cannot be recovered by extending the window. Only data within the new, longer window from the change point onward is retained.",
  "Domain 6: Data Sharing","hard",M,CERT),

c("Can you share a Snowflake table across different cloud providers (e.g., AWS to Azure)?",
  "Yes, via Cross-Cloud Auto-Fulfillment (a Marketplace feature) which automatically replicates the data to the consumer's cloud/region. Standard Secure Data Sharing requires both accounts to be in the same cloud provider and region. For cross-cloud/cross-region, either replicate first or use Marketplace with auto-fulfillment.",
  "Domain 6: Data Sharing","hard",M,CERT),
]


# ════════════════════════════════════════════════════════
# SNOWPRO DATA ENGINEER – expanded
# ════════════════════════════════════════════════════════
M = "SnowPro Data Engineer"
CERT = "snowpro advanced data engineer"

new_cards += [
c("What is the Snowflake Connector for Python?",
  "An official Python library (snowflake-connector-python) that provides a DB-API 2.0 compliant interface to Snowflake. Supports cursor-based query execution, bulk loading via PUT/COPY, key-pair authentication, and result fetching as pandas DataFrames. The foundation of Snowpark for Python.",
  "Data Ingestion","medium",M,CERT),

c("What is the Snowflake JDBC/ODBC driver used for?",
  "Allows BI tools, ETL tools, and custom applications to connect to Snowflake using standard database interfaces. Supports all standard SQL operations. Configuration requires the account identifier, warehouse, database, schema, role, and credentials.",
  "Data Ingestion","medium",M,CERT),

c("How does the Snowflake Spark Connector differ from the Kafka Connector?",
  "The Spark Connector integrates Snowflake with Apache Spark — enabling Spark DataFrames to read/write Snowflake tables and pushing computation to Snowflake where possible. The Kafka Connector is a Kafka Connect plugin that streams Kafka topic messages into Snowflake tables via Snowpipe or direct inserts. They serve different pipeline patterns.",
  "Data Ingestion","hard",M,CERT),

c("What is an External Stage with directory table and how is it used in a pipeline?",
  "An external stage pointing to cloud storage plus a REFRESH of its directory table makes file metadata queryable via TABLE(@stage). A pipeline can JOIN the directory table against a load-tracking table to find only new files, then issue targeted COPY INTO commands for those files only.",
  "Data Ingestion","hard",M,CERT),

c("What is INFER_SCHEMA in Snowflake?",
  "A table function that inspects staged semi-structured files (Parquet, Avro, ORC, JSON, CSV) and returns the inferred column names, types, and nullability. Output can be fed into CREATE TABLE ... USING TEMPLATE to auto-create a matching table without manually defining the schema.",
  "Data Ingestion","hard",M,CERT),

c("What is ENABLE_SCHEMA_EVOLUTION and what risk does it carry?",
  "When TRUE on a table, COPY INTO automatically ADDs new columns found in source files. Risk: unexpected source schema changes (a renamed column, a new field from a different data source) will automatically alter the production table, potentially breaking downstream queries that rely on a fixed schema.",
  "Data Ingestion","hard",M,CERT),

c("How would you implement exactly-once semantics when loading from Kafka to Snowflake?",
  "The Snowflake Kafka Connector uses offset tracking: after successfully writing a batch to Snowflake (via Snowpipe or INSERT), it commits the Kafka offset. On failure, it replays from the last committed offset. Because Snowflake deduplicates by file metadata (for Snowpipe) or by MERGE key, replayed messages don't duplicate rows.",
  "Data Ingestion","hard",M,CERT),

c("What is the difference between Snowpipe auto-ingest and REST API ingest?",
  "Auto-ingest (AUTO_INGEST = TRUE) uses cloud event notifications (SQS for S3, Event Grid for Azure, Pub/Sub for GCP) to trigger Snowpipe automatically when files land. REST API ingest requires the pipeline to explicitly call Snowpipe's insertFiles endpoint with file paths. REST API suits cases where event notifications aren't available or you need programmatic control.",
  "Data Ingestion","hard",M,CERT),

c("What is a Snowflake Task's error-handling behaviour?",
  "By default, a failed task run (exception in the SQL/procedure) suspends the task after a configurable number of consecutive failures (SUSPEND_TASK_AFTER_NUM_FAILURES, default 10 for serverless, configurable). Child tasks in a DAG are skipped if their parent fails. Use Snowflake Alerts or TASK_HISTORY to detect and notify on failures.",
  "Streams & Tasks","hard",M,CERT),

c("What is TASK_HISTORY and how do you query it?",
  "INFORMATION_SCHEMA.TASK_HISTORY() table function (last 7 days, near real-time) or SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY view (365 days, ~45 min latency). Returns task name, run state, start/end time, error message, and query ID for each run. Useful for monitoring pipeline SLAs.",
  "Streams & Tasks","medium",M,CERT),

c("How do you backfill a Dynamic Table?",
  "ALTER DYNAMIC TABLE my_table REFRESH; triggers an immediate full or incremental refresh. For a full recompute from scratch (e.g., after changing the definition), you can DROP and recreate the Dynamic Table, which re-initialises from the current source data.",
  "Streams & Tasks","hard",M,CERT),

c("What is the DOWNSTREAM keyword in Dynamic Table TARGET_LAG?",
  "TARGET_LAG = 'DOWNSTREAM' tells Snowflake to refresh this Dynamic Table only when a downstream Dynamic Table that depends on it requests a refresh. It removes the fixed lag from intermediate tables in a dependency chain, letting the leaf's lag drive the whole pipeline.",
  "Streams & Tasks","hard",M,CERT),

c("What are the performance tuning options for a Snowflake Task that runs heavy SQL?",
  "Switch to a serverless task (Snowflake auto-sizes compute). If using a warehouse-based task, size the warehouse appropriately. Add AFTER to chain the task only when upstream is ready. Use SYSTEM$STREAM_HAS_DATA() to skip runs when there's nothing to process. Partition MERGE keys on the target table's clustering key.",
  "Streams & Tasks","hard",M,CERT),

c("What is an append-only stream and how does it differ in performance from a standard stream?",
  "Append-only streams track only INSERT operations, incurring lower storage overhead because they don't need to store before/after row images for UPDATEs and DELETEs. Consuming an append-only stream is faster when the source table is insert-only (e.g., event log, Snowpipe landing table).",
  "Streams & Tasks","medium",M,CERT),

c("How do you reset a Snowflake Stream's offset?",
  "You cannot directly reset a stream's offset. Options: (1) Drop and recreate the stream (offset resets to current). (2) Create a new stream at a historical point using AT/BEFORE (if within Time Travel window): CREATE STREAM my_stream ON TABLE my_table AT(TIMESTAMP => ...).",
  "Streams & Tasks","hard",M,CERT),

c("What are Snowflake External Functions and what are their latency implications?",
  "External Functions invoke remote HTTPS endpoints (via API Gateway + Lambda/Azure Functions/GCP Functions) during query execution. Each batch of rows is sent as an HTTP request. Latency is much higher than native UDFs — suitable for enrichment or scoring APIs that can't be brought into Snowflake, but not for high-throughput transformations.",
  "Data Ingestion","hard",M,CERT),

c("What is the Snowflake dbt integration and how does it work?",
  "dbt (data build tool) connects to Snowflake via the dbt-snowflake adapter using a profile configuration (account, warehouse, database, schema, role, credentials). dbt compiles SQL models into COPY GRANTS or CREATE TABLE/VIEW statements and runs them against Snowflake. Snowflake-specific features like CLUSTER BY and dynamic materializations are configurable via dbt configs.",
  "Data Ingestion","medium",M,CERT),

c("What is COPY_HISTORY in ACCOUNT_USAGE and how long does it retain data?",
  "SNOWFLAKE.ACCOUNT_USAGE.COPY_HISTORY records every COPY INTO operation (bulk and Snowpipe) account-wide, retaining up to 365 days. Columns include: file name, table name, status, rows loaded, rows parsed, errors, and first/last error messages. Essential for auditing and debugging data load issues.",
  "Data Ingestion","medium",M,CERT),

c("What is a Vectorized (Batch) Python UDF in Snowflake?",
  "A Python UDF decorated with @udf(packages=['pandas']) that receives and returns pandas Series/DataFrames instead of scalar values. Vectorized UDFs are significantly faster than row-by-row Python UDFs because they process batches of rows in a single Python call, reducing per-row interpreter overhead.",
  "Snowpark","hard",M,CERT),

c("What is Snowpark ML and what does it enable?",
  "A Snowpark library extension for machine learning. Provides: a scikit-learn-compatible Preprocessing API that runs in Snowflake, a Model Registry (store, version, deploy ML models), and ML Functions (FORECAST, ANOMALY_DETECTION) that apply pre-built models without writing Python. Keeps ML compute and data in Snowflake.",
  "Snowpark","hard",M,CERT),

c("How does Snowpark for Python differ from running Python outside Snowflake?",
  "Snowpark for Python pushes computation to Snowflake — transformations defined in the Python DataFrame API are translated to SQL and run on Snowflake's compute. Data never needs to leave Snowflake; you get warehouse scalability without moving data to a local machine or external cluster.",
  "Snowpark","hard",M,CERT),

c("What is SYSTEM$STREAM_HAS_DATA() and why is it used in Tasks?",
  "A system function that returns TRUE if the named stream contains unconsumed change records. Used as the WHEN condition in a Task: WHEN SYSTEM$STREAM_HAS_DATA('my_stream'). Prevents the task from running (and consuming warehouse credits) when there is nothing to process.",
  "Streams & Tasks","medium",M,CERT),

c("What is the difference between a table stage and a named internal stage for Snowpipe?",
  "Snowpipe requires a named internal stage or an external stage — it does not support user stages or table stages. Named stages are grantable, configurable, and reusable across pipes and COPY INTO statements. Table stages are tied to a specific table and are not suitable for Snowpipe.",
  "Data Ingestion","hard",M,CERT),

c("What is data skew and how does it manifest in Snowflake query performance?",
  "Data skew is uneven distribution of values in a join or GROUP BY key — a small number of values hold a disproportionately large number of rows. In Snowflake, this causes some worker nodes to process far more data than others, becoming bottlenecks. Visible in Query Profile as partitioned steps with wildly uneven row counts per thread.",
  "Performance","hard",M,CERT),

c("How do you implement a slowly changing dimension (SCD Type 2) in Snowflake?",
  "Option 1: Snowflake Streams + Task MERGE — detect changes in the stream, MERGE into the SCD table inserting new versions and closing old ones with dbt_valid_to. Option 2: Snowflake Snapshots (if using dbt). Option 3: Native snapshots (dbt snapshot command). Snowflake's Time Travel can also query historical states without SCD if retention period is sufficient.",
  "Performance","hard",M,CERT),

c("What is PIPE_EXECUTION_PAUSED and how do you resume a Snowpipe pipe?",
  "PIPE_EXECUTION_PAUSED status means the pipe has been explicitly paused (ALTER PIPE ... PAUSE) or suspended due to errors. Resume with: ALTER PIPE my_pipe RESUME; then confirm with SYSTEM$PIPE_STATUS('my_pipe'). After resuming, Snowpipe reprocesses files that arrived while paused.",
  "Data Ingestion","hard",M,CERT),
]


# ════════════════════════════════════════════════════════
# SNOWPRO ARCHITECT – expanded
# ════════════════════════════════════════════════════════
M = "SnowPro Architect"
CERT = "snowpro advanced architect"

new_cards += [
c("What is the Snowflake Native App Framework and how is it different from data sharing?",
  "Native Apps package application logic (stored procedures, Streamlit UIs, UDFs) along with data and run inside the consumer's Snowflake account. Unlike data sharing (which shares read-only data), Native Apps can write to the consumer's account, show UI, and interact with consumer data under a controlled permission model. Published via the Snowflake Marketplace.",
  "Data Sharing","hard",M,CERT),

c("What is a Snowflake Listing on the Marketplace and what can it contain?",
  "A published product entry. Listings can contain: (1) A data share (live read-only access to provider tables). (2) A Native App. (3) A collaboration listing (both parties share data). Listings can be free, request-based, or paid (via Snowflake billing). Global or regional availability can be configured.",
  "Data Sharing","hard",M,CERT),

c("How would you design a multi-tenant SaaS application on Snowflake?",
  "Options: (1) Separate database per tenant — strong isolation, easier offboarding, but high object count. (2) Shared database, separate schema per tenant — moderate isolation. (3) Shared schema with tenant_id column + Row Access Policy filtering per tenant — simplest but lowest isolation. Choice depends on compliance requirements, tenant count, and query patterns.",
  "Account Design","hard",M,CERT),

c("What is a Snowflake Virtual Private Snowflake (VPS) and when is it required?",
  "VPS is a fully dedicated, single-tenant deployment of Snowflake on dedicated cloud infrastructure — no shared resources with other Snowflake customers. Required by organisations with the strictest data isolation requirements (government, defence, certain financial institutions). Not available for self-service sign-up; requires a Snowflake enterprise contract.",
  "Account Design","hard",M,CERT),

c("What is the Business Critical edition's key differentiator over Enterprise?",
  "Business Critical adds: HIPAA and PCI-DSS compliance support, Tri-Secret Secure (customer-managed key encryption), Private Connectivity (PrivateLink/Private Endpoints), enhanced encryption (all data encrypted with customer-dedicated keys), and enhanced Data Protection SLA. Required for regulated industries.",
  "Account Design","hard",M,CERT),

c("What is a Snowflake Failover Group and what objects does it replicate?",
  "A named group of account objects that are replicated together from primary to secondary account for DR. Can include: databases, integrations, network policies, resource monitors, roles, users, warehouses, and parameters. On failover, the secondary account is promoted and can serve both reads and writes.",
  "Replication & DR","hard",M,CERT),

c("What is the difference between replication and data sharing in Snowflake?",
  "Replication physically copies data to a secondary account — the consumer has their own copy, can write to it (after failover), and no live dependency on the primary. Data sharing provides a live pointer to the provider's data — no copy, always current, consumer is read-only, and the connection depends on the provider's account being available.",
  "Replication & DR","hard",M,CERT),

c("What are Connection Objects (Redirects) in Snowflake DR?",
  "A global, stable URL that can be pointed to a primary or secondary account. When failover occurs, you update the Connection Object's pointer to the secondary — applications using the connection URL automatically reconnect to the new primary without changing connection strings.",
  "Replication & DR","hard",M,CERT),

c("How should an architect design warehouse configuration for a workload with both ETL and BI queries?",
  "Separate virtual warehouses by workload: a large ETL warehouse (L–XL) for heavy transformations, a medium analytics warehouse (M, multi-cluster) for concurrent BI users, and a small ad-hoc warehouse (XS–S) for interactive exploration. Separate warehouses prevent BI queuing from being blocked by ETL and allow independent scaling/suspension.",
  "Performance Architecture","hard",M,CERT),

c("What is warehouse query tagging and how is it used for cost attribution?",
  "SET QUERY_TAG = 'team:finance;project:month_end'; attaches a label to all subsequent queries in the session. Query tags appear in QUERY_HISTORY. Used to attribute compute costs to teams or projects when they share a warehouse — report on QUERY_HISTORY grouped by QUERY_TAG and WAREHOUSE_NAME.",
  "Cost Architecture","hard",M,CERT),

c("What Snowflake views would an architect use to analyse monthly storage costs?",
  "SNOWFLAKE.ACCOUNT_USAGE.STORAGE_USAGE — daily storage totals by storage type (database, stage, fail-safe). SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS — per-table storage breakdown including Time Travel and Fail-Safe bytes. Combine with DATA_RETENTION_TIME settings to identify tables with expensive Time Travel retention.",
  "Cost Architecture","hard",M,CERT),

c("What is the Snowflake data mesh architecture pattern?",
  "Apply data mesh principles on Snowflake: each domain team owns a Snowflake database (or account). Cross-domain data products are shared via Secure Data Sharing or a private Data Exchange. Governance is enforced centrally via Tags, Row Access Policies, and Data Classification applied across all accounts in the organisation.",
  "Account Design","hard",M,CERT),

c("How do you implement column-level lineage tracking in Snowflake?",
  "Snowflake provides OBJECT_DEPENDENCIES in ACCOUNT_USAGE to track object-level references (views, tasks, pipes). For column-level lineage, use ACCESS_HISTORY in ACCOUNT_USAGE (Enterprise+) which records which columns were read by each query. Combine with a data catalog (Atlan, OpenMetadata) that ingests ACCESS_HISTORY for visual lineage.",
  "Governance","hard",M,CERT),

c("What is the Snowflake Governance tri-layer model?",
  "1. Discover: classify sensitive data using Data Classification + Object Tags. 2. Manage: apply masking policies, row access policies, and network policies to control access. 3. Audit: review ACCESS_HISTORY, LOGIN_HISTORY, and POLICY_REFERENCES to verify policies are effective and data is being accessed appropriately.",
  "Governance","hard",M,CERT),

c("What is a custom RBAC hierarchy design pattern for large enterprises?",
  "Create three role types: (1) Functional roles (ANALYST, ENGINEER, REPORTER) — granted to users, define what a person does. (2) Object roles (DB_PROD_READ, SCHEMA_RAW_WRITE) — granted to functional roles, own and grant on specific objects. (3) System roles (SYSADMIN, SECURITYADMIN) — managed by the security team only, never granted to end users.",
  "Governance","hard",M,CERT),

c("When would you use a Private Data Exchange vs. the public Snowflake Marketplace?",
  "A Private Data Exchange is appropriate when sharing data with a defined, invitation-only group (partners, subsidiaries, regulated consumers). The public Marketplace is appropriate for monetising data at scale with any Snowflake customer. Private exchanges allow the provider to control who can discover and request access.",
  "Data Sharing","hard",M,CERT),

c("What is Snowflake's approach to cross-cloud data access without replication?",
  "For cross-cloud access without copying data, Snowflake Marketplace with Cross-Cloud Auto-Fulfillment automatically replicates the share to the consumer's cloud/region on demand. Alternatively, Snowflake External Tables can read data stored on one cloud from a Snowflake account on another cloud (with appropriate network routing).",
  "Data Sharing","hard",M,CERT),

c("How does an architect ensure that a Snowflake deployment meets GDPR requirements?",
  "1. Choose an EU Snowflake region and enable data residency. 2. Use Business Critical edition for private connectivity and enhanced encryption. 3. Apply Data Classification to identify PII columns. 4. Apply Dynamic Data Masking on PII columns. 5. Implement Row Access Policies to restrict access to personal data by role. 6. Enable Access History auditing. 7. Define Data Retention Time policies to support the right to erasure.",
  "Governance","hard",M,CERT),

c("What are Snowflake Budgets and how do they complement Resource Monitors?",
  "Budgets (introduced 2023) set a monthly credit spending limit for a scope (account, or a custom spending group of objects). They can monitor serverless feature costs (Automatic Clustering, Tasks, Snowpipe, Search Optimisation) which Resource Monitors cannot track. Resource Monitors only track virtual warehouse credit consumption. Use both: Resource Monitors per warehouse for real-time suspension, Budgets for account-level serverless cost caps.",
  "Cost Architecture","hard",M,CERT),

c("What is the Snowflake Cost Management Console?",
  "A section of Snowsight that provides visual credit consumption breakdowns by service type (warehouses, serverless, cloud services), over time. Architects use it alongside ACCOUNT_USAGE queries for chargeback reporting, anomaly detection, and capacity planning.",
  "Cost Architecture","medium",M,CERT),

c("How would you architect Snowflake for a global company with users in US, EU, and APAC?",
  "Deploy three Snowflake accounts — one per region (e.g., AWS us-east-1, eu-west-1, ap-southeast-1). Replicate reference/master data to each account. Regional transactional data stays in its home account. BI tools connect to the local account for low-latency queries. Use Marketplace or cross-account sharing for cross-regional reporting. This respects data residency and minimises query latency for local users.",
  "Account Design","hard",M,CERT),

c("What is Snowflake's model for handling PII under the right-to-erasure requirement?",
  "Snowflake does not support deleting individual rows from micro-partitions without rewriting them. Options: (1) DELETE + re-cluster (or CLUSTER BY maintenance) to purge the data. (2) Store PII in a separate table and replace with a pseudonym/token — dropping the PII table satisfies erasure. (3) After deletion, wait for Time Travel and Fail-Safe to expire (up to 97 days) before the data is fully purged from Snowflake infrastructure.",
  "Governance","hard",M,CERT),

c("What is the Snowflake Feature Store and how is it used?",
  "Part of Snowpark ML — a centralised repository for storing, versioning, and serving ML features (pre-computed feature columns) as Snowflake tables or dynamic tables. Data scientists register feature pipelines; model training retrieves consistent features; inference retrieves the same features at prediction time. Ensures train/serve consistency without copying data outside Snowflake.",
  "Data Architecture","hard",M,CERT),

c("What is a Snowflake Streamlit app and how does it integrate with the platform?",
  "Streamlit in Snowflake lets you deploy Python Streamlit web applications that run natively inside Snowflake. The app accesses Snowflake data without exporting it, runs with a specified warehouse for compute, and is governed by Snowflake roles and network policies. Used for internal dashboards, data exploration tools, and Native App UIs.",
  "Data Architecture","hard",M,CERT),
]


# ══ Append new cards to existing Snowflake deck ═══════════
deck = data['decks']['Snowflake']
deck['cards'].extend(new_cards)

with open('frontend/cards.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

from collections import Counter
all_cards = deck['cards']
mods = Counter(c['module'] for c in all_cards)
code  = sum(1 for c in all_cards if c.get('requires_code'))
print(f"Snowflake deck total: {len(all_cards)} cards  ({code} code cards)\n")
for m in deck['modules_ordered']:
    print(f"  {mods[m]:3}  {m}")

grand = sum(len(d['cards']) for d in data['decks'].values())
print(f"\nGrand total across all decks: {grand}")
