"""
Extension module for PIE that provides a powershell context to run commands within a local or remote powershell session.
"""
__VERSION__='0.0.3'


import base64
import shutil


from pie import CmdContextManager,CmdContext,cmd


class powershell(CmdContext):
    """
    A context class used to execute commands within a powershell session
    """
    def __init__(self,hostname=None,username=None,password=None):
        self.hostname=hostname
        self.username=username
        self.password=password
        self.commands=[]


    def cmd(self,c):
        # defer execution until the end of the context
        self.commands.append(c)


    def _escape(self,s):
        for fr,to in (('\x00','`0'),('\a','`a'),('\b','`b'),('\f','`f'),('\n','`n'),('\r','`r'),('\t','`t'),('\v','`v'),('\0','`0'),
                      ('"','`"'),('\'','`\''),('#','`#'),('`','``')):
            s=s.replace(fr,to)
        return s


    def _buildCmd(self):
        if self.hostname is None:
            c='\n'.join(self.commands)

        else:
            # make sure we stop on errors instead of ignore and continue
            c=['$ErrorActionPreference="Stop"']
            # connect to the remote session
            sessionCredentialArgs=''
            if self.username:
                c.append('$sp=ConvertTo-SecureString "%s" -AsPlainText -Force'%(self._escape(self.password)))
                c.append('$cred=New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList ("%s",$sp)'%(self._escape(self.username)))
                sessionCredentialArgs=' -Credential $cred -Authentication Credssp'
            c.append('$s=New-PSSession -ComputerName "%s"%s'%(self._escape(self.hostname),sessionCredentialArgs))
            c.append('')
            # execute commands in the remote session
            c.append('Invoke-Command -Session $s -ScriptBlock {')
            c.extend(['    '+s for s in self.commands])
            c.append('}')
            c='\n'.join(c)
        return c


    def __exit__(self,exc_type,exc_value,traceback):
        if exc_type is None:
            c=self._buildCmd()
            print('Executing powershell code:\n'+c)
            s=base64.b64encode(c.encode('utf-16le'))
            c='powershell -EncodedCommand {}'.format(s.decode('utf8'))
            CmdContextManager.cmd(c,self.contextPosition)
        else:
            print('An error occurred, not running powershell commands')
        super(powershell,self).__exit__(exc_type,exc_value,traceback)


    # ----------------------------------------
    # Additional functionality
    # ----------------------------------------
    @classmethod
    def put(cls,srcPath,destPath):
        """Convenience method to upload files - TODO: (if possible) currently not tied to the hostname parameter."""
        shutil.copy(srcPath,destPath)
