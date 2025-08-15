# Approval Flow Prediction API

A Flask-based API deployed on Azure App Service to predict approval flows for requests.

## Endpoint
POST /predict

### Example Request
```bash
curl -X POST https://your-app-name.azurewebsites.net/predict \
  -H "Content-Type: application/json" \
  -d '{"request_type": "Infra", "description": "Provision new production VM"}'

