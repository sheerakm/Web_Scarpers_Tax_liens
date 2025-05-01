from fastapi import FastAPI
from Nevada.dummy_task  import * # either find all scrapers automaticllay or add to a list

app = FastAPI()

@app.get("/run-script/{script_id}")
async def trigger_scraper(script_id: int):
    result = run_scraper.delay(script_id)
    return {"task_id": result.id}
