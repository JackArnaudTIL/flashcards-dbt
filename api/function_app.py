import azure.functions as func
import json
import logging
import os
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient
import sqlfluff
import ast
import yaml
from jinja2 import Environment, TemplateSyntaxError

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

CONTAINER_NAME = "flashcard-feedback"
BLOB_NAME      = "feedback.jsonl"


def get_blob_client():
    conn_str = os.environ["FEEDBACK_STORAGE_CONNECTION_STRING"]
    service  = BlobServiceClient.from_connection_string(conn_str)
    return service.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

# ─── ENDPOINT 1: Feedback Logger ──────────────────────────────
@app.route(route="flashcardfeedback", methods=["POST", "OPTIONS"])
def flashcardfeedback(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Flashcard feedback function processed a request.')

    # ── CORS preflight ────────────────────────────────────────────
    allowed_origin = os.environ.get("ALLOWED_ORIGIN", "*")
    cors_headers = {
        "Access-Control-Allow-Origin":  allowed_origin,
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers=cors_headers)

    # ── Parse body ────────────────────────────────────────────────
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON body"}),
            status_code=400,
            mimetype="application/json",
            headers=cors_headers,
        )

    # ── Validate required fields ──────────────────────────────────
    required = ["thumb", "question", "answer"]
    missing  = [f for f in required if not body.get(f)]
    if missing:
        return func.HttpResponse(
            json.dumps({"error": f"Missing required fields: {', '.join(missing)}"}),
            status_code=400,
            mimetype="application/json",
            headers=cors_headers,
        )

    if body["thumb"] not in ("up", "down"):
        return func.HttpResponse(
            json.dumps({"error": "thumb must be 'up' or 'down'"}),
            status_code=400,
            mimetype="application/json",
            headers=cors_headers,
        )

    # ── Build record ──────────────────────────────────────────────
    record = {
        "timestamp":     datetime.now(timezone.utc).isoformat(),
        "thumb":         body["thumb"],
        "deck":          body.get("deck", ""),
        "certification": body.get("certification", ""),
        "category":      body.get("category", ""),
        "group":         body.get("group", ""),
        "difficulty":    body.get("difficulty", ""),
        "question":      body["question"],
        "answer":        body["answer"],
        "note":          body.get("note", ""),
    }
    logging.info('Saving feedback record: %s', json.dumps(record))

    # ── Append to blob ────────────────────────────────────────────
    try:
        client = get_blob_client()
        line   = json.dumps(record) + "\n"

        try:
            existing = client.download_blob().readall().decode("utf-8")
            client.upload_blob(existing + line, overwrite=True)
        except Exception:
            # Blob doesn't exist yet — create it
            client.upload_blob(line, overwrite=True)

    except Exception as e:
        logging.error("Blob write failed: %s", e)
        return func.HttpResponse(
            json.dumps({"error": "Failed to save feedback"}),
            status_code=500,
            mimetype="application/json",
            headers=cors_headers,
        )

    return func.HttpResponse(
        json.dumps({"ok": True}),
        status_code=200,
        mimetype="application/json",
        headers=cors_headers,
    )


# ─── ENDPOINT 2: Code Validation Engine ───────────────────────────
@app.route(route="validate_code", methods=["POST", "OPTIONS"])
def validate_code(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing code validation request.')

    # ── CORS preflight ────────────────────────────────────────────
    allowed_origin = os.environ.get("ALLOWED_ORIGIN", "*")
    cors_headers = {
        "Access-Control-Allow-Origin":  allowed_origin,
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers=cors_headers)

    # ── Parse body ────────────────────────────────────────────────
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON body"}),
            status_code=400,
            mimetype="application/json",
            headers=cors_headers,
        )

    code_string = req_body.get('query') or req_body.get('code')
    language = req_body.get('language', 'snowflake').lower()

    if not code_string:
        return func.HttpResponse(
             json.dumps({"error": "Please provide a 'code' or 'query' string in the JSON body."}),
             status_code=400,
             mimetype="application/json",
             headers=cors_headers
        )

    response_payload = {"is_valid": True, "errors": []}

    try:
        # ─── 1. SQL & dbt Validation (via SQLFluff) ───
        if language in ['sql', 'snowflake', 'bigquery', 'postgres', 'dbt']:
            dialect = 'ansi' if language == 'sql' else ('snowflake' if language == 'dbt' else language)
            
            # If it's dbt, use the Jinja templater so SQLFluff ignores {{ ref() }} tags
            templater = 'jinja' if language == 'dbt' else 'jinja'
            
            try:
                lint_results = sqlfluff.lint(code_string, dialect=dialect, templater=templater)
                response_payload["is_valid"] = len(lint_results) == 0
                response_payload["errors"] = lint_results
            except Exception as e:
                 response_payload["is_valid"] = False
                 response_payload["errors"] = [{"description": f"Linter error: {str(e)}"}]

        # ─── 2. Python Validation (via built-in AST) ───
        elif language == 'python':
            try:
                ast.parse(code_string)
            except SyntaxError as e:
                response_payload["is_valid"] = False
                response_payload["errors"] = [{"line": e.lineno, "description": f"Syntax Error: {e.msg}"}]

        # ─── 3. YAML Validation (via PyYAML) ───
        elif language in ['yaml', 'yml']:
            try:
                yaml.safe_load(code_string)
            except yaml.YAMLError as e:
                response_payload["is_valid"] = False
                response_payload["errors"] = [{"description": str(e)}]

        # ─── 4. Jinja2 Validation (via jinja2 Environment) ───
        elif language in ['jinja', 'jinja2']:
            try:
                env = Environment()
                env.parse(code_string)
            except TemplateSyntaxError as e:
                response_payload["is_valid"] = False
                response_payload["errors"] = [{"line": e.lineno, "description": e.message}]

        else:
            return func.HttpResponse(
                 json.dumps({"error": f"Validation for language '{language}' is not supported."}),
                 status_code=400,
                 mimetype="application/json",
                 headers=cors_headers
            )

        return func.HttpResponse(
             json.dumps(response_payload),
             status_code=200,
             mimetype="application/json",
             headers=cors_headers
        )

    except Exception as e:
        logging.error(f"Validation error: {str(e)}")
        return func.HttpResponse(
             json.dumps({"error": str(e)}), 
             status_code=500, 
             mimetype="application/json",
             headers=cors_headers
        )