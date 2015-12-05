import os

import jinja2

protocols = ['1.6']


def create_gw(args, settings):
    filename = "gw_{}_{}.ino".format(args.type, protocols[-1].replace('.', ''))
    skel_dir = _get_skeleton_dir()
    with open(os.path.join(skel_dir, filename)) as f:
        file_in = f.read()

    template = jinja2.Template(file_in)
    file_out = template.render(vars(args))
    with open(args.output, 'w') as f:
        f.write(file_out)


def create_node(args, settings):
    filename = "node_{}.ino".format(protocols[-1].replace('.', ''))
    skel_dir = _get_skeleton_dir()
    with open(os.path.join(skel_dir, filename)) as f:
        file_in = f.read()

    temp = jinja2.Template(file_in)
    file_out = temp.render(vars(args))

    with open(args.output, 'w') as f:
        f.write(file_out)


def _get_skeleton_dir():
    package_dir, filename = os.path.split(__file__)
    skel_dir = os.path.join(package_dir, 'skeletons')

    return skel_dir
