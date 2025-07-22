from fastapi import FastAPI
import LivekitFeatures

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Prewarm the process with necessary data
    LivekitFeatures.prewarm(LivekitFeatures.JobProcess())



