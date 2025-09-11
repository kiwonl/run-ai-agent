resource "google_artifact_registry_repository" "docker-repo" {
  project       = var.project_id
  repository_id = var.docker_repository_id
  location      = var.region
  format        = "DOCKER"
  description   = "Docker repository created via Terraform"
}
