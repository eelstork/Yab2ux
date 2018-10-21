# Yab2ux

Although Unity 3D can handle Blend files internally, their import is and has always been very, very slow.

In spirit, a workaround to this problem is to first export an FBX from Blender, then import the FBX into Unity; but doing this 
manually is annoying and error prone.

This Blender add-on mirrors your blend files to FBX whenever you save.
With the help of a JSON file the add-on reflects a hierarchy of `*.blend` files (outside the Unity `Assets` dir) to a hiearchy of 
`*.fbx` files (inside the Unity `Assets` dir).

## Installation

- Open Blender
- Go to user preferences > Add-ons. 
- Choose 'Install add-on from file' (bottom of the Add-ons tab)
- Enable the addon (Yab2ux) from the Import-Export category.

## Configuration

When saving a blend file, Yab2ux looks for a file named `fbx_config.json` up the path to that file. 
Typically, this file would be like:

```
{
  "path": "Assets/",
  "axis_forward": "Y",
  "axis_up": "Z"
}
```

Except the `path` element, all available properties are defined by Blender's FBX exporter. Said `path` is relative to the 
location of the config file. So, assuming the following project structure, the above file would work wonders:

```
MyUnityProj
-- Assets
-- Blends
-- fbx_config.json
```

In that case all files under `Blends` (recursively) would be reflected as FBX, under `Assets/Blends`.
