from pie import *


@task
def testPs():
    from pie_powershell import powershell
    # TODO: needs real values, but how to do that for any tester?
    with powershell('windowsBox'):
        cmd(r'[Environment]::SetEnvironmentVariable("Path","D:\Python27;D:\Python27\Scripts;"+$env:Path,[System.EnvironmentVariableTarget]::Process)')
        with venv(r'd:\projectA\venv'):
            pip('list')
