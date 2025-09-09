# Enable necessary Google Cloud APIs for the project
# for_each를 사용하여 지정된 Google Cloud API 목록을 프로젝트에서 활성화합니다.
# 각 API는 특정 Google Cloud 서비스를 사용하기 위해 필요합니다.
resource "google_project_service" "default" {
  for_each = toset([
    "dns.googleapis.com",             # Google Cloud DNS API
    "aiplatform.googleapis.com",      # Vertex AI API
    "servicedirectory.googleapis.com" # Service Directory API
  ])

  service            = each.value
  disable_on_destroy = false
}