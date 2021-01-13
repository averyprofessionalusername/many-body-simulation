# many-body-simulation
My first experience with object-oriented programming.

A simulation of many different planets interacting by a simple attractive force. Force is proportional to mass of the attractor multiplied by the mass of the attracted divided by the distance squared, in the direction of the attractor. The three-body problem is the problem of solving the equation of motion of three bodies interacting by gravitation. The problem is famously unsolvable analytically and requires numerical simulation. I have extended the three body problem to simulate as many planets as your computer can handle, planets are spawned into the frame with random masses, positions and velocities. When planets collide, they merge into one planet, maintaining momentum, combining mass, and combining colours to make a new colour.


Requires Python with pygame package to run. 

## PyGame Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pygame.

```bash
pip install pygame
```
## Usage

Set the number of planets you want to simulate by changing the variable 'numplanets' to an integer of the number of planets you want. 

If you want the planets to leave a trail behind to paint a pretty picture you can do so by setting 'Tracer' variable to True.

If you want to change the number of stars on the background you can do so by setting variable 'numstars' to an integer of the number of stars you want.
