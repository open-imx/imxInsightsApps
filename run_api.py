import uvicorn

from imxInsightsApps.api.main import api_app

if __name__ == "__main__":
    uvicorn.run(api_app, host="127.0.0.1", port=8004, reload=False)
