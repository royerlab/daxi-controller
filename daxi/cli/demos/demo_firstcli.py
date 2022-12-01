from click.testing import CliRunner
from daxi.cli.firstcli import acquire
from daxi.globals_configs_constants_general_tools_needbettername.constants import process_configs_yaml_path


def demo_firstcli_acquire(process_configs_path):
  runner = CliRunner()
  result = runner.invoke(acquire, ['-c', process_configs_path])
  print(result)
  return 'successful'


if __name__ == '__main__':
    print('called as a main:')
    demo_firstcli_acquire(process_configs_path=process_configs_yaml_path)
