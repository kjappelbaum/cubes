# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
import click
from cube import Cube


@click.command('cli')
@click.argument('path0', type=click.Path(exists=True))
@click.argument('path1', type=click.Path(exists=True))
@click.option('--spatial_overlap', is_flag=True)
@click.option('--overlap_invergral', is_flag=True)
def main(path0, path1, spatial_overlap, overlap_invergral):
    print('*** Reading cubes ****')
    cube0 = Cube(path0)
    cube1 = Cube(path1)
    print('*** Calculating ***')

    # If nothing selected, return both
    if overlap_invergral + spatial_overlap == 0:
        overlap_invergral, spatial_overlap = True, True
    if overlap_invergral:
        print('Overlap integral {:.4f} \n'.format((cube0 * cube1)))
    if spatial_overlap:
        print('Spatial overlap integral {:.4f}'.format((cube0.spatial_overlap(cube1))))


if __name__ == '__main__':
    main()  # pylint:disable=no-value-for-parameter
