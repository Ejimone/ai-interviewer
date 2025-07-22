from fastapi import FastAPI
from LivekitFeatures import *

app = FastAPI()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
