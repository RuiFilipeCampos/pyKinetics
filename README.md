# pyKinetics

Create and simulate any biokinetic model.


## Example 1: A->B->C

Create a compartment using `Compartimento(initial_quantity, name = "untitled")`. Connect compartments using `A.connect(B, decay_rate)`.

```python
from pyKinetics import *

A = Compartimento(1, name="A")
B = Compartimento(0, name="B")
C = Compartimento(0, name="C")

A.connect(B, 1);
B.connect(C, 1)

model = Model(A, B, C)

model.run(10, 2000) # args-> total time to be simulated , number of points to be acquired
model.plot()
```

![alt text](https://i.imgur.com/OppaEWp.png)


## Example 2: Radiation 

```python

A = Compartimento(250, name="Blood")
B = Compartimento(0, name="Thyroid")
C = Compartimento(0, name="Rest of Body")
D = Compartimento(0, name="Bladder")
E = Compartimento(0, name="Large Intestine")

A.connect(B, 0.035)
A.connect(C, 0.08)

B.connect(D, 3.61E-4)
D.connect(E, 4.81E-4)
D.connect(A, 1.93E-3)

model = Model(A, B, C, D, E)

#model.introduce_decay(3.6E-3)
model.introduce_decay(3.6E-3)
model.introduce_exit(C, 0.058)
model.introduce_exit(E, 0.029)
```
