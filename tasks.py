#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from invoke import run, task
from invoke.util import log


@task
def clean(ctx):
    """clean - remove build artifacts."""
    run('rm -rf build/')
    run('rm -rf dist/')
    run('rm -rf mdpy.egg-info')
    run('find . -name __pycache__ -delete')
    run('find . -name *.pyc -delete')
    run('find . -name *.pyo -delete')
    run('find . -name *~ -delete')

    log.info('cleaned up')


@task
def test(ctx):
    """test - run the test runner."""
    run('py.test --flakes --cov-report html --cov mdpy tests/', pty=True)
    run('open htmlcov/index.html')


@task
def lint(ctx):
    """lint - check style with flake8."""
    run('flake8 mdpy tests')


@task(clean)
def publish(ctx):
    """publish - package and upload a release to the cheeseshop."""
    run('python setup.py sdist upload', pty=True)
    run('python setup.py bdist_wheel upload', pty=True)

    log.info('published new release')

@task
def convert_notebooks(ctx):
    """Convert notebooks to HTML"""
    run('''python ./scripts/convert_notebooks.py notebooks/*.ipynb --exclude='_*' --outdir=notebooks/html''')
    log.info('Converted notebooks to HTML')
