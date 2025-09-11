# AI Agent 인프라 환경 세팅

## 환경설정

환경변수 설정
```bash
export PROJECT_ID=         //qwiklabs-gcp-00-90a5c37a7501
export REGION=us-central1
```

terraform.tfvars 파일 업데이트
```bash
sed -i \
-e "s/your-gcp-project-id/$PROJECT_ID/" \
-e "s/your-region/$REGION/" \
terraform.tfvars
```

## Terraform

```bash
terraform init
```
```bash
terraform plan
```
```bash
terraform apply
```

# MCP Servers 배포

MCP client 인증을 위한 Token 생성

```bash
export RUN_SERVICE_ACCOUNT=run-ai-agent-sa
export RUN_NETWORK=run-ai-agent-vpc
export RUN_SUBNET=run-ai-agent-subnet

export PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")
export ID_TOKEN=$(gcloud auth print-identity-token)
```

## run-currency-mcp
```bash
cd ~/run-ai-agent/run-currency-mcp
gcloud run deploy run-currency-mcp-server \
    --source . \
    --region ${REGION} \
    --service-account ${RUN_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
    --no-allow-unauthenticated \
    --network=${RUN_NETWORK} \
    --subnet=${RUN_SUBNET} \
    --vpc-egress=all-traffic
```

## run-weather-mcp
```bash
cd ~/run-ai-agent/run-weather-mcp
gcloud run deploy currency-mcp-server \
    --source . \
    --region ${REGION} \
    --no-allow-unauthenticated \
    --service-account ${RUN_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
    --network=${RUN_NETWORK} \
    --subnet=${RUN_SUBNET} \
    --vpc-egress=all-traffic
```

## ai-travel-agent
```bash
cd ~/run-ai-agent/run-weather-mcp

adk deploy cloud_run \
  --project=${PROJECT_ID} \
  --region=${REGION} \
  --service_name=travel-ai-agent \
  --with_ui \
  .

gcloud run services update travel-ai-agent \
  --region=europe-west1 \
  --update-labels=dev-tutorial=codelab-adk
  --no-allow-unauthenticated \
  --network=${RUN_NETWORK} \
  --subnet=${RUN_SUBNET} \
```


python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

