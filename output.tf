# Output for the name of the created VM instance
# 생성된 VM 인스턴스의 이름을 출력합니다.
output "vm_name" {
  description = "The name of the VM instance."
  value       = google_compute_instance.vm1.name
}

# Output for the name of the VPC network
# 생성된 VPC 네트워크의 이름을 출력합니다.
output "network_name" {
  description = "The name of the VPC network."
  value       = google_compute_network.default.name
}

# Output for the name of the subnetwork
# 생성된 서브넷의 이름을 출력합니다.
output "subnetwork_name" {
  description = "The name of the subnetwork."
  value       = google_compute_subnetwork.default.name
}