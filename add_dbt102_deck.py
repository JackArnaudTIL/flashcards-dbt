import json

with open('frontend/cards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ── helpers ──────────────────────────────────────────────────────────────────
def concept(q, a, group, difficulty="medium"):
    return {"q": q, "a": a, "group": group, "difficulty": difficulty, "category": group}

def code(q, a, groups, difficulty="Easy"):
    return {
        "q": q,
        "a": a,
        "group": groups if isinstance(groups, list) else [groups],
        "difficulty": difficulty,
        "category": groups[0] if isinstance(groups, list) else groups,
        "requires_code": True,
        "explanation": ""
    }

cards = [

    # ── Jinja Basics ──────────────────────────────────────────────────────────

    concept(
        "What are the three Jinja delimiter types used in dbt SQL files?",
        "{{ expression }} — outputs a value (e.g. {{ ref('model') }}). {% block %} — executes logic with no output (e.g. {% if %}, {% for %}, {% set %}). {# comment #} — comment that is stripped before the SQL is sent to the warehouse.",
        "Jinja Basics", "easy"
    ),
    concept(
        "What does `{% set my_var = 'value' %}` do in a dbt model?",
        "Defines a Jinja variable local to that file. Unlike dbt variables (var()), it exists only at compile time and is not accessible from the command line or dbt_project.yml.",
        "Jinja Basics"
    ),
    concept(
        "What does `{{ this }}` refer to inside a dbt model?",
        "A special dbt variable that resolves to the fully-qualified database relation for the current model (e.g. my_db.my_schema.my_model). Mainly used inside incremental models to self-reference the existing table.",
        "Jinja Basics"
    ),
    concept(
        "What does `{{ run_started_at }}` return in dbt?",
        "The UTC timestamp of when the current dbt run began. Useful for stamping audit columns (e.g. dbt_loaded_at) consistently across all models in a run, even if individual models finish at different times.",
        "Jinja Basics"
    ),
    concept(
        "What is `env_var()` in dbt and when would you use it?",
        "A dbt Jinja function that reads an OS environment variable: {{ env_var('MY_VAR') }}. Accepts an optional default: {{ env_var('MY_VAR', 'default') }}. Used to inject secrets or environment-specific values (e.g. schemas, credentials) without hardcoding them.",
        "Jinja Basics"
    ),
    concept(
        "What is the difference between `var()` and `env_var()` in dbt?",
        "var() reads a dbt project variable defined in dbt_project.yml or passed with --vars on the CLI — it is dbt-aware and version-controllable. env_var() reads an OS environment variable set outside dbt — used for secrets or infrastructure values that must not be committed to source control.",
        "Jinja Basics"
    ),
    concept(
        "How do you pass a variable to a dbt run from the command line?",
        "dbt run --vars '{my_var: my_value}'. Multiple variables: --vars '{var1: val1, var2: val2}'. CLI variables override defaults set in dbt_project.yml.",
        "Jinja Basics"
    ),

    # ── Config & Materializations ─────────────────────────────────────────────

    concept(
        "In what three places can you configure a dbt model, and what is the order of precedence?",
        "1. dbt_project.yml (lowest precedence — project-wide defaults by folder). 2. A config() block at the top of the model file. 3. A config block in a schema.yml (config: key). Model-level config always wins over project-level defaults.",
        "Config & Materializations"
    ),
    concept(
        "What columns does dbt automatically manage in an incremental model?",
        "None — dbt does not add any automatic columns. You are responsible for any audit columns you want (e.g. dbt_loaded_at, dbt_updated_at). The is_incremental() macro and {{ this }} are provided as tools, but column management is entirely in your SQL.",
        "Config & Materializations"
    ),
    concept(
        "What is `unique_key` in an incremental model config and what does it control?",
        "A column (or list of columns) used to identify a row uniquely. When dbt runs incrementally and unique_key is set, it deletes or merges existing rows with matching keys before inserting new ones — preventing duplicates. Without unique_key, dbt only appends rows.",
        "Config & Materializations"
    ),
    concept(
        "What is the `on_schema_change` config for incremental models?",
        "Controls behaviour when upstream columns are added or removed. Options: 'ignore' (default — new columns are silently dropped), 'fail' (error on any schema change), 'append_new_columns' (add new columns, keep old ones), 'sync_all_columns' (keep in sync, dropping removed columns).",
        "Config & Materializations"
    ),
    concept(
        "What is the `schema` config on a model and how does it interact with the target schema?",
        "Sets a custom schema suffix for the model: config(schema='reporting') makes dbt build the model in <target_schema>_reporting (by default). You can override the generate_schema_name macro to change this concatenation behaviour.",
        "Config & Materializations"
    ),
    concept(
        "What is the `alias` config on a dbt model?",
        "Sets the name of the database object dbt creates, independently of the model's filename. config(alias='final_orders') builds a table/view called final_orders regardless of the .sql filename.",
        "Config & Materializations"
    ),

    # ── Sources ───────────────────────────────────────────────────────────────

    concept(
        "What is `loaded_at_field` in a dbt source definition?",
        "The name of the timestamp column in the source table that records when each row was loaded. dbt uses this column in `dbt source freshness` to determine whether the source data is fresh enough.",
        "Sources"
    ),
    concept(
        "What does `dbt source freshness` exit with if a source is stale?",
        "Exit code 1 (error) if any source exceeds its error_after threshold. Sources that exceed only warn_after produce a warning but exit 0. Sources with no freshness config are not checked.",
        "Sources"
    ),
    concept(
        "Can you apply data tests to a source in dbt?",
        "Yes. Define tests under the source table's columns in sources.yml the same way you would for a model — not_null, unique, accepted_values, relationships all work on source columns.",
        "Sources"
    ),
    concept(
        "What is a `source override` in dbt (dbt_project.yml)?",
        "You can set config for all tables in a source at the source level (e.g. +tags, +meta) in sources.yml. This avoids repeating the config on every table. Individual tables can still override source-level config.",
        "Sources"
    ),

    # ── Testing (deeper) ──────────────────────────────────────────────────────

    concept(
        "How do you make a generic test only warn instead of fail?",
        "Set severity: warn in the test config in schema.yml: data_tests: [{not_null: {config: {severity: warn}}}]. The test runs but dbt continues and exits 0 if only warnings occurred.",
        "Testing"
    ),
    concept(
        "What is `store_failures: true` for dbt tests?",
        "When set in the test config (or globally in dbt_project.yml), dbt saves the rows that fail each test into a table in the warehouse. Useful for debugging — you can query the failure table to see exactly which records failed.",
        "Testing"
    ),
    concept(
        "How do you add a custom generic test in dbt?",
        "Create a macro in macros/ named test_<test_name>(model, column_name, ...) that returns a SELECT of failing rows. Then reference it in schema.yml by its name (without the test_ prefix).",
        "Testing"
    ),
    concept(
        "What is `dbt_expectations` and what does it add?",
        "A popular dbt package (from Calogica) that adds 50+ data quality tests modelled after the Great Expectations library — e.g. expect_column_values_to_be_between, expect_table_row_count_to_be_between. Install via packages.yml.",
        "Testing"
    ),

    # ── Tags & Selection ──────────────────────────────────────────────────────

    concept(
        "How do you apply a tag to every model in a subdirectory using `dbt_project.yml`?",
        "Use folder-level config in dbt_project.yml: under models: > project_name: > staging:, add +tags: ['staging']. The + prefix means the config applies to all nodes at and below that path.",
        "Tags & Selection"
    ),
    concept(
        "What does the `--exclude` flag do in dbt?",
        "Removes nodes from the set selected by --select. dbt run --select staging+ --exclude stg_payments runs everything downstream of staging/ except stg_payments and its descendants.",
        "Tags & Selection"
    ),
    concept(
        "What selector syntax targets all models in a specific directory?",
        "Use a path selector: dbt run --select models/staging/ or dbt run --select staging.*. The path selector matches any model whose file path contains that string.",
        "Tags & Selection"
    ),
    concept(
        "What does the `state:modified` selector do?",
        "Selects only models whose compiled SQL or upstream dependency has changed compared to a previous run's manifest.json. Used in Slim CI: dbt build --select state:modified+ --state path/to/previous/target",
        "Tags & Selection"
    ),

    # ── Packages ──────────────────────────────────────────────────────────────

    concept(
        "What is `dbt_utils.generate_surrogate_key()` and when would you use it?",
        "A macro that hashes a list of column values to produce a deterministic surrogate key: {{ dbt_utils.generate_surrogate_key(['order_id', 'line_item_id']) }}. Use it when a natural unique key spans multiple columns or when upstream IDs may not be stable.",
        "Packages"
    ),
    concept(
        "What is `dbt_utils.star()` and when is it useful?",
        "A macro that generates SELECT col1, col2, ... for all columns in a relation, with optional exclusions: {{ dbt_utils.star(from=ref('stg_orders'), except=['pii_column']) }}. Useful in staging models where you want all columns minus a few.",
        "Packages"
    ),
    concept(
        "What is `dbt_utils.date_spine()` used for?",
        "Generates a table of sequential dates between two endpoints — useful for building calendar/date dimension tables or filling gaps in time-series data without relying on existing data to have every date.",
        "Packages"
    ),

    # ── Code Cards (requires_code: true) ─────────────────────────────────────

    code(
        "Write a minimal dbt model that selects all columns from a source table named 'orders' in the 'stripe' source.",
        "```sql\nSELECT *\nFROM {{ source('stripe', 'orders') }}\n```",
        ["Code – Models"]
    ),
    code(
        "Write a `{{ config() }}` block that sets a model to materialise as a table and adds the tag 'nightly'.",
        "```sql\n{{ config(\n    materialized='table',\n    tags=['nightly']\n) }}\n```",
        ["Code – Config"]
    ),
    code(
        "Write a `{{ config() }}` block for an incremental model. The unique key is 'order_id'.",
        "```sql\n{{ config(\n    materialized='incremental',\n    unique_key='order_id'\n) }}\n```",
        ["Code – Config"]
    ),
    code(
        "Write a staging model for the 'raw_orders' source table. Rename 'id' to 'order_id' and 'amt' to 'amount'. Select no other columns.",
        "```sql\nSELECT\n    id  AS order_id,\n    amt AS amount\nFROM {{ source('raw', 'raw_orders') }}\n```",
        ["Code – Models"]
    ),
    code(
        "Write a dbt model using CTEs that selects 'order_id' and 'order_date' from 'stg_orders', keeping only rows where status = 'placed'.",
        "```sql\nWITH source AS (\n    SELECT * FROM {{ ref('stg_orders') }}\n),\nfiltered AS (\n    SELECT order_id, order_date\n    FROM source\n    WHERE status = 'placed'\n)\nSELECT * FROM filtered\n```",
        ["Code – Models"]
    ),
    code(
        "Write the Jinja `{% if is_incremental() %}` block that filters a model to only load rows where 'updated_at' is greater than the maximum value already in the table.",
        "```sql\n{% if is_incremental() %}\nWHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})\n{% endif %}\n```",
        ["Code – Incremental"]
    ),
    code(
        "Write a sources.yml that declares a source named 'stripe' in the 'raw' schema, with one table called 'charges'.",
        "```yaml\nsources:\n  - name: stripe\n    schema: raw\n    tables:\n      - name: charges\n```",
        ["Code – YAML"]
    ),
    code(
        "Write a schema.yml entry for a model named 'stg_orders'. Add not_null and unique tests to the 'order_id' column.",
        "```yaml\nmodels:\n  - name: stg_orders\n    columns:\n      - name: order_id\n        data_tests:\n          - not_null\n          - unique\n```",
        ["Code – YAML"]
    ),
    code(
        "Add an accepted_values test to the 'status' column in a schema.yml for 'stg_orders'. Valid values are 'placed', 'shipped', and 'returned'.",
        "```yaml\nmodels:\n  - name: stg_orders\n    columns:\n      - name: status\n        data_tests:\n          - accepted_values:\n              values: ['placed', 'shipped', 'returned']\n```",
        ["Code – YAML"]
    ),
    code(
        "Write a relationships test in schema.yml that checks every 'customer_id' in 'stg_orders' exists as a 'customer_id' in 'stg_customers'.",
        "```yaml\nmodels:\n  - name: stg_orders\n    columns:\n      - name: customer_id\n        data_tests:\n          - relationships:\n              to: ref('stg_customers')\n              field: customer_id\n```",
        ["Code – YAML"]
    ),
    code(
        "Write a model that joins 'stg_orders' and 'stg_customers' on customer_id. Select order_id, order_date, and customer_name.",
        "```sql\nWITH orders AS (\n    SELECT * FROM {{ ref('stg_orders') }}\n),\ncustomers AS (\n    SELECT * FROM {{ ref('stg_customers') }}\n)\nSELECT\n    o.order_id,\n    o.order_date,\n    c.customer_name\nFROM orders o\nJOIN customers c ON o.customer_id = c.customer_id\n```",
        ["Code – Models"]
    ),
    code(
        "Write the dbt_project.yml config block that sets all models inside the 'staging' folder to materialise as views.",
        "```yaml\nmodels:\n  my_project:\n    staging:\n      +materialized: view\n```",
        ["Code – YAML"]
    ),
    code(
        "Add source freshness checks to the 'charges' source table. Warn if data is older than 12 hours; error if older than 24 hours. The timestamp column is 'loaded_at'.",
        "```yaml\nsources:\n  - name: stripe\n    tables:\n      - name: charges\n        loaded_at_field: loaded_at\n        freshness:\n          warn_after: {count: 12, period: hour}\n          error_after: {count: 24, period: hour}\n```",
        ["Code – YAML"]
    ),
    code(
        "Write a dbt macro named 'cents_to_dollars' that accepts a column name and returns it divided by 100, cast to DECIMAL(10,2).",
        "```sql\n{% macro cents_to_dollars(column_name) %}\n    CAST({{ column_name }} / 100.0 AS DECIMAL(10, 2))\n{% endmacro %}\n```",
        ["Code – Macros"]
    ),
    code(
        "Write a model that uses a project variable named 'start_date' to filter rows where 'created_at' is on or after that date.",
        "```sql\nSELECT *\nFROM {{ ref('stg_events') }}\nWHERE created_at >= '{{ var(\"start_date\") }}'\n```",
        ["Code – Jinja"]
    ),
    code(
        "Use dbt_utils.generate_surrogate_key() to create a column named 'surrogate_key' from 'order_id' and 'line_item_id'.",
        "```sql\nSELECT\n    {{ dbt_utils.generate_surrogate_key(['order_id', 'line_item_id']) }} AS surrogate_key,\n    order_id,\n    line_item_id\nFROM {{ ref('stg_order_items') }}\n```",
        ["Code – Macros"]
    ),
    code(
        "Write a minimal dbt snapshot definition for a 'customers' source table using the timestamp strategy on 'updated_at'. Unique key is 'customer_id'. Target schema is 'snapshots'.",
        "```sql\n{% snapshot customers_snapshot %}\n\n{{ config(\n    target_schema='snapshots',\n    unique_key='customer_id',\n    strategy='timestamp',\n    updated_at='updated_at'\n) }}\n\nSELECT * FROM {{ source('app', 'customers') }}\n\n{% endsnapshot %}\n```",
        ["Code – Snapshots"]
    ),
    code(
        "Write a config() block that applies the tags 'finance' and 'daily', and places the model in a custom schema named 'reporting'.",
        "```sql\n{{ config(\n    tags=['finance', 'daily'],\n    schema='reporting'\n) }}\n```",
        ["Code – Config"]
    ),
    code(
        "Write a dbt expression using env_var() that reads the warehouse username from an environment variable called 'DBT_USER', falling back to 'readonly' if not set.",
        "```sql\n{{ env_var('DBT_USER', 'readonly') }}\n```",
        ["Code – Jinja"]
    ),
    code(
        "Write a packages.yml that installs dbt-labs/dbt_utils at version 1.3.0.",
        "```yaml\npackages:\n  - package: dbt-labs/dbt_utils\n    version: 1.3.0\n```",
        ["Code – YAML"]
    ),
]

data['decks']['dbt 102'] = {
    "section": "Professional Development",
    "cards": cards
}

with open('frontend/cards.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

from collections import Counter
cats = Counter(c['category'] for c in cards)
code_cards = [c for c in cards if c.get('requires_code')]
print(f"Total: {len(cards)} cards  ({len(code_cards)} code cards, {len(cards)-len(code_cards)} conceptual)")
print()
for cat, n in sorted(cats.items()):
    tag = " *" if any(c.get('requires_code') for c in cards if c['category'] == cat) else ""
    print(f"  {n:2}  {cat}{tag}")
print("\n(* = includes code cards)")
