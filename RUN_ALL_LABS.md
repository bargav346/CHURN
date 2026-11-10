# Run every lab in VS Code (Terminal > New Terminal, PowerShell)

Run all commands from the project root (the folder that contains config.yaml).

## 0. One-time setup
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pytest
# VS Code: Ctrl+Shift+P -> "Python: Select Interpreter" -> choose .\venv\Scripts\python.exe

## Lab 3 - Baseline pipeline
python .\pipelines\run_lab3_baseline.py

## Lab 4 - MLflow experiment tracking
python .\pipelines\run_lab4_tracking.py
mlflow ui            # open http://127.0.0.1:5000 (Ctrl+C to stop)

## Lab 5 - Production data pipeline
python .\pipelines\run_lab5_pipeline.py

## Lab 6 - Model registry and lifecycle
python .\pipelines\run_lab6_registry.py

## Lab 7 - Full ML pipeline (stages 01 to 09)
# new_churn.csv is already marked as ingested, so --force is required
python .\src\mlops_pipeline\churn_prediction_pipeline.py --force

## Lab 8 - Quality gate and CI
# the quality gate (07) already runs inside the Lab 7 pipeline
python -m json.tool .\reports\quality_gate_report.json
# CI itself runs on GitHub: push the repo, then Actions > "Lab 8 - MLOps CI" > Run workflow

## Lab 9 - Failure injection and recovery (needs Lab 7 done first)
python .\src\mlops_pipeline\10_failure_injection.py
python -m json.tool .\reports\failure_report.json

## Lab 10 - FastAPI serving, API tests, performance tests
python .\src\mlops_pipeline\11_prepare_deployment.py   # builds deployment/ from the MLflow Production model
pytest .\tests\test_api.py -v
python .\tests\test_performance.py
# interactive: run the API in one terminal, then open http://localhost:8000/docs
uvicorn api.main:app --host 0.0.0.0 --port 8000

## Lab 11 - Docker and Kubernetes (Docker Desktop with Kubernetes enabled)
docker build -t churn-prediction-api:1.0 .
docker run --name churn-api -p 8000:8000 churn-prediction-api:1.0
# new terminal:
python .\tests\test_local_vs_container.py
docker stop churn-api; docker rm churn-api
kubectl apply -f .\k8s\deployment.yaml
kubectl apply -f .\k8s\service.yaml
kubectl get pods
kubectl get service churn-api-service
kubectl scale deployment churn-api --replicas=3
# or the automated version:
python .\deployment\deploy_production.py

## Lab 12 - Drift monitoring and retraining (in this order)
python .\src\mlops_pipeline\12_create_evolved_dataset.py
python .\src\mlops_pipeline\12_create_concept_drift_dataset.py
python .\src\mlops_pipeline\12_data_drift.py
python .\src\mlops_pipeline\12_prediction_drift.py
python .\src\mlops_pipeline\12_concept_drift.py
python .\src\mlops_pipeline\12_drift_analysis.py
python .\src\mlops_pipeline\12_performance_monitoring.py
python .\src\mlops_pipeline\12_performance_trend.py
python .\src\mlops_pipeline\12_create_updated_dataset.py
python .\src\mlops_pipeline\12_retrain_model.py
python .\src\mlops_pipeline\12_model_comparison.py
python .\src\mlops_pipeline\12_update_mlflow_registry.py
# API-log monitoring (needs the API running and some requests sent, e.g. via the tests above):
python .\src\mlops_pipeline\12_request_history.py
python .\src\mlops_pipeline\12_prediction_monitoring.py
python .\src\mlops_pipeline\12_api_performance_monitoring.py

## Lab 13 - End-to-end monitoring trigger
python .\src\mlops_pipeline\12_monitor_trigger.py
python -m json.tool .\outputs\monitoring\monitor_trigger_report.json
# GitHub Actions workflows need a self-hosted Windows runner and a hard-coded path
# (C:\Users\jnane\Favorites\churn-prediction) - edit lab13_*.yml before using them.
