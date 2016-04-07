import base64
import shutil


from pie import CmdContextManager,CmdContext,cmd


class powershell(CmdContext):
    """
    A context class used to execute commands within a powershell session
    """
    def __init__(self,hostname=None):
        self.hostname=hostname
        self.commands=[]


    def cmd(self,c):
        # defer execution until the end of the context
        self.commands.append(c)


    def _buildCmd(self):
        if self.hostname is None:
            c='\n'.join(self.commands)
        else:
            c='''\
$ErrorActionPreference="Stop"
$s=New-PSSession -ComputerName %s

Invoke-Command -Session $s -ScriptBlock {
%s
}
    '''%(self.hostname,'\n'.join(['    '+s for s in self.commands]))
        return c


    def __exit__(self,exc_type,exc_value,traceback):
        if exc_type is None:
            c=self._buildCmd()
            print('Executing powershell code:\n'+c)
            s=base64.b64encode(c.encode('utf-16le'))
            c='powershell -EncodedCommand {}'.format(s)
            return CmdContextManager.cmd(c,self.contextPosition)
        else:
            print('An error occurred, not running powershell commands')


    # ----------------------------------------
    # Additional functionality
    # ----------------------------------------
    @classmethod
    def put(cls,srcPath,destPath):
        """Convenience method to upload files - TODO: (if possible) currently not tied to the hostname parameter."""
        shutil.copy(srcPath,destPath)
