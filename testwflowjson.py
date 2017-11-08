#!/usr/bin/env python
import click
import wflowcelery.backendtasks
import yadageschemas
@click.command()
@click.argument('workflow')
@click.argument('url')
@click.argument('results')
@click.option('-t','--toplevel', default = 'from-github/pseudocap')
@click.option('--cleanup/--no-cleanup',default = True)
def main(workflow,url,results,toplevel,cleanup):
    ctx = {
        'jobguid': 'dummyjobid',
        'shipout_base':'shipout_dummy',
        'inputURL':url,

        'backend':'testbackend',
        'entry_point':'wflowyadageworker.backendtasks:run_workflow',
        'resultlist':results.split(','),
        'workflow_json': yadageschemas.load(workflow, toplevel, 'yadage/workflow-schema')
    }

    wflowcelery.backendtasks.run_analysis_standalone(
        wflowcelery.backendtasks.setupFromURL,
        wflowcelery.backendtasks.dummy_onsuccess,
        wflowcelery.backendtasks.cleanup if cleanup else lambda ctx: None,
        ctx,
        redislogging = False
    )

if __name__ == '__main__':
    main()
