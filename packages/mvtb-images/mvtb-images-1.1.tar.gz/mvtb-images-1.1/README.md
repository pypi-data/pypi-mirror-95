# Images for Machine Vision Toolbox

This package includes images associated with the Machine Vision Toolbox for Python (MVTB-P).

## Rationale

The images are provided as a separate package to work around disk space limitations on PyPI.  Including these images with the MVTB code adds 90MB to every release, which will blow the PyPI limit quite quickly.  Since the image set don't change very much, it makes sense for it to be a standalone package.

## Package contents

This package includes the following images

![image gallery](https://github.com/petercorke/machinevision-toolbox-python/raw/master/figs/gallery1.png)

## Installing the package

You don't need to explicitly install this package, it happens automatically when you when you install MVTB-P

```
pip install machinevisiontoolbox-python
```
since it is a dependency.

## Accessing these images from MVTB

When you load a file using MVTB-P

```python
import machinevisiontoolbox

myimage = Image("monalisa.png")
```
the file is looked for at the given path (relative to the current working directory if it's a relative path), and if not found it is looked for in this package. 

## Accessing these images from your own code

`pip` will install the package at some obscure place in your filesystem, but the path to any of the images can be easily found:

```python
from importlib import resources
try:
    with resources.path("mvtbimages", "monalisa.png") as f:
        # f is the path to the image
```

# Complete image library

A larger set (350MB) of images is all available in the package `mvtb-images-big` which includes several images sequences.  To install this

```
pip install machinevisiontoolbox-python[bigimage]
```

If you want to "upgrade" the images without reinstalling MVTB then do the following

```
pip uninstall mvtb-images
pip install mvtb-images-big
```

The package in each case is called `mvtbimages`.