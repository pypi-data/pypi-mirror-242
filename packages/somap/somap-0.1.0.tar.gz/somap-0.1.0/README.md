# Somap

***Somap*** is a flexible, fast and scalable Self-Organizing Maps library in python. It allows you to define and run different flavors of SOMs (Kohonen, DSOM or your custom ones) on square or hexagonal 2D grid, with or without toroidal topology.

<p align="center">
    <img src="docs/som_on_mnist_hex.png">
    &nbsp;&nbsp;&nbsp;&nbsp;
    <img src="docs/som_on_mnist_square.png">
</p>

# Why a new SOM library?

There are already a few open-source libraries for Self-Organizing Maps in python, of which [MiniSom](https://github.com/JustGlowing/minisom) and [SOMPY](https://github.com/sevamoo/SOMPY) seem to be the most popular. I developped ***Somap*** to overcome what I believe to be two shortcomings of existing libraries for my research on bio-inspired AI: 
- Ability to easily customize the SOM algorithm (e.g. distance, neighborhood, learning rate and update functions).
- Capacity to vectorize the computations over many SOMs (e.g. for distributed learning over 2D maps of SOMs).

Thanks to [JAX](https://github.com/google/jax)'s `jit` and `vmap` magic functions, it turned out that performance was also significantly better compared to other frameworks. More precisely, it relies indirectly on JAX via the [Equinox](https://github.com/patrick-kidger/equinox) library that offers an easy-to-use PyTorch-like syntax.

# Installation

Requires Python 3.10+ and a working installation of JAX 0.4.20+. You can follow [these instructions](https://github.com/google/jax#installation) to install JAX with the relevant hardware acceleration support.

Then:

```bash
pip install somap
```

# Quick example

The classic workflow goes as follow:
```python
import somap as smp

# Load the MNIST dataset as a Numpy array of shape (60000, 28, 28)
data = smp.datasets.MNIST().data

# Initialize the 2D map
model = smp.StaticKsom(
    shape = (11, 13), 
    topography = "hex", 
    borderless = False, 
    input_shape = (28, 28), 
    params = smp.StaticKsomParams(sigma=0.3, alpha=0.5)
)

# Train (see documentation to understand the "bu_v" dict key)
model, aux = smp.make_steps(model, {"bu_v": data})

# Plot the 2D map 
smp.plot(model)

# Retrieve the errors from all steps
quantization_errors = aux["metrics"]["quantization_error"]
topographic_errors = aux["metrics"]["topographic_error"]
```

# Documentation

* [Documentation website](https://mthiboust.github.io/somap/)
* [Examples from notebooks](notebooks/)

# Citation

If you found this library to be useful in academic work, then please cite:
```
@misc{thiboust2023somap,
  title={Somap: a flexible, fast and scalable python library for Self-Organizing Maps.},
  author={Matthieu Thiboust},
  year={2023},
  url={https://github.com/mthiboust/somap/},
}
```


