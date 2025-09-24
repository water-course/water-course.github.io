# 🧪 Tutorials

This section contains a growing collection of **Python tutorials** that support this course. All notebooks are available via our GitHub repository:

👉 [github.com/water-course/colab-tutorials](https://github.com/water-course/colab-tutorials)

They are fully executable and designed to be loaded into [Google Colab](https://colab.research.google.com/), an online Python notebook environment provided by Google.

In addition, **executed versions of these tutorials (with all answers)** are rendered directly on this site using the `jupytext` plugin. These are meant to help you follow the logic and confirm your own solutions.

!!! note "Try it yourself first!"
    All answers are available — but that is not the spirit of things. You are encouraged to first try solving the problems in Colab or on your local machine before reading the provided solutions. Programming and data analysis are learned by doing.

## ⚙️ What is Google Colab?

[Colab](https://colab.research.google.com/) is a free Jupyter notebook environment that runs in the cloud. It allows you to:

- Run Python code without installing anything locally
- Use a notebook interface similar to JupyterLab
- Access notebooks directly from GitHub
- Use free cloud-based GPUs (optional)

!!! tip
    Sometimes Colab may not have all required libraries pre-installed. For example, `cartopy` is **not** available by default.

    To install it inside a code cell:

    ```python
    !pip install cartopy
    ```

Replace `cartopy` with the name of the missing library as needed.

## ▶️ How to load tutorials from Colab

Below is a short demo showing how to load the full Jupyter notebook directory into Google Colab:

<div style="position:relative; width:100%; height:0px; padding-bottom:53.594%"><iframe allow="fullscreen" allowfullscreen height="100%" src="https://streamable.com/e/o0n81t?loop=0&muted=1" width="100%" style="border:none; width:100%; height:100%; position:absolute; left:0px; top:0px; overflow:hidden;"></iframe></div>

1. Visit [colab.research.google.com](https://colab.research.google.com/)
2. Go to the **GitHub** tab
3. Paste `water-course/colab-tutorials`
4. Select the notebook you want to work on

---

## 📘 Tutorial List

### [Tutorial 1](computer-lab/basics_00_solution.ipynb)
A beginner-friendly introduction to Python programming for geoscience applications, covering basic maths, loops, formatted output, and simple map plotting with Cartopy.
### [Tutorial 2](computer-lab/basics_01_solution.ipynb)
Learn how to perform geospatial analysis in Python by working with shapefiles, spatial queries, NetCDF rainfall data, and basin-scale integration over the Murray-Darling Basin.
### [Tutorial 3](computer-lab/Ex1_Precipitation_solution.ipynb)
Apply multiple interpolation methods to estimate missing rainfall values, using real storm data and geospatial coordinates — adapted from a tutorial by [Jesús Casado Rodríguez](https://github.com/casadoj).
### [Tutorial 4](computer-lab/basics_02_solution.ipynb)
Learn a practical approach for adjusting surface-area differences across latitude–longitude grids.

---

📂 **Access all notebooks:** [github.com/water-course/colab-tutorials](https://github.com/water-course/colab-tutorials)
