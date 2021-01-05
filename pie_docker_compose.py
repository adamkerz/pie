"""
Python3.6+ only
"""
__VERSION__='0.0.1'


from pie import *


class DockerCompose:
    def __init__(self, docker_compose_filename, project_name=None):
        self.docker_compose_filename = docker_compose_filename
        self.project_name = project_name

    def cmd(self, compose_cmd, compose_options=[], options=[]):
        cops = [f'-f {self.docker_compose_filename}']
        if self.project_name:
            cops.append(f'-p {self.project_name}')
        cops.extend(compose_options)
        compose_options_str = ' '.join(cops)
        options_str = ' '.join(options)
        c = f'docker-compose {compose_options_str} {compose_cmd} {options_str}'
        # --no-ansi
        print(c)
        cmd(c)

    def service(self, service_name):
        return DockerComposeService(self, service_name)

    @classmethod
    def set_ignore_orphans_env_variable(cls, value):
        """If you use multiple docker compose files in the same project, docker compose thinks that some services have been orphaned, but really it's just that docker compose doesn't know about the other docker compose files"""
        env.set('COMPOSE_IGNORE_ORPHANS', 'True' if value else 'False')


class DockerComposeService:
    def __init__(self, compose_obj, service_name):
        self.compose_obj = compose_obj
        self.service_name = service_name

    def cmd(self, compose_cmd, compose_options=[], options=[], container_cmd=''):
        options_ext = list(options)
        options_ext.extend([self.service_name, container_cmd])
        self.compose_obj.cmd(compose_cmd, compose_options, options_ext)
