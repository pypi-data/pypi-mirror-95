git; Mirror Upstream to Local to Downstream (muld)
==================================================

.. image:: https://img.shields.io/pypi/v/muld.svg
   :target: https://pypi.org/project/muld
   :alt: PyPI

Provide a list of repository upstream/downstream pairs such as::

  repos:
    - name: "spdk"
      upstream: "https://github.com/spdk/spdk"
      downstream: "ssh://git@example.com/somewhere/else/spdk.git"
    - name: "dpdk"
      upstream: "https://github.com/spdk/dpdk.git"
      downstream: "ssh://git@example.com/somewhere/else/dpdk.git"

In a file and name it as e.g. ``muld.yml``. Then invoke ``muld``::

  muld --mirrors $HOME/mirrors --conf muld.yml

It will initially clone the **upstream**, if it exists then just fetch and
prune, then push tags and branches to **downstream**.

If ``--conf`` is not given, then it assumes that a file named ``muld.yml``
exists inside the directory pointed to by ``--mirrors``.

If ``--mirrors`` is not given, then it uses the current-working-dir.

E.g. if you have prepared home for mirrors with a config inside it::

  # Setup
  mkdir $HOME/mirrors
  echo "repos: [{upstream: 'https://github.com/spdk/spdk'}]" > muld.yml
  cd $HOME/mirrors

Then you can just goto the directory and run ``muld``::

  # Run it...
  cd $HOME/mirrors
  muld

Regarding the config-file, only ``upstream`` is required. When ``name`` is left
out, then ``muld`` will produce a named based on the given ``upstream`` URL.

If ``downstream`` is left out, then it simply won't push anywhere, it will just
clone, prune and fetch.
