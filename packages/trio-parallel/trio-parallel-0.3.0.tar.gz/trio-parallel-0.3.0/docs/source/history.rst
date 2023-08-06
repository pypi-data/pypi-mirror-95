trio-parallel 0.3.0 (2021-02-21)
--------------------------------

Bugfixes
~~~~~~~~

- Fixed an underlying race condition in IPC. Not a critical bugfix, as it should not be triggered in practice. (`#15 <https://github.com/richardsheridan/trio-parallel/issues/15>`__)
- Reduce the production of zombie children on Unix systems (`#20 <https://github.com/richardsheridan/trio-parallel/issues/20>`__)
- Close internal race condition when waiting for subprocess exit codes on macOS. (`#23 <https://github.com/richardsheridan/trio-parallel/issues/23>`__)
- Avoid a race condition leading to deadlocks when a worker process is killed right after receiving work. (`#25 <https://github.com/richardsheridan/trio-parallel/issues/25>`__)


Improved Documentation
~~~~~~~~~~~~~~~~~~~~~~

- Reorganized documentation for less redundancy and more clarity (`#16 <https://github.com/richardsheridan/trio-parallel/issues/16>`__)


Release history
===============

.. currentmodule:: trio_parallel

.. towncrier release notes start

trio_parallel 0.2.0 (2021-02-02)
--------------------------------

Bugfixes
~~~~~~~~

- Changed subprocess context to explicitly always spawn new processes (`#5 <https://github.com/richardsheridan/trio-parallel/issues/5>`__)
- Changed synchronization scheme to achieve full passing tests on

  - Windows, Linux, MacOS
  - CPython 3.6, 3.7, 3.8, 3.9
  - Pypy 3.6, 3.7, 3.7-nightly

  Note Pypy on Windows is not supported here or by Trio (`#10 <https://github.com/richardsheridan/trio-parallel/issues/10>`__)
