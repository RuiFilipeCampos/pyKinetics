# pyKinetics

Create and simulate any biokinetic model.

This is a side project I'm doing for fun. 

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

![modelo_iodo](https://user-images.githubusercontent.com/63464503/128603978-1abc524b-ce1b-4c83-bc23-6ae0bf7d729f.png)


```python
from pyKinetics import *

blood   = Entity(250, name="Bloodstream")
thyroid = Entity(0, name="Thyroid")
rest    = Entity(0, name="Rest of Body")
bladder = Entity(0, name="Bladder")
large_intestine = Entity(0, name="Large Intestine")

blood.connect(thyroid, 0.035)
blood.connect(rest, 0.08)

thyroid.connect(bladder, 3.61E-4)
bladder.connect(large_intestine, 4.81E-4)
bladder.connect(blood, 1.93E-3)

excretory_system = Model(blood, thyroid, rest, bladder, large_intestine, name = "Radio-isotope model")


#model.introduce_decay(3.6E-3)
excretory_system.introduce_decay(3.6E-3)
excretory_system.introduce_exit(rest, 0.058)
excretory_system.introduce_exit(large_intestine, 0.029)

excretory_system.run(200)
excretory_system.plot()
```

![radioactivity_model](https://user-images.githubusercontent.com/63464503/128603962-49618e52-49cf-4f8e-9adf-f187074126b4.png)


## Example 3: Covid 19 Simulation 
![model_NK_covid](https://user-images.githubusercontent.com/63464503/128604273-25feab06-10f2-4b20-a26f-529b298d2e5b.png)
