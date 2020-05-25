"""
Python3.6+ only
"""
from pie import *



class Docker:
    def __init__(self,options=[]):
        self.options=options

    def build(self,context,options=[]):
        self.cmd('build',options+[context])

    def run(self,image,cmd_and_args=None,options=[]):
        ops=list(options)
        ops.append(image)
        if cmd_and_args:
            ops.append(cmd_and_args)
        self.cmd('run',ops)

    def cmd(self,docker_cmd,cmd_options=[]):
        docker_options_str=' '.join(self.options)
        cmd_options_str=' '.join(cmd_options)
        c=f'docker {docker_options_str} {docker_cmd} {cmd_options_str}'
        print(c)
        cmd(c)
