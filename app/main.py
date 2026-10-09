from fastapi import FastAPI

app = FastAPI(
    title="AI Job Research & Resume Agent",
    version="0.1.0",
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-job-research-agent",
        "version": "0.1.0",
    }

#test comment