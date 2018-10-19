"""
Extension module for PIE that provides unix specific shortcuts.
"""
__VERSION__='0.0.1'

import pie


def cmd(c,use_sudo=False):
    sudo(c) if use_sudo else pie.cmd(c)

def sudo(c):
    pie.cmd(f'sudo {c}')


def set_permissions(p,mode=None,owner=None,group=None,use_sudo=False):
    if mode: cmd(f'chmod {mode:04o} {p}',use_sudo)
    if owner: cmd(f'chown {owner} {p}',use_sudo)
    if group: cmd(f'chgrp {group} {p}',use_sudo)


def mkdir(p,mode=None,owner=None,group=None,use_sudo=False):
    cmd(f'mkdir {p}',use_sudo)
    set_permissions(p,mode,owner,group,use_sudo)

def put_file(src,dest,mode=None,owner=None,group=None,use_sudo=False):
    cmd(f'cp {src} {dest}',use_sudo)
    set_permissions(dest,mode,owner,group,use_sudo)

