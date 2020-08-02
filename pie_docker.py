"""
Python3.6+ only
"""
from pie import *



class Docker:
    def __init__(self,options=None):
        self.options=list(options) if options is not None else []


    def build(self,context,options=None):
        """
        Builds a command and runs it like this:
        docker <self.options> build <options> <context>
        """
        ops=list(options) if options is not None else []
        ops.append(context)
        self.cmd('build',ops)

    def run(self,image,cmd_and_args=None,options=None):
        """
        Builds a command and runs it like this:
        docker <self.options> run <options> <image> <cmd_and_args>
        """
        ops=list(options) if options is not None else []
        ops.append(image)
        if cmd_and_args:
            ops.append(cmd_and_args)
        self.cmd('run',ops)

    def exec(self,container,cmd_and_args=None,options=None):
        """
        Builds a command and runs it like this:
        docker <self.options> exec <options> <container> <cmd_and_args>
        """
        ops=list(options) if options is not None else []
        ops.append(container)
        if cmd_and_args:
            ops.append(cmd_and_args)
        self.cmd('exec',ops)

    def stop(self,containers,options=None):
        """
        Builds a command and runs it like this:
        docker <self.options> stop <options> <containers>
        """
        ops=list(options) if options is not None else []
        if isinstance(containers,str):
            containers=[containers]
        ops.extend(containers)
        self.cmd('stop',ops)

    def volume_create(self,name,options=None):
        ops=list(options) if options is not None else []
        ops.append(name)
        self.cmd('volume create',ops)

    def volume_rm(self,name,options=None):
        ops=list(options) if options is not None else []
        ops.append(name)
        self.cmd('volume rm',ops)

    def cmd(self,docker_cmd,cmd_options=None):
        """
        Builds a command and runs it like this:
        docker <self.options> <docker_cmd> <cmd_options>
        """
        docker_options_str=' '.join(self.options)
        cmd_options_str=' '.join(cmd_options) if cmd_options is not None else ''
        c=f'docker {docker_options_str} {docker_cmd} {cmd_options_str}'
        print(c)
        cmd(c)
