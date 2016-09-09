#!/usr/bin/env python
import click
import recastbackend.backendtasks
import recastcap.backendtasks

@click.command()
@click.argument('analysis')
@click.argument('url')
@click.argument('results')
@click.option('-t','--toplevel', default = 'from-github/pseudocap')
@click.option('--cleanup/--no-cleanup',default = True)
def main(analysis,url,results,toplevel,cleanup):
    ctx = {
        'jobguid': 'dummyjobid',
        'workflow':analysis,
        'toplevel':toplevel,
        'inputURL':url,
        'entry_point':'recastcap.backendtasks:recast',
        'backend':'testbackend',
        'shipout_base':'shipout_dummy',
        'resultlist':results.split(','),
        # 'fixed_pars':{
        #   'some_preset_par': 'dummy'
        # }
    }

    recastbackend.backendtasks.run_analysis_standalone(
        recastbackend.backendtasks.setupFromURL,
        recastbackend.backendtasks.dummy_onsuccess,
        recastbackend.backendtasks.cleanup if cleanup else lambda ctx: None,
        ctx,
        redislogging = False
    )

if __name__ == '__main__':
    main()
