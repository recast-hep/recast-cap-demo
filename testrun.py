#!/usr/bin/env python
import click
import recastcap.backendtasks

@click.command()
@click.argument('analysis')
@click.argument('jobguid')
def main(analysis,jobguid):
    recastcap.backendtasks.recast({'analysis':analysis,'jobguid':jobguid})
    
if __name__ == '__main__':
    main()