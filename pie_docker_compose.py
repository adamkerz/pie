"""
Python3.6+ only
"""
__VERSION__='0.0.3'


from pathlib import Path

from pie import *


def _path_or_list_to_list(s):
    if isinstance(s,str) or isinstance(s,Path):
        return [s]
    elif isinstance(s,(list,tuple)):
        return list(s)
    return []


def _make_list_parameter_safe(ls):
    return list(ls) if ls is not None else []


class DockerCompose:
    def __init__(self,docker_compose_filenames=None,project_name=None):
        self.docker_compose_filenames=_path_or_list_to_list(docker_compose_filenames)
        self.project_name=project_name


    def cmd(self,compose_cmd,compose_options=None,options=None):
        """
        Builds a command and runs it like this:
        docker-compose -f <self.docker_compose_filenames...> [-p <self.project_name>] <compose_options> <compose_cmd> <cmd_options>
        """
        compose_options=_make_list_parameter_safe(compose_options)
        options=_make_list_parameter_safe(options)
        c_ops=[f'-f {fn}' for fn in self.docker_compose_filenames]
        if self.project_name:
            c_ops.append(f'-p {self.project_name}')
        c_ops.extend(compose_options)
        compose_options_str=' '.join(c_ops)
        options_str=' '.join(options)
        c=f'docker-compose {compose_options_str} {compose_cmd} {options_str}'
        # --no-ansi
        print(c)
        return cmd(c)


    def build(self,service=None,compose_options=None,options=None):
        """
        Builds a command and runs it like this (see `cmd` for exact pre-`compose_options` content):
        docker-compose ... <compose_options> build <options> [<service(s)...>]
        """
        compose_options=_make_list_parameter_safe(compose_options)
        options=_make_list_parameter_safe(options)
        if isinstance(service,str):
            options.append(service)
        elif isinstance(service,(list,tuple)):
            options.extend(service)
        return self.cmd('build',compose_options=compose_options,options=options)


    class Service:
        """
        Named service commands. Single service only.
        """
        def __init__(self,compose_obj,name):
            self.compose_obj=compose_obj
            self.name=name

        def cmd(self,compose_cmd,compose_options=None,options=None,container_cmd=''):
            options=_make_list_parameter_safe(options)
            options.append(self.name)
            options.append(container_cmd)
            return self.compose_obj.cmd(compose_cmd,compose_options=compose_options,options=options)

        def build(self,compose_options=None,options=None):
            return self.compose_obj.build(self.name,compose_options=compose_options,options=options)

        def up(self,compose_options=None,options=None):
            options=_make_list_parameter_safe(options)
            options.append(self.name)
            return self.compose_obj.cmd('up',compose_options=compose_options,options=options)

        def start(self,compose_options=None):
            options=[self.name]
            return self.compose_obj.cmd('start',compose_options=compose_options,options=options)

        def stop(self,compose_options=None,options=None):
            options=_make_list_parameter_safe(options)
            options.append(self.name)
            return self.compose_obj.cmd('stop',compose_options=compose_options,options=options)

    def service(self,name):
        return self.Service(self,name)


    @classmethod
    def set_ignore_orphans_env_variable(cls,value):
        """If you use multiple docker compose files in the same project, docker compose thinks that some services have been orphaned, but really it's just that docker compose doesn't know about the other docker compose files"""
        env.set('COMPOSE_IGNORE_ORPHANS','True' if value else 'False')



