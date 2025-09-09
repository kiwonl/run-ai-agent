# 이 파일의 변수들을 자신의 Google Cloud 환경에 맞게 수정해주세요.

# Google Cloud Project ID
project_id = "your-gcp-project-id"

# Google Cloud Region
region = "us-central1"

# VPC Network ID
network_id = "gemini-vpc-net"

# VM instance name
vm_name = "cli-vm"

# VM machine type
machine_type = "n2-standard-2"

# Source IP ranges for SSH access. For better security, specify your IP range.
# 예: ["203.0.113.0/24"]
ssh_source_ranges = ["0.0.0.0/0"]