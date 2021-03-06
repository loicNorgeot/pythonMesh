# Fluid outside an object

## 1 - Preparation in Blender

### HR mesh
![alt text](https://user-images.githubusercontent.com/11873158/28868549-15f6c2ba-777a-11e7-8473-676d720e807d.png)

### Checking LR mesh with 3D print toolbox
Using check all to compute the quality, and clicking on intersect faces and non manifold to get the intersections and holes
![alt text](https://user-images.githubusercontent.com/11873158/28868590-3b803cb4-777a-11e7-82bd-52b6e47a1cfa.png)

### Closing the model
With the "F" shortcut, after selecting loops with Shift + Alt + Right click for instance
![alt text](https://user-images.githubusercontent.com/11873158/28868654-6c84d568-777a-11e7-9585-9dac566a355d.png)

### Adding a computational domain
![](https://user-images.githubusercontent.com/11873158/28868916-3e62e2aa-777b-11e7-90d1-59abb773cdd5.png)

![](https://user-images.githubusercontent.com/11873158/28868913-3e600cce-777b-11e7-8af3-4d16e69b1dcd.png)

![](https://user-images.githubusercontent.com/11873158/28868914-3e601e3a-777b-11e7-9b24-413740aced98.png)

![](https://user-images.githubusercontent.com/11873158/28868917-3e64e474-777b-11e7-914c-619f34bb0de9.png)

### Exporting to .mesh
![](https://user-images.githubusercontent.com/11873158/28868915-3e622798-777b-11e7-95c5-4ac5f44fc888.png)

### Checking in medit
```bash
medit suzanne.mesh
```
* Z to zoom in
* Shift + Z to zoom out
* F1 to toogle clip
* e to display references
* b to change background
* l to toggle wireframe

![](https://user-images.githubusercontent.com/11873158/28868918-3e66b04c-777b-11e7-998c-aebbea30a944.png)

### Running tetgen
```bash
tetgen -pgaA suzanne.mesh
```
Writes to suzanne.1.mesh

You can get the reference of a tetrahedra with Shift + click, and looking in the terminal (blue = 0, red = 1, green = 2)

![](https://user-images.githubusercontent.com/11873158/28868919-3e74e086-777b-11e7-9af6-a322cefa9bf2.png)

### Removing the green domain (reference 2)
```bash
python pythonMesh/src/removeReference.py suzanne.1.mesh 2
```
![](https://user-images.githubusercontent.com/11873158/28868920-3e75b57e-777b-11e7-847e-91c7231b6792.png)

### Remeshing with mmg3d
```bash
mmg3d suzanne.1.d.mesh
```
Writes in + "suzanne.1.d.o.mesh"

![](https://user-images.githubusercontent.com/11873158/28868921-3e7a200a-777b-11e7-92f1-d8acd68a559e.png)

### Parameter file
Save as DEFAULT.nstokes in the same directory that your remeshed object
```bash
Dirichlet # Type of boundary condition
3 # 3 different regions for boundary conditions
1 triangle v 0. 0. 0. # The region of reference has a null velocity
2 triangle v 0. 1. 0. # The region of reference 2 is the input : v = (0,-1,0)
4 triangle v 0. 0. 0. # 4 also has a null velocity

Domain
1 #The number of domains in which we are computing the flow
1 1. 1. # reference one (red tetrahedras), nu and rho
```

### Running the simulation
```bash
nstokes -r 0.005 suzanne.1.d.o.mesh
```

### Looking at results
The original file has been modified, and should now contain the vector and scalar fields.
```bash
medit suzanne.1.d.o.mesh
```

### Converting to paraview
We have to write a file compatible with paraview in order
```bash
python pythonMesh/src/convertToParaview.py suzanne.1.d.o.mesh
```
A file called suzanne.1.d.o.vtk has been created (hopefully)

### Visualizations in Paraview
A whole new tool...

Import the vtk file in paraview, and apply your filters.

When you are satisfied, go to File -> Export Scene and choose .x3d format. You will be able to open that file in blender.

![](https://user-images.githubusercontent.com/11873158/28874459-33f19a3e-7792-11e7-9916-25f10aa110ce.png)

### Importing back in blender
You can now import back the x3d file in blender, to visualize the results.

File -> import -> .x3d

However, you will see that the axis are not aligned. To fix this, you must rotate your results in blender:
* R + x + 90
* R + z + 180
Be sure to rotate around the origin of the scene!
![](https://user-images.githubusercontent.com/11873158/28874328-b44e9994-7791-11e7-8e64-7f68d7cdd36b.png)
