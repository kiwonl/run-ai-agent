# Terraform block to define required providers
# 사용할 Terraform 공급자를 정의합니다.
# 이 경우 Google Cloud 공급자(hashicorp/google)를 사용하며, 버전은 5.0 이상을 요구합니다.
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# Provider block to configure the Google Cloud provider
# Google Cloud 공급자를 설정합니다.
# var.project_id와 var.region 변수를 사용하여 프로젝트 ID와 리전을 지정합니다.
provider "google" {
  project = var.project_id
  region  = var.region
}