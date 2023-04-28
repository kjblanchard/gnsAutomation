resource "null_resource" "gns_instance_inventory" {

  triggers = {
    mytest = timestamp()
  }

  provisioner "local-exec" {
    command = "echo [tf] > inventory && echo ${aws_instance.gns_instance.tags.Name} ansible_host=${aws_instance.gns_instance.public_ip} ansible_user=ec2-user ansible_ssh_private_key_file=/root/xyz.pem >> inventory"
  }


  depends_on = [
    aws_instance.gns_instance
  ]

}
