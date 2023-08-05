=============
hg-fastimport
=============

WARNING: this extension is incomplete and lightly tested.  It is
currently intended for Mercurial developers or particularly daring
users.

hg-fastimport is a Mercurial extension for importing Git's fast-import
dumps into Mercurial. fast-import is a file format for representing the
entire history of a version control repository.

This file format was designed to make it easier to write tools which
convert from foreign (non-Git) VCS repository formats into Git; such
tools exist for CVS, Mercurial, Darcs, and Perforce.

==============
How to Install
==============

Using Pip
---------

You can install the latest released version using pip::

  $ pip install --user hg-fastimport

Then enable it in yourn hgrc::

  [extensions]
  fastimport =

From Source
-----------

To install a local version from source::

  $ hg clone https://roy.marples.name/hg/hg-fastimport/
  $ cd hg-fastimport
  $ pip install --user .

Then enable it in your hgrc::

  [extensions]
  fastimport =

==========
How to Use
==========

To import into a brand-new Mercurial repository::

  $ hg init new
  $ cd new
  $ hg fastimport --datesort FILE...

where FILE... is a list of one or more fast-import dumps.
