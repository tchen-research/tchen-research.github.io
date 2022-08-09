#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import bibtexparser

os.environ['PATH'] += os.pathsep + '/home/tyler/anaconda3/bin/'


def bib_to_html(pub_idx,bib_entry):
    """
    given bibtex entry, output html string.
    """
    
    # build html
    html = '<div tabindex="0" class="paper">\n'\
           +f'<div class="pub-idx">[{pub_idx}]</div>'\
           +f'<div class="pub-container"><div class="title">{bib_entry["title"]}</div><br>\n'
    
    html += f'<div class="authors">{bib_entry["author"]}</div><br>\n'
           
    html += (f'<div class="journal">{bib_entry["journal"]}</div><br>\n' if "journal" in bib_entry.keys() else '')\
           +(f'<div class="journal">{bib_entry["booktitle"]}</div><br>\n' if "booktitle" in bib_entry.keys() else '')
           
    html += (f'<div class="pdf"><a href="{"./"+file_loc+".pdf" if bib_entry["pdf"]=="" else bib_info["pdf"]}">[pdf]</a></div>\n' if "pdf" in bib_entry.keys() else '')\
           +(f'<div class="doi"><a href="https://doi.org/{bib_entry["doi"]}">[journal]</a></div>\n' if "doi" in bib_entry.keys() else '')\
           +(f'<div class="eprint"><a href="https://arxiv.org/abs/{bib_entry["eprint"]}">[arXiv]</a></div>\n' if "eprint" in bib_entry.keys() else '')\
           +(f'<div class="notes">{bib_entry["note"]}.</div>\n' if "note" in bib_entry.keys() else '')
    
    html += '</div>\n</div>\n'
    
    return html


def build_html(file_name):
    """
    generate html file from markdown
    """

    print(f'now building {file_name}')

    # convert md to html

    options = ['--from markdown+tex_math_single_backslash-auto_identifiers',
               '--to html5',
               '--wrap=preserve',
               '--standalone ',
               '--mathjax',
               f'--data-dir={os.getcwd()}',
               f'--variable depth={"../"*file_name.count("/")}'
               ]

    os.system(f'pandoc {" ".join(options)} -o {file_name}.html {file_name}.md --template template.html')
    #os.system(f'pandoc -o {file_name}.pdf src/{file_name}.md')



def add_publications():
    """
    add publications to research page
    """
    
    with open('publications.bib') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    
    IDs = [bib_entry['ID'] for bib_entry in bib_database.entries]
    
    
    f = open(f'index.html','r')
    html_raw = f.read()
    f.close()

    html_new = html_raw

    for loc,regex in [('publications',r'\[pub:(.*?)\]'),('talks',r'\[talk:(.*?)\]')]:
        pubs = re.findall(regex,html_raw)
        for k,pub in enumerate(pubs):            
            for bib_entry in bib_database.entries:
                if bib_entry['ID'] == pub:
            
                    pub_html = bib_to_html(len(pubs)-k,bib_entry)

                    html_new = html_new.replace(f'[pub:{pub}]',pub_html)
                    html_new = html_new.replace(f'[talk:{pub}]',pub_html)

    f = open(f'index.html','w')
    f.write(html_new)
    f.close()

def build_cg():
    print('building CG')
    os.chdir('cg')
    os.system('python build_cg.py')
    os.chdir('../..')

build_html('index')
add_publications()