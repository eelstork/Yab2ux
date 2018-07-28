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
"""

import json
import os

import bpy
import bpy.ops
from bpy.app.handlers import persistent

CONFIG_FILENAME = "/fbx_config.json"
KEY_PATH = 'path'
FBX = 'fbx'
CURRENT_FILE = '//'

bl_info = {"name": "Yab2ux", "category": "Import-Export"}


def register():
    """Required by addon manager"""
    bpy.app.handlers.save_post.append(save_fbx)


def unregister():
    """Required by addon manager"""
    if save_fbx in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.remove(save_fbx)


@persistent
def save_fbx(dummy):
    path = get_path()
    print('Save to ' + path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.export_scene.fbx(filepath=path)


def get_path():
    config, root = load_config()
    subpath = config[KEY_PATH]
    abs = bpy.path.abspath(CURRENT_FILE)
    branch = abs[len(root):]
    print('Branch: '+branch)
    if len(branch) > 0:
        branch += '/'
    name = bpy.path.basename(bpy.context.blend_data.filepath)[:-5] + FBX
    outpath = root + subpath + '/' + branch + name
    return outpath


def load_config():
    path = bpy.path.abspath(CURRENT_FILE)
    config = None
    while config is None:
        try:
            print("Check path:" + path)
            with open(path + CONFIG_FILENAME) as file:
                data = json.load(file)
                config = data
        except FileNotFoundError:
            print("Not here")
            new_path = os.path.dirname(path)
            if new_path == path:
                break;
            path = new_path
    if config is None:
        print("Nothing found")
    return config, path
