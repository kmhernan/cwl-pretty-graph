"""A module for loading CWL files"""
from cwltool.load_tool import fetch_document, validate_document, make_tool
from cwltool.resolver import tool_resolver
from cwltool import workflow

def load_workflow(fpath):
    """Takes a path to a cwl document and returns the tool object"""
    document_loader, workflowobj, uri = fetch_document(fpath, resolver=tool_resolver,
                                                       fetcher_constructor=None)

    document_loader, avsc_names, processobj, metadata, uri \
        = validate_document(document_loader, workflowobj, uri,
                            enable_dev=False, strict=False,
                            preprocess_only=False,
                            fetcher_constructor=None,
                            skip_schemas=False)
    make_tool_kwds = {}
    make_tool_kwds["find_default_container"] = None

    tool = make_tool(document_loader, avsc_names, metadata, uri,
                     workflow.defaultMakeTool, make_tool_kwds)
    return tool
