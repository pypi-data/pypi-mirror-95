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

In a file and name it as e.g. ``repos.yml``. Then invoke ``muld``::

  muld --yaml repos.yml --mirrors $HOME/mirrors

It will initially clone the **upstream**, if it exists then just fetch and
prune, then push tags to **downstream**.
