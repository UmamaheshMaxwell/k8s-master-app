# Step 1: Build the Docker image
DOCKERFILE_PATH="Dockerfile"

docker build -f "$DOCKERFILE_PATH" -t us-east1-docker.pkg.dev/gke-projects-443614/artifacts-python/fastapi-auth:latest .

# Step 2: Push the Docker image to Google Container Registry
docker push us-east1-docker.pkg.dev/gke-projects-443614/artifacts-python/fastapi-auth:latest


