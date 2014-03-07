#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import rename, listdir
from os.path import isfile, isdir, join
from sys import argv
import re
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
        
clean2regex = re.compile("<div class=\"d3\">\s+<small>\(c\)2010 Ditjen PP :: \|\| \|\|</small>\s+</div>")
def clean2(filename, content):
    test = """
    <div class="d3">
      <small>(c)2010 Ditjen PP :: || ||</small>
    </div>
"""
    new_content = clean2regex.sub("", content)
    if (new_content != content):
        print filename
    return new_content

def clean3(filename, content):
    test = "<div class=\"d3\" align=\"right\"></div>"
    if (test in content):
        print filename
        content = content.replace(test, '')
    return content

clean4regex = re.compile("<img src=\"([a-zA-Z\./]+)\" border=\"0\">(\s+)?(<br>)?(\s+)?(<br>)?")
def clean4(filename, content):
    new_content = clean4regex.sub("", content)
    if (new_content != content):
        print filename
    return new_content

def clean5(filename, content):
    text = '&Acirc;&nbsp;'
    if (text in content):
        print filename
        content = content.replace(text, ' ')
    return content

clean6regex1 = re.compile("\b\s+|\n\s+|\s+\n|\s+\b");
clean6regex2 = re.compile("^(Menimbang|Mengingat|Menetapkan|Memperhatikan|Mendengar|Kepada)(\s+)?:");
def clean6(filename, content):
    html_content = html.fromstring(content)
    sm_parts = html_content.xpath('//div[@class=\'sm\']')
    for sm_part in sm_parts:
        text = clean6regex1.sub(' ', sm_part.text).strip()
        match = clean6regex2.match(text)
        if (match):
            print filename
            element = html.Element('div', {'class': 'xsm'})
            element.text = ''
            parent = sm_part.getparent()
            
            element2 = html.Element('strong')
            element2.text = match.group(1)


            element.append(element2)
            ol = html.Element('ol')
            li = html.Element('li')
            li.text = clean6regex2.sub('', text).strip() 
            ol.append(li)

            sibling = sm_part.getnext()
            sm_siblings = []
            while (sibling is not None and sibling.get('class') == 'sm1'):
                sm_siblings.append(sibling)
                sibling = sibling.getnext()
            for sibling in sm_siblings:
                if (sibling.text is not None):
                    li = html.Element('li')
                    li.text = clean6regex1.sub(' ', sibling.text).strip()
                    ol.append(li)
                parent.remove(sibling)

            element.append(ol)
            sm_part.addprevious(element)
            parent.remove(sm_part)

    return etree.tostring(html_content)


#Parse string PASAL XX in <center></center> and replace it with h4
clean7regex1 = re.compile('Pasal (\d+)(\s+)</center>')
def clean7(filename, content):
    print filename
    content = clean7regex1.sub('</center><h4>Pasal \g<1></h4>', content)
    return content

clean8regex1 = re.compile("<\/h4>(.*?)<br>\n\n", re.DOTALL)
def clean8(filename, content):
    return clean8regex1.sub("</h4><div class=\"sx\">\g<1></div><br>\n\n", content)

def clean9(filename, content):
    return content.replace('</div><br>', '</div>')

clean10regex1 = re.compile('No\.\s?(\d+),\s?(\d{4})')
def clean10(filename, content):
    html_content = html.fromstring(content)
    small = html_content.xpath('//table//small')
    if (len(small) > 0):
        small = small[0]
        if (clean10regex1.match(small.text)):
            bodies = small.iterancestors('body')
            print len(bodies)
            small.getparent().remove(small)

#This will convert group of s14 to OL/LI
def clean11(filename, content):
    html_content = html.fromstring(content)
    sx_parts = html_content.xpath('//div[@class=\'sx\']')
    tags = []
    for sx_part in sx_parts:
        children = sx_part.getchildren()
        no_extra_text = not any(child.tail and child.tail.strip() for child in children)
        all_class_s14 = all(child.get('class')  == 's14' for child in children)
        no_text = sx_part.text and not sx_part.text.strip()
        if children and no_extra_text and no_text and all_class_s14:
            tags.append(sx_part)

    if (len(tags) > 0):
        print filename
    for sx_part in tags:
        sx_part.tag = 'ol'
        for child in sx_part.getchildren():
            child.tag = 'li'

    return etree.tostring(html_content)

def clean12(filename, content):
    return content.replace('<br/></div>', '</div>')

def processfile(filename):
    fi = open(filename, "rb")
    content = fi.read()
    fi.close()
    new_content = clean12(filename, content)
    fo = open(filename, "w")
    fo.write(new_content)
    fo.close()

if __name__ == '__main__':
    if len(argv) > 1:
        if (isfile(argv[1])):
            processfile(argv[1])
        elif (isdir(argv[1])):
            for f in listdir(argv[1]):
                filename = join(argv[1], f) 
                processfile(filename)