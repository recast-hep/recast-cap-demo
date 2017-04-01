#!/usr/bin/env python
import click
import recastcelery.backendtasks

@click.command()
@click.argument('analysis')
@click.argument('url')
@click.argument('results')
@click.option('-t','--toplevel', default = 'from-github/pseudocap')
@click.option('--cleanup/--no-cleanup',default = True)
def main(analysis,url,results,toplevel,cleanup):
    ctx = {
        'jobguid': 'dummyjobid',
        'shipout_spec': {
            'user': 'dummy_user',
            'host': 'dummy_host',
            'port': 'dummy_port',
            'location': 'dummy_location'
        },
        'inputURL':url,
        'backend':'testbackend',
        'entry_point':'recastyadage.backendtasks:recast',
        'resultlist':results.split(','),
        'workflow':analysis,
        'toplevel':toplevel,
    }

    recastcelery.backendtasks.run_analysis_standalone(
        recastcelery.backendtasks.setupFromURL,
        recastcelery.backendtasks.dummy_onsuccess,
        recastcelery.backendtasks.cleanup if cleanup else lambda ctx: None,
        ctx,
        redislogging = False
    )

if __name__ == '__main__':
    main()
