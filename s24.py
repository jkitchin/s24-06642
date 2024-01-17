# adapted from https://forums.fast.ai/t/jupyter-notebook-enhancements-tips-and-tricks/17064/39
# and https://discourse.jupyter.org/t/how-to-get-kernel-state-from-running-local-jupyter-notebook/15028/6

import os
import requests
import ipykernel
from notebook import notebookapp

import urllib, json, ipykernel


from nbconvert import HTMLExporter
from notebook_as_pdf import PDFExporter
import nbformat
import re
import tempfile
import subprocess
import time

import shlex
from IPython.core.magic import register_line_magic

from IPython.display import HTML, Markdown


def get_notebook_path():
    """Returns the absolute path of the Notebook or None if it cannot be determined
    NOTE: works only when the security is token-based or there is also no password
    """
    connection_file = os.path.basename(ipykernel.get_connection_file())
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]

    payload = {'token': os.environ['JUPYTERHUB_API_TOKEN']}
    
    for srv in notebookapp.list_running_servers():
        result = requests.get(srv['url'] + 'api/sessions', params=payload)
        sessions = result.json()

        for sess in sessions:
            if sess['kernel']['id'] == kernel_id:
                return os.path.join(srv['notebook_dir'],sess['notebook']['path'])
    return None





def pdf_from_html(pdf=None, verbose=False):
    """Export the current notebook as a PDF.
    pdf is the name of the PDF to export.
    """
    if verbose:
        print("PDF via notebook_to_pdf")

    fname = get_notebook_path() # absolute path to notebook
    root, fn = os.path.split(fname)
    
    p = fname.replace(os.environ['HOME'] + '/', '')
    url =  ('https://jupyterhub-dev.cheme.cmu.edu' + 
             os.environ['JUPYTERHUB_SERVICE_PREFIX'] +
            'lab/tree/' + p)
    
    md = nbformat.notebooknode.from_dict({'cell_type': 'markdown',
                                          'metadata': {},
                                          'source': f'Generated at {time.asctime()}. \n\n Source at [{url}]({url}).'})
        
    with open(fname) as f:
        ipynb = f.read()

    exporter = PDFExporter()

    nb = nbformat.reads(ipynb, as_version=4)
    
    # One problem with this package is it doesn't show local images because the html is generated in a temp directory.
    # Here we try to use absolute paths.
    # Replace local paths with full paths
    # From https://github.com/betatim/notebook-as-pdf/issues/18
    RE_local_Images = re.compile(r"!\[(.*)\]\((?!https?://|[A-Z]:\\|/|~/)(.*?)( (\"|').*(\"|'))?\)")

    for cell in nb['cells']:
        if not cell['cell_type'] == 'markdown':
            continue

        offset = 0
        
        for match in RE_local_Images.finditer(cell['source']):
            path = match.group(2)
            fullpath = (os.path.realpath(os.path.join(root, path))).replace(' ', '%20')
            cell['source'] = cell['source'][:match.start(2)+offset] + fullpath + cell['source'][match.end(2)+offset:]
            offset += len(fullpath)-(match.end(2)-match.start(2))                
    
    # insert header    
    nb['cells'].insert(0, md)
    body, resources = exporter.from_notebook_node(nb)
    
    base, ext = os.path.splitext(fname)
    pdf = base + '.pdf'
    with open(pdf, 'wb') as f:
        f.write(body)

    rpath = os.path.relpath(pdf, os.getcwd())
    
    display(Markdown(f'[Open {rpath}]({rpath})'))
            
    html = HTML(f'<a href="{rpath}" download="{os.path.split(rpath)[-1]}">download {rpath}</a>')
    display(html)


            
def pdf(line=""):
    """Line magic to export a notebook to PDF.
    """
    args = shlex.split(line)

    if args and args[-1].endswith(".pdf"):
        pdf = args[-1]
    else:
        pdf = None

    verbose = "-v" in args

    pdf_from_html(pdf, verbose)
    
try:
    pdf = register_line_magic(pdf)
except:
    pass



# Update environment
#import os
#if not os.path.exists(os.path.expanduser('~/share')):
#    os.symlink('/usr/local/share/s24-06623',os.path.expanduser('~/share'), target_is_directory=True)
    