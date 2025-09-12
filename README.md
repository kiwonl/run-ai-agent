# AI Agent 인프라 환경 세팅

## 환경설정

환경변수 설정
```bash
export PROJECT_ID=
export REGION=us-central1
```

terraform.tfvars 파일 업데이트
```bash
cd ~/run-ai-agent/terraform

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

Outputs:
```
network_name = "run-ai-agent-vpc"
service_account_account_id = "run-ai-agent-sa"
service_account_display_name = "google_service_account"
service_account_email = "run-ai-agent-sa@qwiklabs-gcp-02-c885537ad9e1.iam.gserviceaccount.com"
subnetwork_name = "run-ai-agent-subnet"
```

### 생성되는 리소스

- **google_project_service**
  - `servicedirectory.googleapis.com`
  - `dns.googleapis.com`
  - `run.googleapis.com`
  - `aiplatform.googleapis.com`
  - `artifactregistry.googleapis.com`
  - `cloudbuild.googleapis.com`
- **google_project_iam_member**
  - `cloud_build_run_admin`
  - `cloud_build_builds_builder`
  - `cloud_build_service_account_user`
  - `ai_platform_user`
- **google_compute_network**: `default`
- **google_service_account**: `sa`
- **google_compute_global_address**: `default`
- **google_compute_subnetwork**: `default`
- **google_compute_router**: `default`
- **google_dns_managed_zone**: `private_zone`
- **google_dns_record_set**
  - `cname_record`
  - `a_record`
- **google_compute_global_forwarding_rule**: `default`
- **google_compute_router_nat**: `default`

MCP client 인증을 위한 Token 생성

```bash
export RUN_SERVICE_ACCOUNT=run-ai-agent-sa
export RUN_NETWORK=run-ai-agent-vpc
export RUN_SUBNET=run-ai-agent-subnet

export PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")
```

# Zoo MCP server 배포
```bash
cd ~/run-ai-agent/

gcloud run deploy zoo-mcp-server \
    --source ./zoo-mcp-server/ \
    --region ${REGION} \
    --service-account ${RUN_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
    --no-allow-unauthenticated \
    --network=${RUN_NETWORK} \
    --subnet=${RUN_SUBNET} \
    --vpc-egress=all-traffic
```
# Google ADK 설치
https://google.github.io/adk-docs/get-started/installation/
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install google-adk
```

# AI Agent 배포
```bash
adk deploy cloud_run \
  --project=${PROJECT_ID} \
  --region=${REGION} \
  --service_name=zoo-tour-guide \
  --with_ui \
  .

gcloud run services update travel-ai-agent \
  --region=${REGION} \
  --service-account ${RUN_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
  --network=${RUN_NETWORK} \
  --subnet=${RUN_SUBNET}  \
  --vpc-egress=all-traffic
```


Reference
- MCP Server: https://codelabs.developers.google.com/codelabs/cloud-run/how-to-deploy-a-secure-mcp-server-on-cloud-run?hl=ko#6
- AI Agent : https://codelabs.developers.google.com/codelabs/cloud-run/use-mcp-server-on-cloud-run-with-an-adk-agent?hl=ko#0
