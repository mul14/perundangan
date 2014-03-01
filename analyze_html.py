#!/usr/bin/env python
from os import rename, listdir
from os.path import isfile, join
from re import match
from sys import argv
from lxml import html, etree

def clean1(filename, content):
    test = """
    <table align="left" border="0" cellspacing="0">
      <tbody>
        <tr>
          <td width="43"></td>

          <td></td>
        </tr>
      </tbody>
    </table>

    <p align="right"></p>

    <div align="right" class="d4"></div>
"""
    if (test in content):
        print filename
        content = content.replace(test, '')
        #print content
    return content
        
def clean2(filename, content):
    test = """
    <div class="d3">
      <small>(c)2010 Ditjen PP :: || ||</small>
    </div>
"""
    if (test in content):
        print filename
        content = content.replace(test, '')
    return content

if __name__ == '__main__':
    if len(argv) > 1:
        for f in listdir(argv[1]):
            filename = join(argv[1], f) 
            fi = open(filename, "rb")
            content = fi.read()
            fi.close()
            new_content = clean2(filename, content)
            fo = open(filename, "w")
            fo.write(new_content)
            fo.close()