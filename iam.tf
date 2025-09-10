# 이 Terraform 코드는 Google Cloud 서비스 계정을 생성하고 해당 계정에 AI 플랫폼 사용자 역할을 부여합니다.
resource "google_service_account" "sa" {
  project      = var.project_id
  account_id   = var.gcp_service_account
  display_name = "our famous recommendation service"
}

resource "google_project_iam_member" "ai_platform_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.sa.email}"
}
