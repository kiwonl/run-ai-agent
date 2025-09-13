# Cloud Run 을 위한 Google Cloud 서비스 계정을 생성
resource "google_service_account" "sa" {
  project      = var.project_id
  account_id   = var.run_service_account
  display_name = "google_service_account"
}

# Cloud Run 서비스 계정에 AI 플랫폼 사용자 역할을 부여합니다.
resource "google_project_iam_member" "ai_platform_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.sa.email}"
}

# Cloud Run 서비스 계정에 Cloud Run 호출자 역할을 부여합니다.
resource "google_project_iam_member" "run_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.sa.email}"
}

# Cloud Build 서비스 계정에 Cloud Run 관리자 역할을 부여합니다.
resource "google_project_iam_member" "cloud_build_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

# Cloud Build 서비스 계정에 서비스 계정 사용자 역할을 부여합니다.
resource "google_project_iam_member" "cloud_build_service_account_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

# Cloud Build 서비스 계정에 작업을 실행할 권한을 부여합니다.
resource "google_project_iam_member" "cloud_build_builds_builder" {
  project = var.project_id
  role    = "roles/cloudbuild.builds.builder"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}