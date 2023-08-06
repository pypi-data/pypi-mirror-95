.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_api_plot_sampling_strategy_usage.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_api_plot_sampling_strategy_usage.py:


====================================================
How to use ``sampling_strategy`` in imbalanced-learn
====================================================

This example shows the different usage of the parameter ``sampling_strategy``
for the different family of samplers (i.e. over-sampling, under-sampling. or
cleaning methods).


.. code-block:: default


    # Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
    # License: MIT

    from collections import Counter

    import numpy as np
    import matplotlib.pyplot as plt

    from sklearn.datasets import load_iris

    from imblearn.datasets import make_imbalance

    from imblearn.over_sampling import RandomOverSampler
    from imblearn.under_sampling import RandomUnderSampler
    from imblearn.under_sampling import TomekLinks

    print(__doc__)


    def plot_pie(y):
        target_stats = Counter(y)
        labels = list(target_stats.keys())
        sizes = list(target_stats.values())
        explode = tuple([0.1] * len(target_stats))

        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return f"{pct:.2f}%  ({val:d})"

            return my_autopct

        fig, ax = plt.subplots()
        ax.pie(
            sizes,
            explode=explode,
            labels=labels,
            shadow=True,
            autopct=make_autopct(sizes),
        )
        ax.axis("equal")









First, we will create an imbalanced data set from a the iris data set.


.. code-block:: default


    iris = load_iris()

    print(f"Information of the original iris data set: \n {Counter(iris.target)}")
    plot_pie(iris.target)

    sampling_strategy = {0: 10, 1: 20, 2: 47}
    X, y = make_imbalance(iris.data, iris.target, sampling_strategy=sampling_strategy)

    print(
        f"Information of the iris data set after making it"
        f" imbalanced using a dict: \n sampling_strategy={sampling_strategy} \n "
        f"y: {Counter(y)}"
    )
    plot_pie(y)




.. rst-class:: sphx-glr-horizontal


    *

      .. image:: /auto_examples/api/images/sphx_glr_plot_sampling_strategy_usage_001.png
          :alt: plot sampling strategy usage
          :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/api/images/sphx_glr_plot_sampling_strategy_usage_002.png
          :alt: plot sampling strategy usage
          :class: sphx-glr-multi-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Information of the original iris data set: 
     Counter({0: 50, 1: 50, 2: 50})
    Information of the iris data set after making it imbalanced using a dict: 
     sampling_strategy={0: 10, 1: 20, 2: 47} 
     y: Counter({2: 47, 1: 20, 0: 10})




Using ``sampling_strategy`` in resampling algorithms
##############################################################################

``sampling_strategy`` as a ``float``
....................................

``sampling_strategy`` can be given a ``float``. For **under-sampling
methods**, it corresponds to the ratio :math:`\\alpha_{us}` defined by
:math:`N_{rM} = \\alpha_{us} \\times N_{m}` where :math:`N_{rM}` and
:math:`N_{m}` are the number of samples in the majority class after
resampling and the number of samples in the minority class, respectively.


.. code-block:: default


    # select only 2 classes since the ratio make sense in this case
    binary_mask = np.bitwise_or(y == 0, y == 2)
    binary_y = y[binary_mask]
    binary_X = X[binary_mask]

    sampling_strategy = 0.8

    rus = RandomUnderSampler(sampling_strategy=sampling_strategy)
    X_res, y_res = rus.fit_resample(binary_X, binary_y)
    print(
        f"Information of the iris data set after making it "
        f"balanced using a float and an under-sampling method: \n "
        f"sampling_strategy={sampling_strategy} \n y: {Counter(y_res)}"
    )
    plot_pie(y_res)




.. image:: /auto_examples/api/images/sphx_glr_plot_sampling_strategy_usage_003.png
    :alt: plot sampling strategy usage
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Information of the iris data set after making it balanced using a float and an under-sampling method: 
     sampling_strategy=0.8 
     y: Counter({2: 12, 0: 10})




For **over-sampling methods**, it correspond to the ratio
:math:`\\alpha_{os}` defined by :math:`N_{rm} = \\alpha_{os} \\times N_{M}`
where :math:`N_{rm}` and :math:`N_{M}` are the number of samples in the
minority class after resampling and the number of samples in the majority
class, respectively.


.. code-block:: default


    ros = RandomOverSampler(sampling_strategy=sampling_strategy)
    X_res, y_res = ros.fit_resample(binary_X, binary_y)
    print(
        f"Information of the iris data set after making it "
        f"balanced using a float and an over-sampling method: \n "
        f"sampling_strategy={sampling_strategy} \n y: {Counter(y_res)}"
    )
    plot_pie(y_res)




.. image:: /auto_examples/api/images/sphx_glr_plot_sampling_strategy_usage_004.png
    :alt: plot sampling strategy usage
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Information of the iris data set after making it balanced using a float and an over-sampling method: 
     sampling_strategy=0.8 
     y: Counter({2: 47, 0: 37})




``sampling_strategy`` has a ``str``
...................................

``sampling_strategy`` can be given as a string which specify the class
targeted by the resampling. With under- and over-sampling, the number of
samples will be equalized.

Note that we are using multiple classes from now on.


.. code-block:: default


    sampling_strategy = "not minority"

    rus = RandomUnderSampler(sampling_strategy=sampling_strategy)
    X_res, y_res = rus.fit_resample(X, y)
    print(
        f"Information of the iris data set after making it "
        f"balanced by under-sampling: \n sampling_strategy={sampling_strategy} \n"
        f" y: {Counter(y_res)}"
    )
    plot_pie(y_res)

    sampling_strategy = "not majority"

    ros = RandomOverSampler(sampling_strategy=sampling_strategy)
    X_res, y_res = ros.fit_resample(X, y)
    print(
        f"Information of the iris data set after making it "
        f"balanced by over-sampling: \n sampling_strategy={sampling_strategy} \n "
        f"y: {Counter(y_res)}"
    )
    plot_pie(y_res)




.. rst-class:: sphx-glr-horizontal


    *

      .. image:: /auto_examples/api/images/sphx_glr_plot_sampling_strategy_usage_005.png
          :alt: plot sampling strategy usage
          :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/api/images/sphx_glr_plot_sampling_strategy_usage_006.png
          :alt: plot sampling strategy usage
          :class: sphx-glr-multi-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Information of the iris data set after making it balanced by under-sampling: 
     sampling_strategy=not minority 
     y: Counter({0: 10, 1: 10, 2: 10})
    Information of the iris data set after making it balanced by over-sampling: 
     sampling_strategy=not majority 
     y: Counter({0: 47, 1: 47, 2: 47})




With **cleaning method**, the number of samples in each class will not be
equalized even if targeted.


.. code-block:: default


    sampling_strategy = "not minority"
    tl = TomekLinks(sampling_strategy)
    X_res, y_res = tl.fit_resample(X, y)
    print(
        f"Information of the iris data set after making it "
        f"balanced by cleaning sampling: \n sampling_strategy={sampling_strategy} \n "
        f"y: {Counter(y_res)}"
    )
    plot_pie(y_res)




.. image:: /auto_examples/api/images/sphx_glr_plot_sampling_strategy_usage_007.png
    :alt: plot sampling strategy usage
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/glemaitre/Documents/packages/imbalanced-learn/imblearn/utils/_validation.py:587: FutureWarning: Pass sampling_strategy=not minority as keyword args. From version 0.9 passing these as positional arguments will result in an error
      warnings.warn(
    Information of the iris data set after making it balanced by cleaning sampling: 
     sampling_strategy=not minority 
     y: Counter({2: 46, 1: 19, 0: 10})




``sampling_strategy`` as a ``dict``
...................................

When ``sampling_strategy`` is a ``dict``, the keys correspond to the targeted
classes. The values correspond to the desired number of samples for each
targeted class. This is working for both **under- and over-sampling**
algorithms but not for the **cleaning algorithms**. Use a ``list`` instead.


.. code-block:: default



    sampling_strategy = {0: 10, 1: 15, 2: 20}

    rus = RandomUnderSampler(sampling_strategy=sampling_strategy)
    X_res, y_res = rus.fit_resample(X, y)
    print(
        f"Information of the iris data set after making it "
        f"balanced by under-sampling: \n sampling_strategy={sampling_strategy} \n "
        f"y: {Counter(y_res)}"
    )
    plot_pie(y_res)

    sampling_strategy = {0: 25, 1: 35, 2: 47}

    ros = RandomOverSampler(sampling_strategy=sampling_strategy)
    X_res, y_res = ros.fit_resample(X, y)
    print(
        f"Information of the iris data set after making it "
        f"balanced by over-sampling: \n sampling_strategy={sampling_strategy} \n "
        f"y: {Counter(y_res)}"
    )
    plot_pie(y_res)




.. rst-class:: sphx-glr-horizontal


    *

      .. image:: /auto_examples/api/images/sphx_glr_plot_sampling_strategy_usage_008.png
          :alt: plot sampling strategy usage
          :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/api/images/sphx_glr_plot_sampling_strategy_usage_009.png
          :alt: plot sampling strategy usage
          :class: sphx-glr-multi-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Information of the iris data set after making it balanced by under-sampling: 
     sampling_strategy={0: 10, 1: 15, 2: 20} 
     y: Counter({2: 20, 1: 15, 0: 10})
    Information of the iris data set after making it balanced by over-sampling: 
     sampling_strategy={0: 25, 1: 35, 2: 47} 
     y: Counter({2: 47, 1: 35, 0: 25})




``sampling_strategy`` as a ``list``
...................................

When ``sampling_strategy`` is a ``list``, the list contains the targeted
classes. It is used only for **cleaning methods** and raise an error
otherwise.


.. code-block:: default


    sampling_strategy = [0, 1, 2]
    tl = TomekLinks(sampling_strategy=sampling_strategy)
    X_res, y_res = tl.fit_resample(X, y)
    print(
        f"Information of the iris data set after making it "
        f"balanced by cleaning sampling: \n sampling_strategy={sampling_strategy} "
        f"\n y: {Counter(y_res)}"
    )
    plot_pie(y_res)




.. image:: /auto_examples/api/images/sphx_glr_plot_sampling_strategy_usage_010.png
    :alt: plot sampling strategy usage
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Information of the iris data set after making it balanced by cleaning sampling: 
     sampling_strategy=[0, 1, 2] 
     y: Counter({2: 46, 1: 19, 0: 10})




``sampling_strategy`` as a callable
...................................

When callable, function taking ``y`` and returns a ``dict``. The keys
correspond to the targeted classes. The values correspond to the desired
number of samples for each class.


.. code-block:: default



    def ratio_multiplier(y):
        multiplier = {1: 0.7, 2: 0.95}
        target_stats = Counter(y)
        for key, value in target_stats.items():
            if key in multiplier:
                target_stats[key] = int(value * multiplier[key])
        return target_stats


    X_res, y_res = RandomUnderSampler(sampling_strategy=ratio_multiplier).fit_resample(X, y)

    print(
        f"Information of the iris data set after balancing using a callable"
        f" mode:\n ratio={ratio_multiplier} \n y: {Counter(y_res)}"
    )
    plot_pie(y_res)

    plt.show()



.. image:: /auto_examples/api/images/sphx_glr_plot_sampling_strategy_usage_011.png
    :alt: plot sampling strategy usage
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Information of the iris data set after balancing using a callable mode:
     ratio=<function ratio_multiplier at 0x7fb4e6404550> 
     y: Counter({2: 44, 1: 14, 0: 10})
    /home/glemaitre/Documents/packages/imbalanced-learn/examples/api/plot_sampling_strategy_usage.py:242: UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.
      plt.show()





.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  5.575 seconds)

**Estimated memory usage:**  24 MB


.. _sphx_glr_download_auto_examples_api_plot_sampling_strategy_usage.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_sampling_strategy_usage.py <plot_sampling_strategy_usage.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_sampling_strategy_usage.ipynb <plot_sampling_strategy_usage.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
