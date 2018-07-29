"""
This add-on exports an fbx copy whenever a blend file is saved.
Starting from the containing folder, the add-on will look for a json file named
'fbx_config.json' up the hierarchy. If no such file is found, no fbx file is
generated.
If the config file is found, the 'path' key points at a directory (relative to
that which contains the config file) where fbx files are saved.
The general idea is that you have an fbx file hierarchy in your Assets folder,
that mirrors the blend file hierarchy that you organise your files with.
TODO: when there is no config file, don't export
TODO: when multiple configs are present, nodes down the hiearchy override
ancestors
TODO: pass parameters to fbx exporter
"""

import json
import os
from os import makedirs
from os.path import abspath, basename, dirname, join, relpath

CONFIG_FILENAME = "fbx_config.json"
KEY_PATH = 'path'
FBX = 'fbx'
CURRENT_FILE = '//'

bl_info = {"name": "Yab2ux", "category": "Import-Export"}

# Functions that require Blender ----------------------------------------------

def register():
    """Required by addon manager"""
    import bpy
    bpy.app.handlers.save_post.append(export_fbx)


def unregister():
    """Required by addon manager"""
    import bpy
    if export_fbx in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.remove(export_fbx)

try:
    from bpy.app.handlers import persistent
    @persistent
    def export_fbx(arg):
        import bpy
        inpath = bpy.path.abspath(CURRENT_FILE)
        config, root = load_config(inpath)
        if config is None:
            print("No fbx export config present; skip")
            return
        outpath = get_export_path(bpy.context.blend_data.filepath, config,
                                  root)
        do_export_fbx(outpath, config, root)
except ModuleNotFoundError:
    pass


def bl_to_fbx(path, **kwargs):
    import bpy.ops
    bpy.ops.export_scene.fbx(filepath=path, **kwargs)

# Other functions ------------------------------------------------------------


def do_export_fbx(path, config, root):
    makedirs(dirname(path), exist_ok=True)
    params = config.copy()
    params.pop('path')
    bl_to_fbx(path, **params)


def get_export_path(absolute_path, config, root):
    subpath = config[KEY_PATH]
    branch = relpath(dirname(absolute_path), root)
    name = basename(absolute_path)[:-5] + FBX
    outpath = join(root, subpath, branch, name)
    return outpath


def load_config(path_to_blend_file):
    path = path_to_blend_file
    root = None
    config = None
    while dirname(path) != path:
        node = load_config_file(path)
        if node is not None:
            if config:
                node.update(config)
                print("Use config @ " + path)
            config=node
            root = path
        path = dirname(path)
    return config, root


def load_config_file(dir):
    try:
        path = join(dir, CONFIG_FILENAME)
        with open(path) as file:
            return json.load(file)
    except FileNotFoundError:
        return None


# EOF ---------------------------------
