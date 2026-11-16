from fastapi import FastAPI

app = FastAPI(title="FastAPI Kubernetes CI/CD Demo")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "FastAPI Kubernetes CI/CD demo"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
