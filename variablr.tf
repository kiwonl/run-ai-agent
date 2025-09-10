# Variable for the Google Cloud project ID
variable "project_id" {
  type        = string
  description = "The ID of the Google Cloud project."
  default     = "your-gcp-project-id"
}

# Variable for the Google Cloud region
variable "region" {
  description = "The region for the resources."
  type        = string
  default     = "us-central1"
}

# Variable for the VPC network ID
variable "network_id" {
  type        = string
  description = "The ID of the VPC network."
  default     = "gemini-vpc-net"
}