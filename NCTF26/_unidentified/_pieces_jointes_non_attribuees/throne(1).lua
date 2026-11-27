wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.body = os.getenv("CLAIM_BODY")
