"""A module containing classes for building the CWL graph objects into graphviz"""
import graphviz
import os
from cwltool.cwlrdf import lastpart
from cwltool.process import shortname

class GraphHandler(object):
    def __init__(self, prefix, fmt='png'):
        self.g = graphviz.Digraph(
            name='workflow',
            format=fmt,
            graph_attr={
                'bgcolor': '#eeeeee',
                'color': 'black',
                'fontsize': "10",
                'labeljust': "left",
                'clusterrank': "local",
                'ranksep': "0.22",
                'nodesep': "0.05"
            },
            node_attr={
                'fontname': "Helvetica",
                'fontsize': "10",
                'fontcolor': "black",
                'shape': "record",
                'height': "0",
                'width': "0",
                'color': "black",
                'fillcolor': "lightgoldenrodyellow",
                'style': "filled"
            },
            edge_attr={
                'fontname': "Helvetica",
                'fontsize': "8",
                'fontcolor': "black",
                'color': "black",
                'arrowsize': "0.7"
            }
        )
        self.prefix = prefix

class CwlGraphHandler(GraphHandler):
    def process(self, workflow):
        self.addInputs(workflow)
        self.writeSteps(workflow)
        self.addOutputs(workflow)
        self.write()

    def addInputs(self, workflow):
        graph_attr = {'rank': 'same', 'style': 'dashed', 'label': 'Workflow Inputs'}
        with self.g.subgraph(name='cluster_inputs', graph_attr=graph_attr) as c:
            for inp in workflow.tool["inputs"]:
                self.addInputOutput(c, inp)

    def addOutputs(self, workflow):
        graph_attr = {'rank': 'same', 'style': 'dashed', 'label': 'Workflow Outputs'}
        with self.g.subgraph(name='cluster_outputs', graph_attr=graph_attr) as c:
            for outp in workflow.tool["outputs"]:
                self.addInputOutput(c, outp)

    def writeSteps(self, workflow):
        # Write each of the steps as a node
        for step in workflow.steps:

            label = step.tool.get('label')
            if not label:
                label = shortname(step.id)

            if step.embedded_tool.tool["class"] == "Workflow":
                self.g.node(lastpart(str(step.id)), label, fillcolor="#F3CEA1")
            else:
                self.g.node(lastpart(str(step.id)), label)

        # map inputs
        names = set([i["id"] for i in workflow.tool["inputs"]])
        indic = {}
        #indefaults = {}
        #for i in workflow.tool["inputs"]:
        #    if "default" in i: 
        #        indefaults[i["id"]] = str(i["default"])
        #defaultCounts = 0
        for step in workflow.steps:
            for inp in step.tool["inputs"]:
                source = inp["source"]
                if source in names:
                    #has_default = False
                    #if 'default' in inp:
                    #    has_default = True
                    #    default = str(inp['default'])
                    #    self.g.node("default{0}".format(defaultCounts), default, fillcolor="#D5AEFC")

                    #elif source in indefaults:
                    #    has_default = True
                    #    default = indefaults[source]
                    #    self.g.node("default{0}".format(defaultCounts), default, fillcolor="#D5AEFC")

                    #if has_default:                         
                    #    self.g.edge("default{0}".format(defaultCounts), lastpart(str(step.id)), label=shortname(source))
                    #    defaultCounts += 1
                    self.g.edge(lastpart(source), lastpart(str(step.id)))
                else:
                    if step.id not in indic: indic[step.id] = []
                    indic[step.id].append(source)

        # write links between nodes
        outdic = {}
        for i in workflow.tool["outputs"]:
            outdic[i["outputSource"]] = i

        for step in workflow.steps:
            for outp in step.tool["outputs"]:
                if outp["id"] in outdic:
                    self.g.edge(lastpart(str(step.id)), lastpart(str(outdic[outp["id"]]["id"])))

        for i in indic:
            right_step = lastpart(i)
            left_steps = []
            for k in indic[i]:
                first, rest = k.split('#')
                first = os.path.basename(first)
                rest  = os.path.dirname(rest)
                left_step = first + '#' + rest
                left_steps.append(left_step)

            for left_step in list(set(left_steps)):
                self.g.edge(left_step, right_step)

        # Workaround to force outputs to lowest ranking, see #104
        if len(workflow.tool["outputs"]) > 0:
            oiter = iter(workflow.tool["outputs"])
            for step in workflow.steps:
                try:
                    self.g.edge(lastpart(step.id), lastpart(next(oiter)['id']), style='invis')
                except StopIteration:
                    pass

    def addInputOutput(self, g, obj):
        #nodeOptions = {'fillcolor': "#94DDF4"}
        label = obj.get('label')
        if not label:
            label = shortname(obj["id"])
        g.node(lastpart(obj["id"]), label, fillcolor="#94DDF4")

    def write(self):
        self.g.render(self.prefix, view=False)
