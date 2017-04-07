#!/usr/bin/env python
import click
import recastcelery.backendtasks

specs = {}

specs['spec1'] =  {
    'adapter': {
        'toplevel': '/Users/lukas/Code/yadagedev/dynamic_compose/sherpa',
        'workflow': 'sherpagen.yml',
        'interface_parameters': {
            'hepmcfiles': {'stages': 'upstream.[0].sherpa', 'output': 'hepmcfile', 'unwrap': True}
        }
    }, 
    'analysis':  {
        'toplevel': '/Users/lukas/Code/yadagedev/dynamic_compose/sherpa',
        'workflow': 'rivetanflow.yml',
        'preset_pars': {
            'analysis': 'MC_GENERIC'
        }
    }
}
specs['spec2'] =  {
    'adapter': 'from-request', 
    'analysis':  {
        'toplevel': '/Users/lukas/Code/yadagedev/dynamic_compose/sherpa',
        'workflow': 'rivetanflow.yml',
        'preset_pars': {
            'analysis': 'MC_GENERIC'
        }
    }
}

specs['spec3'] = {
    'adapter': {
        'toplevel': 'from-github/mcevgen/pythia_delphes',
        'interface_parameters': {
            'xsecval': {'output': 'xsection.value', 'stages': 'upstream.[0].init', 'unwrap': True},
            'rootfiles': {'output': 'rootfile', 'stages': 'upstream.[0].delphes'},
            'xsec_in_pb': {'output': 'xsec_in_pb', 'stages': 'upstream.[0].init', 'unwrap': True}
        },
        'workflow': 'workflow.yml'
    },
    'analysis': {
        'toplevel': 'from-github/recast_analyses/delphes_analysis',
        'preset_pars': {
            'obsdata': '/some/obs/data',
            'storedbgdata': '/some/bg/data'
        },
        'workflow': 'analysis_flow.yml'
    }
}


specs['spec4'] =  {
    'adapter': {
        'toplevel': 'from-github/mcevgen/pythia_delphes',
        'interface_parameters': {
            'rootfiles': {'output': 'rootfile', 'stages': 'upstream.[0].delphes'},
            'xsec_in_pb': {'output': 'xsec_in_pb', 'stages': 'upstream.[0].init', 'unwrap': True}
        },
        'workflow': 'workflow.yml'
    },
    'analysis': {
        'toplevel': 'from-github/recast_analyses/delphes_analysis',
        'preset_pars': {'obsdata': '/some/obs/data', 'bgdata': '/some/bg/data'},
        'workflow': 'analysis_flow.yml'}
}

@click.command()
@click.argument('url')
@click.argument('specname')
@click.argument('results')
@click.option('--cleanup/--no-cleanup',default = True)
def main(url,results,specname,cleanup):
    ctx = {
        'jobguid': 'dummyjobid',
        'entry_point':'yadageworker.backendtasks:recast',
        'backend':'testbackend',
        'shipout_base':'shipout_dummy',
        'resultlist':results.split(','),
        'inputURL':url,
        'combinedspec': specs[specname]
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
