import mlflow

mlflow.set_tracking_uri("https://dagshub.com/turvashsingh/Capstone_Project.mlflow")

with mlflow.start_run() as run:
    mlflow.log_param("sanity", True)
    mlflow.log_metric("num", 1)
    print("Run id:", run.info.run_id)

