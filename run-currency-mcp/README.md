# currency-mcp-server on Cloud Run

## 배포
1. API 활성화 (Cloud Run, Artifact Registry, Cloud Build)
```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com
```

2. 환경변수 설정
```bash
export RUN_SERVICE_ACCOUNT=run-ai-agent-sa
export RUN_NETWORK=run-ai-agent-vpc
export RUN_SUBNET=run-ai-agent-subnet

export ID_TOKEN=$(gcloud auth print-identity-token)
```

3. Cloud Run 에 배포
```bash
gcloud run deploy run-currency-mcp-server \
    --source . \
    --region ${REGION} \
    --service-account ${RUN_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
    --no-allow-unauthenticated \
    --network=${RUN_NETWORK} \
    --subnet=${RUN_SUBNET} \
    --vpc-egress=all-traffic
```

## 2. Cloud Shell 환경의 Gemini CLI 에서 테스트
1. 호출 권한 추가
```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member=user:$(gcloud config get-value account) \
    --role='roles/run.invoker'
```

2. Gemini CLI 에 mcp-server 설정
```bash
cat <<EOF > ~/.gemini/settings.json
{
  "selectedAuthType": "cloud-shell", // only cloudshell
  "mcpServers": {
    "exchange-mcp-server": {
      "httpUrl": "https://exchange-mcp-server-\$PROJECT_NUMBER.us-central1.run.app/mcp/",
      "headers": {
        "Authorization": "Bearer \$ID_TOKEN"
      }
    }
  }
}
EOF
```

# Reference
Qwiklabs : https://explore.qwiklabs.com/authoring/labs/192218

Codelab : 