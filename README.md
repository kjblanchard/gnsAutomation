# Goon GNS
Provision a gns server for remote config, and build a network with nornir.

## Remote Gns Server
- Gns server is remote in aws, and created with Terraform, configured with ansible.
- Use OpenVPN to connect to the instance
- Configured with TAP and pushes a specific route to your pc when connecting to OpenVPN
- Backend is remote by default, and you will either need to update the backend.tf, or create your own tfbackend file and use that when initializing terraform (which is what I do)


## Setup GNS server
- Create a tfbackend file for remote state, or delete the backend.tf file and use local state.
- SSH to the box with a typical ssh command, with the ubuntu username specified
```bash
ssh ubuntu@3.144.81.203
```

## Requirements
- A ssh key generated, will default to id_rsa_pub
- Basic knowledge of Terraform and Ansible
- Unix like environment: WSL, gitbash, macos/linux (mainly for creating the inventory file with the command in ansible_inventory, could likely change that and be fine, also it may just work in powershell)