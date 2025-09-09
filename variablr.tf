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

# Variable for the VM instance name
variable "vm_name" {
  description = "The name of the VM instance."
  type        = string
  default     = "cli-vm"
}

# Variable for the VM machine type
variable "machine_type" {
  description = "The machine type for the VM instance."
  type        = string
  default     = "n2-standard-2"
}

# Variable for SSH source ranges
variable "ssh_source_ranges" {
  type        = list(string)
  description = "The source IP ranges to allow for SSH access."
  default     = ["0.0.0.0/0"]
}