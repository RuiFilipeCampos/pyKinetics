# pyKinetics

Create and simulate any biokinetic model.

```
pip install pyKinetics
```

Note: these examples work on the code in this repo, the distribution in pypi is not up to date yet.

## Example 1: A->B->C

```python
from pyKinetics import *

A = Entity(1, name="A")
B = Entity(0, name="B")
C = Entity(0, name="C")

A.connect(B, 1)
B.connect(C, 1)

model = Model(A, B, C, name = "ABC model")

model.run(time = 10, Np = 1000)
model.plot()
```

<img align="middle" alt="ABCmodel" src = "https://user-images.githubusercontent.com/63464503/128603547-cea700e3-00f6-4c6f-9b8b-5c22629b7ca6.png" width = "688"> 

## Example 2: Radiation 

```python
from pyKinetics import *

A = Entity(250, name="Blood")
B = Entity(0, name="Thyroid")
C = Entity(0, name="Rest of Body")
D = Entity(0, name="Bladder")
E = Entity(0, name="Large Intestine")

A.connect(B, 0.035)
A.connect(C, 0.08)

B.connect(D, 3.61E-4)
D.connect(E, 4.81E-4)
D.connect(A, 1.93E-3)

model = Model(A, B, C, D, E, name = "Radio-isotope model")


#model.introduce_decay(3.6E-3)
model.introduce_decay(3.6E-3)
model.introduce_exit(C, 0.058)
model.introduce_exit(E, 0.029)

model.run(200)
model.plot()
```


## Example 3: Covid 19 Simulation 
