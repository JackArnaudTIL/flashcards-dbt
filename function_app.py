import azure.functions as func
import json
import logging
import os
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

CONTAINER_NAME = "feedback"
BLOB_NAME       = "feedback.jsonl"


def get_blob_client():
    conn_str = os.environ["FEEDBACK_STORAGE_CONNECTION_STRING"]
    service  = BlobServiceClient.from_connection_string(conn_str)
    return service.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)


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