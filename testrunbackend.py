#!/usr/bin/env python
import click
import recastbackend.backendtasks
import recastcap.backendtasks

@click.command()
@click.argument('analysis')
@click.argument('url')
@click.argument('results')
def main(analysis,url,results):
    ctx = {
        'jobguid': 'dummyjobid',
        'analysis':analysis,
        'inputURL':url,
        'entry_point':'recastcap.backendtasks:recast',
        'backend':'testbackend',
        'shipout_base':'shipout_dummy',
        'resultlist':results.split(',')
    }
    
    recastbackend.backendtasks.run_analysis_standalone(
        recastbackend.backendtasks.setupFromURL,
        recastbackend.backendtasks.dummy_onsuccess,
        recastbackend.backendtasks.cleanup,
        ctx,
        redislogging = False
    )
    
if __name__ == '__main__':
    main()