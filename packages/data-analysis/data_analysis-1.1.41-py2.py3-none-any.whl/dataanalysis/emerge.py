import os
import json
import yaml as yaml
import argparse

import dataanalysis.importing as importing
from dataanalysis.caches.resources import jsonify
from dataanalysis.printhook import log, log_logstash
import dataanalysis.graphtools
from dataanalysis import hashtools
import dataanalysis.core as da
import imp

dd_module_names=[]

def import_ddmodules(module_names=None):
    if module_names is None:
        module_names=dd_module_names

    modules=[]
    for dd_module_name in module_names:
        if isinstance(dd_module_name,str) and dd_module_name.startswith("dataanalysis."):
            continue

        log("importing", dd_module_name,level="top")
        dd_module=importing.load_by_name(dd_module_name)
        modules.append(dd_module[0])

        log("module",dd_module[1],"as",dd_module[0],"set to global namespace",level="top")
        globals()[dd_module[1]]=dd_module[0]

 #       reload(dd_module[0])

    return modules

class InconsitentEmergence(Exception):
    def __init__(self,message,cando,wanttodo):
        self.message=message
        self.cando=cando
        self.wanttodo=wanttodo

    def __repr__(self):
        return self.__class__.__name__+": "+repr(self.message)

def emerge_from_identity(identity):
    da.reset()

    imp.reload(dataanalysis.graphtools)
    print(("fresh factory knows",da.AnalysisFactory.cache))


    import_ddmodules(identity.modules)

    log("assumptions:",identity.assumptions)

    #A = da.AnalysisFactory.byname(identity.factory_name)


    for i,assumption in enumerate(identity.assumptions):
        log("requested assumption:", assumption)

        if assumption[0] == '':
            log("ATTENTION: dangerous eval from string",assumption[1])
            da.AnalysisFactory.WhatIfCopy('queue emergence %i'%i, eval(assumption[1]))
        else:
            a = da.AnalysisFactory.byname(assumption[0])
            a.import_data(assumption[1])
            da.AnalysisFactory.WhatIfCopy('queue emergence %i'%i, a)

            log("emerge_from_identity uses assumption", a, level="top")

    A = da.AnalysisFactory.byname(identity.factory_name)
    producable_hashe=A.get_hashe()

    producable_hashe_jsonified=jsonify(hashtools.hashe_replace_object(producable_hashe, None, "None"))
    expected_hashe_jsonified=jsonify(identity.expected_hashe)

    if identity.expected_hashe is None or identity.expected_hashe == "None":
        log("expected hashe verification skipped")
    elif producable_hashe_jsonified != expected_hashe_jsonified:
        log("producable:\n",jsonify(producable_hashe_jsonified),"\n",level="top")
        log("requested:\n",jsonify(expected_hashe_jsonified),level="top")

        try:
            from dataanalysis import displaygraph
            displaygraph.plot_hashe(producable_hashe_jsonified,"producable.png")
            displaygraph.plot_hashe(expected_hashe_jsonified,"expected.png")
        except Exception as e:
            pass

        log_logstash("emergence exception",note="inconsistent_emergence",producable=producable_hashe_jsonified,expected_hashe=expected_hashe_jsonified)

        raise InconsitentEmergence(
            "unable to produce\n"+repr(producable_hashe_jsonified)+"\n while can produce"+repr(expected_hashe_jsonified),
            producable_hashe_jsonified,
            expected_hashe_jsonified,
        )

    log("successfully emerged")

    return A

def emerge_from_graph(graph):
    pass


def main():
    log('hello world')


    parser = argparse.ArgumentParser(description='client to remote dda combinator')
    parser.add_argument('target')
    parser.add_argument('-p',dest='just_print',action='store_true',default=False)
    parser.add_argument('-F',dest='from_file',action='store_true',default=False)
    parser.add_argument('-m',dest='modules',action='append',default=[])
    parser.add_argument('-a',dest='assume',action='append',default=[])
    parser.add_argument('-i',dest='inject',action='append',default=[])
    parser.add_argument('-D',dest='prompt_delegate',action='store_true',default=False)
    parser.add_argument('-H',dest='from_hub',action='store_true',default=False)

    args = parser.parse_args()

    custom_source_flags = { k:getattr(args, k) for k in ['from_hub', 'from_file'] }

    if sum(custom_source_flags.values()) > 1:
        raise Exception(f"{', '.join(custom_source_flags.keys())} are mutually exclusive!")

    if sum(custom_source_flags.values()) == 0:
        log("target:",args.target)
        log("modules:",args.modules)

    if args.from_hub:
        import dqueue
        q = dqueue.from_uri(os.environ.get('ODAHUB', None))
        ti = json.loads(q.task_info(args.target)['task_dict_string'])
        print(ti)
        identity=da.DataAnalysisIdentity.from_dict(ti['task_data']['object_identity'])

    if args.from_file:
        identity=da.DataAnalysisIdentity.from_dict(yaml.load(open(args.target)))

    if args.just_print:
        print(identity)

        c = identity.factory_name

        for m in identity.modules:
            print(m)
            if m[0] == 'git':
                if m[2] is None or m[2] == 'None':
                    c += f' -m git://{m[1]}'
                else:
                    c += f' -m git://{m[1]}/{m[2]}'
            else:
                c += f' -m {m}'

        for a in identity.assumptions:
            if a[0] == '':
                c += ' -a \'' + str(a[1]) + '\''
        
        print(c)
    else:
        emerge_from_identity(identity).get()


if __name__ == "__main__":
    main()
