# pyKinetics

Create and simulate any biokinetic model.


## Example 1:

Create a compartment using `Compartimento(initial_quantity, name = "untitled")`. Connect compartments using `A.connect(B, decay_rate)` 

```python
from pyKinetics import *

A = Compartimento(1, name="A")
B = Compartimento(0, name="B")
C = Compartimento(0, name="C")

A.connect(B, 1);
B.connect(C, 1)

model = Model(A, B, C)

model.run(10, 2000) #t_total, # de pontos
model.plot()
```

![alt text](http://url/to/img.png)
