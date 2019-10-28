# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
import click
from cube import Cube


@click.command('cli')
@click.argument('path0', type=click.Path(exists=True))
@click.argument('path1', type=click.Path(exists=True))
def main(path0, path1):
    print('*** Reading cubes ****')
    cube0 = Cube(path0)
    cube1 = Cube(path1)

    print('*** Calculating overlap ***')
    print((cube0 * cube1))


if __name__ == '__main__':
    main()  # pylint:disable=no-value-for-parameter
