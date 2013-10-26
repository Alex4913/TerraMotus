# TerraMotus :: 15-112 Term Project

## Overview
_TerraMotus_ is a bridge between the tangible, malleable world and the infinite
realm of computer simulation. The aim is to give the user a unique experience,
in that they can terraform a simulated world in real-time using a physical,
malleable input device: a sandbox read by a Microsoft Kinect.

## Project Requirements
This project uses Python 2.7.3 with a few external dependencies:
* [libfreenect](https://github.com/OpenKinect/libfreenect)
* [PyOpenGL 3.x](http://pyopengl.sourceforge.net/)
* [PyODE 1.2.x](http://pyode.sourceforge.net/)
* [NumPy](http://www.numpy.org/)

## The Meat
This program melds a physics engine with real-time depth data collected by a
Kinect Sensor. This alone is near-trivial, as both libraries provide functions
to make the transition nearly seamless, albeit with a few changes to the format
of the data.

### Error Correction
An interesting feature of the program is error correction. The Kinect is a very
powerful tool, but it does come with errors. If an object has the ability to
reflect light, it has the possibility of skewing the IR beams that the Kinect
uses for depth perception. This, along with occasional errors in the sensor
itself pose an interesting problem to handle.

The error correction works by identifying areas of error within the depth data
and slowly averaging the edge-cases with non-erroneous neighbors. This process
is repeated until the errors are gone.

Surprisingly, this yields fairly accurate patches in the Kinect data, a behavior
I did not initially expect.

### The Pièce de Résistance :: Optimization

#### Initial Woes
The Kinect gives back a depth field of size 640 x 480. Some simple arithmetic
indicates that this translates to 307,200 individual depth data points. This is
not nearly on the scale of _Big Data_, but this still poses an issue when
showing a rendered sandbox on the screen.

Initially, I took the simple approach to draw triangles between adjacent points,
yielding a total of 612,162 triangles to draw for the entire surface, as between
a "box" of points, that is a grouping of four adjasent data-points, there were
two triangles drawn. Shown below:

![Initial Approach](https://github.com/Alex4913/TerraMotus/blob/master/media/images/tri-boxes.png?raw=true)

This gave incredible fidelity to the terrain, but clearly, this was not the way
to approach drawing the environment. This made the program unusable as there 
were over half a million triangles drawn every frame.

#### Combating (OpenG)Lethargy
What followed this was to apply a few filters to the depth data. The following
illustrate various optimization strategies. There is a pattern in these
approaches: I did not want to sacrifice fidelity in the terrain in order to draw
faster, but rather find more optimal ways to draw the data I have.

__Sampling__:

One method to make the data more manageable was to "sample" the data at a 
regular interval. While this would make drawing faster, this sacrifices
fidelity in the terrain.

__Nearest-Neighbor Interpolation__:

Another method was to average the depth data, almost like re-sizing a photo. 
This would make the depth feild smaller, but it would keep a more accurate 
representation of the reduced data. Again, this would lead to a loss in 
fidelity.

__Triangle Strips__:

Instead of drawing two trinagles per block, draw only one, by combining
neighboring triangles. This take advantage of OpenGL's Triangle Stip drawing
method, considered to be the fastest way to draw triangles.
It follows this example:

![Triangle Strips](https://github.com/Alex4913/TerraMotus/blob/master/media/images/tri-strip.png?raw=true)

However, this leaves gaps in the drawing, but it significantly reduces the
number of triangles drawn.

__Grouping Near-Parallel Planes__
Now comes the real improvement! This method involves approaching the problem
from an applied, Multi-Variable Calculus route. Instead of drawing individual
triangles, many of whom have neighboring triangles that are near-parallel,
rather, it is efficient to draw groups of near-parallel triangles as a single 
plane.

For this, we define near-parallel planes as having normal vectors within a
certain error of angle, a radix. As we increase that error, the more fidelity
in the terrain is lost.

This algorithm first finds triangles with similar normal vectors, ensuring that
they are adjacent, then it finds the best way to fill that area with triangles,
minimizing the number drawn. An example shown below:

![Efficiency!](https://github.com/Alex4913/TerraMotus/blob/master/media/images/tri-big.png?raw=true)

For a grid of size 100 x 100, here are the comparative triangle totals:

|          Method          | Triangles Generated |
|:------------------------:| -------------------:|
| Triangle Boxes           |              19,602 |
| Triangle Strips          |               5,200 |
| Sampling (step = 2)      |               4,902 |
| Interpolation (step = 2) |               4,902 |
| Near-Parallel Grouping   |                 > 1 |
