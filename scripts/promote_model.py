# promote model

import os
import mlflow

def promote_model():
    # Set up DagsHub credentials for MLflow tracking
    dagshub_token = os.getenv("CAPSTONE_TEST")
    if not dagshub_token:
        raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    dagshub_url = "https://dagshub.com"
    repo_owner = "turvashsingh"
    repo_name = "Capstone_Project"

    # Set up MLflow tracking URI
    mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

    client = mlflow.MlflowClient()
    model_name = "my_model"

    # Get the latest version in "Staged"
    staged_versions = client.get_latest_versions(model_name, stages=["Staged"])
    if not staged_versions:
        print(f"No model found in 'Staged' stage for '{model_name}'.")
        return
    latest_version_staged = staged_versions[0].version

    # Archive all current production models
    prod_versions = client.get_latest_versions(model_name, stages=["Production"])
    for version in prod_versions:
        client.transition_model_version_stage(
            name=model_name,
            version=version.version,
            stage="Archived"
        )
        print(f"Archived previous Production model version: {version.version}")

    # Promote the new model to Production
    client.transition_model_version_stage(
        name=model_name,
        version=latest_version_staged,
        stage="Production"
    )
    print(f"✅ Model version {latest_version_staged} promoted to Production successfully!")

if __name__ == "__main__":
    promote_model()
