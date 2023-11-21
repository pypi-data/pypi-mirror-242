# SDCD: Stable Differentiable Causal Discovery

SDCD is a method for inferring causal graphs from labeled interventional data.\
You can read the associated preprint, ["Stable Differentiable Causal Discovery"](https://arxiv.org/abs/2311.10263), on arXiv.

![sdcd-cartoon](https://github.com/azizilab/sdcd/assets/14086852/f1d29a7a-7835-401c-a06e-aabcf8c77ec6)


If you find this work useful, please consider citing our work:

```bibtex
@article{nazaret2023stable,
  title={Stable Differentiable Causal Discovery}, 
  author={Achille Nazaret and Justin Hong and Elham Azizi and David Blei},
  journal={arXiv preprint arXiv:2311.10263},
  year={2023}
}
```

---
## Quick Start

For the main implementation of the method, see the [SDCD](sdcd/models/_sdcd.py) class.

For a tutorial on the basic usage of SDCD, see [this notebook](tutorials/SDCD_basic_usage.ipynb).

Code used to generate paper figures can be found in [this folder](paper_experiments/).

