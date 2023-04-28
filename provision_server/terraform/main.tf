data "http" "public_ip" {
  url = var.public_ip_url
}

locals {
  public_ip = "${trimspace(data.http.public_ip.response_body)}/32"

}

resource "aws_ebs_volume" "myvol" {
  availability_zone = aws_instance.gns_instance.availability_zone
  size              = 20
  tags = {
    Name = "gns_ebs"
  }
}

resource "aws_security_group" "gns_allow_initial_ssh" {
  name        = "Gns required Traffic"
  description = "Allow gns traffic from my IP"
  #   vpc_id      = aws_vpc.main.id

  dynamic "ingress" {
    for_each = var.security_group_rules
    content {
      description = ingress.value.description
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = [local.public_ip]
    }
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "Gns Required Traffic"
  }
}


resource "aws_volume_attachment" "gns_ebs_attachment" {
  force_detach = true
  device_name  = "/dev/sdh"
  volume_id    = aws_ebs_volume.myvol.id
  instance_id  = aws_instance.gns_instance.id
}

resource "aws_network_interface" "gns_interface" {
  subnet_id       = var.subnet_id
  security_groups = [aws_security_group.gns_allow_initial_ssh.id]
  tags = {
    Name = "gns_network_interface"
  }
}

resource "aws_instance" "gns_instance" {
  ami           = var.ami_id
  instance_type = var.instance_size

  network_interface {
    network_interface_id = aws_network_interface.gns_interface.id
    device_index         = 0
  }
  key_name = aws_key_pair.gns_keypair.key_name
  tags = {
    Name = "gns_instance"
  }
}

resource "aws_key_pair" "gns_keypair" {
  key_name   = "gns_keypair"
  public_key = file(var.keypair_location)
}
