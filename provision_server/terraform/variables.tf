variable "tags" {
  default = {
    CreatedBy = "gns_provisioner"
  }
}

variable "ami_id" {
}

variable "instance_size" {
}

variable "subnet_id" {
}

variable "keypair_location" {
}
variable "public_ip_url" {
}

variable "security_group_rules" {
  default = [
    {
      protocol    = "icmp",
      from_port   = -1,
      to_port     = -1,
      description = "ICMP"
    },
    {
      protocol    = "tcp",
      from_port   = 8003,
      to_port     = 8003,
      description = "8003"
    },
    {
      protocol    = "tcp",
      from_port   = 22,
      to_port     = 22,
      description = "ssh"
    },
    {
      protocol    = "udp",
      from_port   = 1194,
      to_port     = 1194,
      description = "1194"
    }
  ]
}
