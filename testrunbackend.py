#!/usr/bin/env python
import click
import wflowbackend.backendtasks
import yadage.utils as utils
@click.command()
@click.argument('workflow')
@click.argument('url')
@click.argument('results')
@click.option('-t','--toplevel', default = 'from-github/pseudocap')
@click.option('-p', '--parameter', multiple=True, help = '<parameter name>=<yaml string> input parameter specifcations ')
@click.option('--cleanup/--no-cleanup',default = True)
def main(workflow,url,results,toplevel,parameter,cleanup):

    initdata = utils.getinit_data([], parameter)
    ctx = {
        'jobguid': 'dummyjobid',
        'shipout_base':'shipout_dummy',
        'inputURL':url,
        'inputAuth': True,
        'backend':'testbackend',
        'entry_point':'wflowyadageworker.backendtasks:run_workflow',
        'resultlist':results.split(','),
        'preset_pars': initdata,
        'workflow':workflow,
        'toplevel':toplevel,
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
