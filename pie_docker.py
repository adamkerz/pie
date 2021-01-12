"""
Python3.6+ only
"""
__VERSION__='0.0.2'


from pie import *


def _make_list_parameter_safe(ls):
    return list(ls) if ls is not None else []


class Docker:
    def __init__(self,options=None):
        self.options=_make_list_parameter_safe(options)


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


    def build(self,context,options=None):
        """
        Builds a command and runs it like this:
        docker <self.options> build <options> <context>
        """
        ops=_make_list_parameter_safe(options)
        ops.append(context)
        self.cmd('build',ops)

    def run(self,image,cmd_and_args=None,options=None):
        """
        Builds a command and runs it like this:
        docker <self.options> run <options> <image> <cmd_and_args>
        """
        ops=_make_list_parameter_safe(options)
        ops.append(image)
        if cmd_and_args:
            ops.append(cmd_and_args)
        self.cmd('run',ops)

    def exec(self,container,cmd_and_args=None,options=None):
        """
        Builds a command and runs it like this:
        docker <self.options> exec <options> <container> <cmd_and_args>
        """
        ops=_make_list_parameter_safe(options)
        ops.append(container)
        if cmd_and_args:
            ops.append(cmd_and_args)
        self.cmd('exec',ops)

    def stop(self,containers,options=None):
        """
        Builds a command and runs it like this:
        docker <self.options> stop <options> <containers>
        """
        ops=_make_list_parameter_safe(options)
        if isinstance(containers,str):
            containers=[containers]
        ops.extend(containers)
        self.cmd('stop',ops)


    class Volume:
        """
        Named volume commands
        """
        def __init__(self,docker_obj,name):
            self.docker_obj=docker_obj
            self.name=name

        def create(self,options=None):
            ops=_make_list_parameter_safe(options)
            ops.append(self.name)
            self.docker_obj.cmd('volume create',ops)

        def rm(self,options=None):
            ops=_make_list_parameter_safe(options)
            ops.append(self.name)
            self.docker_obj.cmd('volume rm',ops)

    def volume(self,name):
        return self.Volume(self,name)


    class Network:
        """
        Named network commands
        """
        def __init__(self,docker_obj,name):
            self.docker_obj=docker_obj
            self.name=name

        def create(self,options=None):
            ops=_make_list_parameter_safe(options)
            ops.append(self.name)
            self.docker_obj.cmd('network create',ops)

        def rm(self,options=None):
            ops=_make_list_parameter_safe(options)
            ops.append(self.name)
            self.docker_obj.cmd('network rm',ops)

    def network(self,name):
        return self.Network(self,name)
