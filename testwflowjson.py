#!/usr/bin/env python
import click
import wflowbackend.backendtasks
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

    wflowbackend.backendtasks.run_analysis_standalone(
        wflowbackend.backendtasks.setupFromURL,
        wflowbackend.backendtasks.dummy_onsuccess,
        wflowbackend.backendtasks.cleanup if cleanup else lambda ctx: None,
        ctx,
        redislogging = False
    )

if __name__ == '__main__':
    main()
