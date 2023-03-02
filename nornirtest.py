from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

config_file = "./config.yml"
def netmiko_test(task):
    task.run(task=netmiko_send_command, command_string="show ip int brief | exc unass")


# # Body
if __name__ == "__main__":
    nr = InitNornir(config_file=config_file)
    nr_access = nr.filter(role="access")
    results=nr.run(task=netmiko_test)
    print_result(results)
