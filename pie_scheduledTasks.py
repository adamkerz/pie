"""
Extension module for PIE that allows manipulation of scheduled tasks. These must be run within a powershell context, and therefore, require pie_powershell.
"""
__VERSION__='0.0.1'


from pie import *


class scheduledTasks(object):
    @classmethod
    def configure(cls,folder,name,command,arguments,workingDir,username,password,scheduledTaskTriggerArguments):
        cmd('$action = New-ScheduledTaskAction -Execute "%s" -Argument "%s" -WorkingDirectory "%s"'%(command,arguments,workingDir))
        cmd('$trigger = New-ScheduledTaskTrigger %s'%(scheduledTaskTriggerArguments,))
        cmd('$settingsSet = New-ScheduledTaskSettingsSet -Compatibility Win8')

        cmd('$task = Get-ScheduledTask -ErrorAction Ignore -TaskPath "%s" -TaskName "%s"'%(folder,name))
        cmd('''If($task -ne $Null){
            $task.Actions = $action
            $task.Triggers = $trigger
            $task.Settings = $settingsSet
            Set-ScheduledTask -InputObject $task -User "%s" -Password "%s"
        }Else{
            Register-ScheduledTask -TaskPath "%s" -TaskName "%s" -User "%s" -Password "%s" -Action $action -Trigger $trigger -Settings $settingsSet
        }'''%(username,password,folder,name,username,password))


    @classmethod
    def enable(cls,folder,name):
        cmd('Enable-ScheduledTask -ErrorAction Ignore -TaskPath "%s" -TaskName "%s"'%(folder,name))


    @classmethod
    def disable(cls,folder,name):
        cmd('Disable-ScheduledTask -ErrorAction Ignore -TaskPath "%s" -TaskName "%s"'%(folder,name))


    @classmethod
    def start(cls,folder,name):
        cmd('Start-ScheduledTask -TaskPath "%s" -TaskName "%s"'%(folder,name))
