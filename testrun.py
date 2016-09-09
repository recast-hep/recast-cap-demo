#!/usr/bin/env python
import click
import recastcap.backendtasks

@click.command()
@click.argument('analysis')
@click.argument('jobguid')
@click.option('-t','--toplevel', default = 'from-github/pseudocap')
def main(analysis,jobguid,toplevel):
    recastcap.backendtasks.recast({
        'workflow':analysis,
        'jobguid':jobguid,
        'toplevel':toplevel
    })

if __name__ == '__main__':
    main()
