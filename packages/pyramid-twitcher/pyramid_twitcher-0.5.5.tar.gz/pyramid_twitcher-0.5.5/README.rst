=====================================
Twitcher: A simple OWS Security Proxy
=====================================

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
   :target: http://twitcher.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/bird-house/twitcher.svg?branch=master
   :target: https://travis-ci.org/bird-house/twitcher
   :alt: Travis Build

.. image:: https://img.shields.io/github/license/bird-house/twitcher.svg
   :target: https://github.com/bird-house/twitcher/blob/master/LICENSE.txt
   :alt: GitHub license

.. image:: https://badges.gitter.im/bird-house/birdhouse.svg
   :target: https://gitter.im/bird-house/birdhouse?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
   :alt: Join the chat at https://gitter.im/bird-house/birdhouse


Twitcher (the bird-watcher)
  *a birdwatcher mainly interested in catching sight of rare birds.* (`Leo <https://dict.leo.org/ende/index_en.html>`_).

Twitcher is a security proxy for Web Processing Services (WPS). The execution of a WPS process is blocked by the proxy.
The proxy service uses access tokens (UUID) to run a WPS process.
The access tokens are valid only for a short period of time.
In addition one can also use X.509 certificates for WPS client authentication.

The implementation is not restricted to WPS services.
It will be extended to more OWS services like WMS (Web Map Service) and CSW (Catalogue Service for the Web)
and might also be used for Thredds catalog services.

Twitcher extensions:

* `Magpie`_ is an AuthN/AuthZ service provided by the `PAVICS`_ project.
* `Weaver`_  middleware by CRIM_. A reimplementation of an old `Twitcher fork <https://github.com/ouranosinc/twitcher/>`_
  for workflow execution and a Swagger RESTful interface for Web Processing Services.

Twitcher is implemented with the Python `Pyramid`_ web framework.

Twitcher is part of the `Birdhouse`_ project. The documentation is on `ReadTheDocs`_.

Twitcher `Docker`_ images are also available for most recent tagged versions.

.. _Birdhouse: http://birdhouse.readthedocs.io/en/latest/
.. _Pyramid: http://www.pylonsproject.org
.. _ReadTheDocs: http://twitcher.readthedocs.io/en/latest/
.. _Magpie: https://github.com/Ouranosinc/Magpie
.. _PAVICS: https://ouranosinc.github.io/pavics-sdi/index.html
.. _Weaver: https://github.com/crim-ca/weaver
.. _CRIM: https://www.crim.ca/en
.. _Swagger: https://swagger.io/
.. _Docker: https://cloud.docker.com/u/birdhouse/repository/docker/birdhouse/twitcher/general
