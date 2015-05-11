# Preparing the script

In section *define body sections* add or remove rocket sections using commands like

```
rocket.addSection(<sectionName>(<sectionParameters>))
```

In section *define and build fins* define fin sections and build their profile,
then define, build and append their group (Fins)

Once you specified the rocket parts, you can set the dimensions and offset
of the outer space (cylinder)

In the *meshing* section, you can set various mesh parameters for the 2D, 3D
and boundary layer meshes.

Finally, you can export the mesh to a file

# Running the script
When done, you can launch the script by cd-ing in the script directory and
issuing the command

```
~$ salome -t mesher.py
```

where "salome" is the command to execute salome.

It is **essential** that salome be run
from the directory of mesher.py, otherwise salome's interpreter won't find the
other source files.

The command to launch salome could be similar to
```
~$ /path/to/salome/appli_V7_5_1/runAppli
```

If you do not specify the `-t` option, salome will be run with the GUI.
In this case, in salome's interpreter, in the lower part of the window, an "execfile" command
appears. Any error in the execution of mesher.py is displayed in that
interpreter.

# Visualization in the GUI
If execution terminated normally, Expand item "Mesh" in the object browser
[left column] and press F5 to update the tree.
One or more mesh objects will appear and you can make it visible by toggling the eye icon.

You can observe the result in the viewer.
Right-click the surface and choose clipping for a better 3D
rendering.
Click the mouse-like icon in the viewer toolbar to enable 3D rotation of the
generated image.
