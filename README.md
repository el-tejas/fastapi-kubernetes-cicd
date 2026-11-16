# FastAPI Kubernetes CI/CD Demo

A small portfolio project that takes a FastAPI app from tests to a Docker image and a local Kubernetes deployment with Minikube.

## Cost and simplest learning path

This project does not need a cloud account, paid Kubernetes cluster, container registry, or paid deployment service. Python, FastAPI, Docker, Minikube, and `kubectl` are available at no cost. Minikube runs Kubernetes on your own computer, so it uses your computer's resources rather than creating a cloud bill.

GitHub Actions' standard hosted runners are free for public repositories. If you keep the repository private, check the Actions allowance for your GitHub plan before using it. Never make a repository public if it contains passwords, access tokens, personal information, or other private material.

For your first run, learn the GitHub-hosted CI workflow and deploy to Minikube with the local commands below. The optional self-hosted deployment workflow is an advanced step; you can ignore it and still learn how CI and Kubernetes work.

## GitHub in a few words

- A **repository** is the project and its files on GitHub.
- A **commit** is a saved snapshot of your changes.
- A **branch** is a separate line of work, so you can make changes without immediately changing `main`.
- A **pull request** asks to bring a branch's changes into `main`.
- **GitHub Actions** runs automation when an event happens. In this project it tests the code and builds a Docker image when you push to `main` or open a pull request.

Once this project is in your GitHub repository, open its **Actions** tab to see the `CI` workflow. To practice the normal workflow, make a small change on a branch, push it to GitHub, and open a pull request. GitHub will run the checks; after you merge the pull request into `main`, it runs them again. A green check means the tests and image build succeeded. It does not mean the app was deployed.

## What this project does

- Serves a welcome message at `/` and a health check at `/health`.
- Runs API tests and builds the Docker image on GitHub-hosted runners for pushes to `main` and pull requests.
- Can deploy to Minikube only when someone manually starts the optional deployment workflow from `main` on a configured self-hosted runner.

GitHub-hosted runners cannot connect to Minikube running on your own computer. The deployment workflow therefore uses a self-hosted Linux runner on the machine that can access your Minikube cluster. CI and pull-request validation stay on GitHub-hosted runners.

## Run the app and tests locally

You need Python 3.12 or newer.

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs> for the interactive API documentation, or visit <http://127.0.0.1:8000/health>.

## Build and run with Docker

```bash
docker build -t fastapi-kubernetes-cicd:local .
docker run --rm -p 8000:8000 fastapi-kubernetes-cicd:local
```

Visit <http://127.0.0.1:8000/health>.

## Deploy locally to Minikube

You need Docker, `kubectl`, and Minikube installed.

```bash
minikube start
minikube image build -t fastapi-kubernetes-cicd:local .
kubectl apply -f k8s/
kubectl rollout status deployment/fastapi-api
kubectl port-forward service/fastapi-api 8000:80
```

While port-forwarding is running, visit <http://127.0.0.1:8000/health>. Stop port-forwarding with Ctrl+C. To remove the app, run `kubectl delete -f k8s/`.

## GitHub Actions

`.github/workflows/ci.yml` runs tests and builds the container on GitHub-hosted runners. It runs for pull requests and pushes to `main`; it does not deploy.

### Advanced optional step: automatic deployment to your Minikube

The deploy workflow is intentionally separate from CI. It has no pull-request trigger, runs only when manually started from `main`, and requires a self-hosted runner labeled `self-hosted`, `linux`, and `minikube`. The runner must be installed on a Linux machine with `minikube` and `kubectl` on `PATH`, and must already have access to the intended Minikube cluster. You do not need this workflow to learn the project; deploy locally with the commands above first.

1. Set up a dedicated self-hosted runner for this repository on the Minikube machine and give it the `minikube` label.
2. In repository **Settings → Environments**, create an environment named `minikube`. Consider adding required reviewers and deployment branch restrictions.
3. In **Actions**, select **Deploy to Minikube → Run workflow**, choose `main`, and start the run.

The job builds the image into Minikube, applies the manifests, and waits for the rollout. No registry or deployment credentials are needed. Do not use this runner for pull-request workflows: self-hosted runners can access the host machine and cluster, so only run trusted code from `main` on it. If you do not want to maintain a self-hosted runner, use the local Minikube commands above instead.
