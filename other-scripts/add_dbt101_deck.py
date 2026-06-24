import json

with open('frontend/cards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cards = [

    # ── Core Concepts ──────────────────────────────────────────────────────────

    {
        "q": "What is dbt?",
        "a": "dbt (data build tool) is an open-source transformation framework that lets analysts and engineers write modular SQL SELECT statements, which dbt compiles and runs against a data warehouse to build and test tables and views.",
        "group": "Core Concepts", "difficulty": "easy", "category": "Core Concepts"
    },
    {
        "q": "What problem does dbt solve?",
        "a": "It brings software engineering best practices (version control, testing, documentation, modularity) to data transformation. Before dbt, transformations were often scattered across stored procedures, BI tools, and ad-hoc scripts with no lineage or tests.",
        "group": "Core Concepts", "difficulty": "easy", "category": "Core Concepts"
    },
    {
        "q": "What is a dbt model?",
        "a": "A single SQL SELECT statement saved as a .sql file in the models/ directory. When dbt runs a model it wraps the SELECT in a CREATE TABLE or CREATE VIEW statement and executes it in the data warehouse.",
        "group": "Core Concepts", "difficulty": "easy", "category": "Core Concepts"
    },
    {
        "q": "What does dbt NOT do?",
        "a": "dbt does not extract or load data. It only transforms data that already exists in your warehouse. The EL (Extract, Load) step is handled by separate tools like Fivetran, Airbyte, or custom pipelines.",
        "group": "Core Concepts", "difficulty": "easy", "category": "Core Concepts"
    },
    {
        "q": "What is a dbt source?",
        "a": "A declaration in a sources.yml file that tells dbt where your raw data lives — the database, schema, and table name. Using source() instead of direct table references lets dbt track lineage and test freshness.",
        "group": "Core Concepts", "difficulty": "easy", "category": "Core Concepts"
    },
    {
        "q": "What does the `ref()` function do?",
        "a": "It references another dbt model by name (e.g., ref('stg_orders')). dbt replaces it with the actual compiled relation at runtime, automatically builds a dependency graph, and ensures models run in the right order.",
        "group": "Core Concepts", "difficulty": "easy", "category": "Core Concepts"
    },
    {
        "q": "What does the `source()` function do?",
        "a": "It references a raw source table declared in sources.yml (e.g., source('stripe', 'payments')). This lets dbt track lineage from raw sources, and enables freshness checks on those tables.",
        "group": "Core Concepts", "difficulty": "easy", "category": "Core Concepts"
    },
    {
        "q": "What is the difference between `ref()` and `source()`?",
        "a": "ref() references another dbt model (something you built). source() references a raw table loaded by an external pipeline (something you didn't build). Both generate the correct relation name and track lineage.",
        "group": "Core Concepts", "difficulty": "easy", "category": "Core Concepts"
    },
    {
        "q": "What is a dbt seed?",
        "a": "A CSV file in the seeds/ directory that dbt loads into the warehouse as a table. Useful for small, static lookup data (e.g., country codes, cost centres) that changes infrequently.",
        "group": "Core Concepts", "difficulty": "easy", "category": "Core Concepts"
    },
    {
        "q": "What is a dbt snapshot?",
        "a": "A dbt feature that captures the historical state of a mutable source table over time (Type 2 SCD). dbt adds dbt_valid_from / dbt_valid_to columns so you can query what data looked like at any point in time.",
        "group": "Core Concepts", "difficulty": "medium", "category": "Core Concepts"
    },
    {
        "q": "What is a dbt macro?",
        "a": "A reusable block of Jinja-templated SQL or logic defined in the macros/ directory. Macros work like functions — you call them from models or other macros and they return SQL text at compile time.",
        "group": "Core Concepts", "difficulty": "easy", "category": "Core Concepts"
    },
    {
        "q": "What is a dbt package?",
        "a": "A reusable collection of models, macros, and tests published as a standalone dbt project (e.g., dbt_utils, dbt_expectations). Install packages via packages.yml and run dbt deps to download them.",
        "group": "Core Concepts", "difficulty": "easy", "category": "Core Concepts"
    },
    {
        "q": "What is the DAG in dbt?",
        "a": "The Directed Acyclic Graph — dbt's internal representation of how models depend on each other. Built from ref() and source() calls, it determines the order models are built and is visualised in dbt's lineage graph.",
        "group": "Core Concepts", "difficulty": "medium", "category": "Core Concepts"
    },
    {
        "q": "What is Jinja in the context of dbt?",
        "a": "A templating language that dbt embeds in SQL files. It lets you use variables ({{ }}), logic blocks ({% %}), and macros to make SQL dynamic — e.g., {{ ref('my_model') }}, {% if is_incremental() %}, {{ config(...) }}.",
        "group": "Core Concepts", "difficulty": "easy", "category": "Core Concepts"
    },
    {
        "q": "What is the difference between dbt Core and dbt Cloud?",
        "a": "dbt Core is the open-source CLI tool — free, runs anywhere, but you manage your own environment. dbt Cloud is a managed SaaS platform built on top of Core — adds a web IDE, job scheduling, CI/CD, lineage explorer, and collaboration features.",
        "group": "Core Concepts", "difficulty": "easy", "category": "Core Concepts"
    },

    # ── Project Structure ──────────────────────────────────────────────────────

    {
        "q": "What is the purpose of `dbt_project.yml`?",
        "a": "The main project configuration file. It sets the project name, model paths, materialization defaults, variable definitions, and folder-level config (e.g., all models in staging/ use +schema: staging). Every dbt project must have one.",
        "group": "Project Structure", "difficulty": "easy", "category": "Project Structure"
    },
    {
        "q": "What is `profiles.yml` and where does it live?",
        "a": "Contains connection credentials for each dbt target environment (dev, prod) — warehouse type, host, database, schema, credentials. Lives at ~/.dbt/profiles.yml (local) and is NOT committed to source control. dbt Cloud manages this separately.",
        "group": "Project Structure", "difficulty": "easy", "category": "Project Structure"
    },
    {
        "q": "What is `schema.yml` used for in dbt?",
        "a": "YAML files (commonly named schema.yml, but any .yml file works) in the models/ directory where you document models and columns, and define data tests. Also used to declare sources (sources.yml) and exposures.",
        "group": "Project Structure", "difficulty": "easy", "category": "Project Structure"
    },
    {
        "q": "What is the standard dbt project folder structure?",
        "a": "models/ (SQL models), seeds/ (CSV files), snapshots/ (snapshot SQL), macros/ (Jinja macros), tests/ (singular tests), analyses/ (ad-hoc SQL), dbt_project.yml (project config), packages.yml (package dependencies).",
        "group": "Project Structure", "difficulty": "easy", "category": "Project Structure"
    },
    {
        "q": "What is the recommended layer structure for dbt models?",
        "a": "Staging (stg_) — one-to-one with source tables, light cleaning only. Intermediate (int_) — joins and business logic. Marts (fct_, dim_) — final models consumed by BI tools. This separation makes the project easier to navigate and test.",
        "group": "Project Structure", "difficulty": "medium", "category": "Project Structure"
    },
    {
        "q": "What naming convention do dbt projects typically follow?",
        "a": "stg_ prefix for staging models, int_ for intermediate, fct_ for fact tables, dim_ for dimension tables. Seeds use plain names. Snapshots often end in _snapshot. Consistent naming makes lineage and model purpose immediately clear.",
        "group": "Project Structure", "difficulty": "easy", "category": "Project Structure"
    },
    {
        "q": "What is `packages.yml` and what command reads it?",
        "a": "A file listing external dbt packages your project depends on (e.g., dbt-labs/dbt_utils). Run `dbt deps` to download and install them into the dbt_packages/ directory.",
        "group": "Project Structure", "difficulty": "easy", "category": "Project Structure"
    },

    # ── Materializations ───────────────────────────────────────────────────────

    {
        "q": "What are the four core dbt materializations?",
        "a": "view — creates a database view (default). table — creates a physical table, rebuilt each run. ephemeral — no database object created; inlined as a CTE wherever it's referenced. incremental — creates a table and only processes new/changed rows on subsequent runs.",
        "group": "Materializations", "difficulty": "easy", "category": "Materializations"
    },
    {
        "q": "What is the default dbt materialization and when should you change it?",
        "a": "The default is 'view'. Change to 'table' when the view is slow to query (complex transformations). Change to 'incremental' when the model processes large datasets where rebuilding is too expensive.",
        "group": "Materializations", "difficulty": "easy", "category": "Materializations"
    },
    {
        "q": "When should you use `materialized='table'` over `materialized='view'`?",
        "a": "When the model is expensive to compute and queried frequently. A table stores the result physically, so each query reads pre-computed data. A view re-runs the SQL on every query.",
        "group": "Materializations", "difficulty": "easy", "category": "Materializations"
    },
    {
        "q": "When should you use an ephemeral model?",
        "a": "For simple helper logic that is only used once by a single downstream model — like a CTE you'd rather keep in a separate file for readability. Ephemeral models create no database object and are inlined at compile time.",
        "group": "Materializations", "difficulty": "medium", "category": "Materializations"
    },
    {
        "q": "What is an incremental model and what problem does it solve?",
        "a": "An incremental model only processes rows that are new or changed since the last run, rather than rebuilding the entire table. This makes large-table transformations (billions of rows) practical to run on a schedule.",
        "group": "Materializations", "difficulty": "medium", "category": "Materializations"
    },
    {
        "q": "What does `dbt run --full-refresh` do to an incremental model?",
        "a": "Drops and recreates the incremental model from scratch, processing all rows. Use this when the model's logic changes or when you suspect the table has drifted from what a clean build would produce.",
        "group": "Materializations", "difficulty": "medium", "category": "Materializations"
    },
    {
        "q": "How does dbt know what rows to skip in an incremental model?",
        "a": "It doesn't automatically — you write a `{% if is_incremental() %}` Jinja block in the model with a WHERE clause that filters for new rows (e.g., where updated_at > max(updated_at) from the existing table).",
        "group": "Materializations", "difficulty": "medium", "category": "Materializations"
    },

    # ── Commands ───────────────────────────────────────────────────────────────

    {
        "q": "What does `dbt run` do?",
        "a": "Compiles all selected SQL models and executes them against the data warehouse, creating or replacing the corresponding views or tables. Does not run tests.",
        "group": "Commands", "difficulty": "easy", "category": "Commands"
    },
    {
        "q": "What does `dbt test` do?",
        "a": "Runs all data tests defined in schema.yml (and singular tests in tests/) against the existing tables. Returns a non-zero exit code if any test fails.",
        "group": "Commands", "difficulty": "easy", "category": "Commands"
    },
    {
        "q": "What does `dbt build` do, and how is it different from `dbt run` + `dbt test`?",
        "a": "dbt build runs models, seeds, snapshots, and tests in DAG order — it runs a model's tests before building downstream models that depend on it. dbt run + dbt test runs everything first, then all tests — tests cannot gate downstream builds.",
        "group": "Commands", "difficulty": "medium", "category": "Commands"
    },
    {
        "q": "What does `dbt compile` do?",
        "a": "Renders all Jinja in your SQL files and writes the compiled SQL to the target/ directory, but does NOT execute anything in the warehouse. Useful for inspecting what SQL dbt will actually run.",
        "group": "Commands", "difficulty": "easy", "category": "Commands"
    },
    {
        "q": "What does `dbt debug` do?",
        "a": "Tests your database connection and validates your profiles.yml and dbt_project.yml configuration. Run it first when setting up a new project or troubleshooting connection errors.",
        "group": "Commands", "difficulty": "easy", "category": "Commands"
    },
    {
        "q": "What does `dbt deps` do?",
        "a": "Reads packages.yml and downloads all declared package dependencies into the dbt_packages/ directory. Must be run after adding or updating a package.",
        "group": "Commands", "difficulty": "easy", "category": "Commands"
    },
    {
        "q": "What does `dbt seed` do?",
        "a": "Loads CSV files from the seeds/ directory into the data warehouse as tables. Useful for small static lookup tables (e.g., country codes, cost centres).",
        "group": "Commands", "difficulty": "easy", "category": "Commands"
    },
    {
        "q": "What does `dbt snapshot` do?",
        "a": "Runs all snapshot definitions, comparing current source data to the existing snapshot table and inserting new records for any changed rows, with dbt_valid_from/dbt_valid_to populated.",
        "group": "Commands", "difficulty": "medium", "category": "Commands"
    },
    {
        "q": "What does `dbt docs generate` do?",
        "a": "Builds a documentation website for your project by compiling model descriptions, column descriptions, test definitions, and the DAG lineage graph into a set of static files in the target/ directory.",
        "group": "Commands", "difficulty": "easy", "category": "Commands"
    },
    {
        "q": "What does `dbt docs serve` do?",
        "a": "Launches a local web server to view the documentation website generated by dbt docs generate. Opens the lineage graph and all model/column documentation in your browser.",
        "group": "Commands", "difficulty": "easy", "category": "Commands"
    },
    {
        "q": "What does `dbt source freshness` do?",
        "a": "Queries the loaded_at_field of each declared source table and compares the most recent timestamp against warn_after and error_after thresholds. Exits with a non-zero code if any source is stale.",
        "group": "Commands", "difficulty": "medium", "category": "Commands"
    },
    {
        "q": "What does `dbt ls` (list) do?",
        "a": "Prints the names of all nodes that match a given --select expression, without running them. Useful for validating selection syntax before running an expensive job.",
        "group": "Commands", "difficulty": "easy", "category": "Commands"
    },
    {
        "q": "How do you run only a single model in dbt?",
        "a": "dbt run --select model_name — the --select flag (or -s) accepts model names, folder paths, tags, and other selectors to limit what dbt runs.",
        "group": "Commands", "difficulty": "easy", "category": "Commands"
    },
    {
        "q": "What does the `+` suffix mean in dbt node selection? e.g. `dbt run --select stg_orders+`",
        "a": "Selects the model AND all its downstream dependents (children, grandchildren…). A prefix (+stg_orders) selects the model AND all its upstream ancestors. Both (+stg_orders+) selects the full lineage.",
        "group": "Commands", "difficulty": "medium", "category": "Commands"
    },

    # ── Testing ────────────────────────────────────────────────────────────────

    {
        "q": "What are the four built-in generic tests in dbt?",
        "a": "not_null — no NULLs in the column. unique — all values are distinct. accepted_values — only specified values appear. relationships — every value exists in another model's column (referential integrity).",
        "group": "Testing", "difficulty": "easy", "category": "Testing"
    },
    {
        "q": "Where do you define generic tests in dbt?",
        "a": "In a YAML file (e.g., schema.yml) alongside the model, under the columns section: data_tests: [not_null, unique, ...]. dbt compiles each test into a SQL query that returns failing rows.",
        "group": "Testing", "difficulty": "easy", "category": "Testing"
    },
    {
        "q": "How does dbt determine whether a test passes or fails?",
        "a": "dbt runs each test as a SQL query that returns failing rows. If the query returns 0 rows, the test passes. If it returns any rows, the test fails. You never need to write assertions — just a SELECT of bad rows.",
        "group": "Testing", "difficulty": "easy", "category": "Testing"
    },
    {
        "q": "What is a singular test in dbt?",
        "a": "A custom SQL file saved in the tests/ directory. It returns rows that fail the test — if it returns any rows, the test fails. Use for complex assertions that can't be expressed as a generic test (e.g., cross-table comparisons).",
        "group": "Testing", "difficulty": "medium", "category": "Testing"
    },
    {
        "q": "What is the difference between a generic test and a singular test?",
        "a": "Generic tests (defined in YAML) are reusable across many models. Singular tests (SQL files in tests/) are one-off assertions. Both fail if they return rows, but generic tests accept parameters while singular tests are self-contained.",
        "group": "Testing", "difficulty": "medium", "category": "Testing"
    },
    {
        "q": "What happens to downstream models if an upstream test fails during `dbt build`?",
        "a": "dbt build stops and skips all downstream nodes that depend on the failed model. This prevents bad data from propagating downstream — unlike dbt run + dbt test, which runs everything before testing.",
        "group": "Testing", "difficulty": "medium", "category": "Testing"
    },
    {
        "q": "What does test severity: warn do?",
        "a": "Instead of failing the build when a test returns rows, dbt logs a warning and continues. The run completes but is flagged as having warnings. Useful for checks you want to monitor without blocking deployment.",
        "group": "Testing", "difficulty": "medium", "category": "Testing"
    },

    # ── Documentation ──────────────────────────────────────────────────────────

    {
        "q": "How do you add a description to a dbt model?",
        "a": "In schema.yml, add a 'description:' field under the model name. You can also add descriptions at the column level. These appear in dbt docs and dbt Explorer.",
        "group": "Documentation", "difficulty": "easy", "category": "Documentation"
    },
    {
        "q": "What is dbt Explorer?",
        "a": "A dbt Cloud feature that provides an interactive, always-up-to-date view of your project's lineage graph, model metadata, test results, and column-level documentation. Replaces the self-hosted dbt docs site for dbt Cloud users.",
        "group": "Documentation", "difficulty": "easy", "category": "Documentation"
    },
    {
        "q": "What is a doc block in dbt and when would you use one?",
        "a": "A named block of markdown text defined in a .md file using {% docs block_name %}...{% enddocs %}. Reference it in schema.yml with {{ doc('block_name') }}. Use it when descriptions are long enough to deserve their own file.",
        "group": "Documentation", "difficulty": "medium", "category": "Documentation"
    },

    # ── dbt Cloud ─────────────────────────────────────────────────────────────

    {
        "q": "What is a dbt Cloud environment?",
        "a": "A named configuration that maps to a dbt target — it specifies the warehouse connection, dbt version, and environment variables. You typically have at least two: Development and Production.",
        "group": "dbt Cloud", "difficulty": "easy", "category": "dbt Cloud"
    },
    {
        "q": "What is a dbt Cloud job?",
        "a": "A configured set of dbt commands (e.g., dbt build) that runs in a specific environment on a schedule or trigger. Jobs produce run artifacts (manifest.json, run_results.json) visible in the run history.",
        "group": "dbt Cloud", "difficulty": "easy", "category": "dbt Cloud"
    },
    {
        "q": "What is Slim CI in dbt Cloud?",
        "a": "A CI pattern that only builds and tests models that changed in a pull request, using `dbt build --select state:modified+ --defer`. This dramatically reduces CI run time and cost compared to rebuilding the full project.",
        "group": "dbt Cloud", "difficulty": "medium", "category": "dbt Cloud"
    },
    {
        "q": "What is the dbt Cloud IDE?",
        "a": "A browser-based SQL and Jinja editor inside dbt Cloud. Lets developers write, preview, compile, and run dbt models without installing anything locally. Connects directly to the warehouse and shows a live lineage graph.",
        "group": "dbt Cloud", "difficulty": "easy", "category": "dbt Cloud"
    },
    {
        "q": "What is a dbt Cloud service token used for?",
        "a": "A machine-readable API credential (not tied to a user account) used to trigger dbt Cloud jobs programmatically — from CI/CD systems, orchestrators, or external tools. Scoped to specific permissions.",
        "group": "dbt Cloud", "difficulty": "medium", "category": "dbt Cloud"
    },

    # ── Best Practices ─────────────────────────────────────────────────────────

    {
        "q": "Why should you always use `source()` to reference raw tables instead of hardcoding schema.table?",
        "a": "source() registers the dependency in dbt's DAG (enabling lineage), allows freshness checks, and makes it easy to swap schemas between environments. Hardcoded references bypass all of this.",
        "group": "Best Practices", "difficulty": "easy", "category": "Best Practices"
    },
    {
        "q": "Why should staging models only reference sources, not other models?",
        "a": "Staging models are a 1:1 mapping with source tables — their job is to clean and type raw data. Referencing other models in staging breaks this contract and makes it harder to trace issues back to raw data.",
        "group": "Best Practices", "difficulty": "medium", "category": "Best Practices"
    },
    {
        "q": "What is the recommended SQL style for dbt models?",
        "a": "Use CTEs (WITH clauses) instead of nested subqueries. Name CTEs after what they represent (source, renamed, filtered, final). This makes models easier to read, test, and debug.",
        "group": "Best Practices", "difficulty": "easy", "category": "Best Practices"
    },
    {
        "q": "Why should you avoid using `SELECT *` in dbt models?",
        "a": "SELECT * makes the model's output schema unpredictable — new columns added upstream will silently appear downstream. Explicit column selection documents the model's schema and prevents unexpected changes.",
        "group": "Best Practices", "difficulty": "easy", "category": "Best Practices"
    },
    {
        "q": "What is the purpose of the staging layer in a dbt project?",
        "a": "To provide a clean, consistent view of each raw source table — renaming columns to a standard convention, casting data types, filtering deleted rows, and deduplicating. All downstream models build on staging, never on raw sources directly.",
        "group": "Best Practices", "difficulty": "easy", "category": "Best Practices"
    },
    {
        "q": "When should you materialise a staging model as a table vs. a view?",
        "a": "Start with view (default) — staging models are simple and views avoid storage cost. Switch to table if the staging model is expensive (large source, complex deduplication) or queried very frequently by many downstream models.",
        "group": "Best Practices", "difficulty": "medium", "category": "Best Practices"
    },
    {
        "q": "What is the purpose of adding descriptions to models and columns in dbt?",
        "a": "Descriptions become part of the project's self-documenting lineage in dbt docs / Explorer. They help teammates (and your future self) understand what a model represents without reading the SQL.",
        "group": "Best Practices", "difficulty": "easy", "category": "Best Practices"
    },
]

data['decks']['dbt 101'] = {
    "section": "Professional Development",
    "cards": cards
}

with open('frontend/cards.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

from collections import Counter
cats = Counter(c['category'] for c in cards)
diffs = Counter(c['difficulty'] for c in cards)
print(f"Total: {len(cards)} cards")
print()
for cat, n in sorted(cats.items()):
    print(f"  {n:2}  {cat}")
print()
print("Difficulty:", dict(diffs))
