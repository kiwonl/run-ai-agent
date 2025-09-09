# MCP Servers 배포

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

## 1. Terraform 설치

```bash
terraform init
```
```bash
terraform plan
```
```bash
terraform apply
```

## Terraform 으로 생성되는 리소스
*   **`google_project_service`**: 다음 API를 활성화합니다.
    *   `dns.googleapis.com`
    *   `aiplatform.googleapis.com`
    *   `servicedirectory.googleapis.com`
*   **`google_compute_network`**: `gemini-vpc-net`이라는 이름의 VPC 네트워크를 생성합니다.
*   **`google_compute_subnetwork`**: `vm1-subnet`이라는 이름의 서브넷을 생성합니다. Private Google Access 를 활성화 하여 Gemini 로의 호출을 Private Connection 을 유지합니다.
*   **`google_compute_global_address`**: `gemini-ip` 라는 이름의 Private Service Connect 용 내부 IP 주소를 생성합니다.
*   **`google_compute_global_forwarding_rule`**: `pscgemini` 라는 이름의 Private Service Connect 전달 규칙을 생성합니다.
*   **`google_dns_managed_zone`**: `googleapis.com`에 대한 `googleapis-private` 라는 이름의 비공개 DNS 영역을 생성합니다.
*   **`google_dns_record_set`**: 
    *   `googleapis.com`에 대한 A 레코드를 생성합니다.
    *   `*.googleapis.com`에 대한 CNAME 레코드를 생성합니다.

C권한 설정
```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member=user:$(gcloud config get-value account) \
    --role='roles/run.invoker'
```

MCP client 인증을 위한 Token 생성

```bash
export PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")
export ID_TOKEN=$(gcloud auth print-identity-token)
```



## run-currency-mcp
```bash
cd ~/run-ai-agent/run-currency-mcp

gcloud run deploy run-currency-mcpexchange-mcp-server \
    --no-allow-unauthenticated \
    --region=${REGION} \
    --source=.
```

```bash
```

## run-weather-mcp
```bash
cd ~/run-ai/agent/run-weather-mcp

gcloud run deploy run-weather-mcp \
    --no-allow-unauthenticated \
    --region=${REGION} \
    --source=.
```

```bash
```

## run-travel-ai-agent