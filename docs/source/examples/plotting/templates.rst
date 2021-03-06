.. rst-class:: sphx-glr-example-title

.. _sphx_glr_examples_plotting_templates.py:


Plot Templates
============================

:mod:`pyrolite` includes some ready-made templates for well-known plots. These can
be used to create new plots, or add a template to an existing
:class:`matplotlib.axes.Axes`.


.. code-block:: default

    import matplotlib.pyplot as plt
    from pyrolite.util.plot.axes import share_axes









First let's build a simple total-alkali vs silica (
:func:`~pyrolite.plot.templates.TAS`) diagram:



.. code-block:: default

    from pyrolite.plot.templates import TAS

    ax = TAS(linewidth=0.5, labels='ID')
    plt.show()



.. image:: /examples/plotting/images/sphx_glr_templates_001.png
    :class: sphx-glr-single-img





The other templates currently included in :mod:`pyrolite` are the
:func:`~pyrolite.plot.templates.pearceThNbYb` and
:func:`~pyrolite.plot.templates.pearceTiNbYb` diagrams.
We can create some axes and add these templates to them:



.. code-block:: default

    from pyrolite.plot.templates import pearceThNbYb, pearceTiNbYb

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    share_axes(ax, which="x")  # these diagrams have the same x axis

    pearceThNbYb(ax=ax[0])
    pearceTiNbYb(ax=ax[1])

    plt.tight_layout()  # nicer spacing for axis labels




.. image:: /examples/plotting/images/sphx_glr_templates_002.png
    :class: sphx-glr-single-img





References and other notes for diagram templates can be found within the docstrings
and within the pyrolite documentation:



.. code-block:: default

    help(TAS)




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Help on function TAS in module pyrolite.plot.templates.TAS:

    TAS(ax=None, relim=True, color='k', **kwargs)
        Adds the TAS diagram from Le Bas (1992) [#pyrolite.plot.templates.TAS.TAS_1]_ to an axes.
    
        Parameters
        ----------
        ax : :class:`matplotlib.axes.Axes`
            Axes to add the template on to.
        relim : :class:`bool`
            Whether to relimit axes to fit the built in ranges for this diagram.
        color : :class:`str`
            Line color for the diagram.
    
        Returns
        -------
        ax : :class:`matplotlib.axes.Axes`
    
        References
        -----------
        .. [#pyrolite.plot.templates.TAS.TAS_1] Le Bas, M.J., Le Maitre, R.W., Woolley, A.R., 1992.
                    The construction of the Total Alkali-Silica chemical
                    classification of volcanic rocks.
                    Mineralogy and Petrology 46, 1–22.
                    doi: `10.1007/BF01160698 <https://dx.doi.org/10.1007/BF01160698>`__






.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  1.965 seconds)


.. _sphx_glr_download_examples_plotting_templates.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example


  .. container:: binder-badge

    .. image:: https://mybinder.org/badge_logo.svg
      :target: https://mybinder.org/v2/gh/morganjwilliams/pyrolite/develop?filepath=docs/source/examples/plotting/templates.ipynb
      :width: 150 px


  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: templates.py <templates.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: templates.ipynb <templates.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
