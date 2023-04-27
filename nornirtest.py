from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
# Use this for advanced filtering.
from nornir.core.filter import F

config_file = "./config.yml"
def netmiko_test(task):
    task.run(task=netmiko_send_command, command_string="show ip int brief | exc unass", delay_factor=4)


# # Body
if __name__ == "__main__":
    nr = InitNornir(config_file=config_file)
    nr_access = nr.filter(group="telnet")
    results=nr_access.run(task=netmiko_test)
    print_result(results)
