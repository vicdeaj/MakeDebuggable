#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libaml.aml import AML
from libaml.aml import ResTypes
from libaml.aml import ResXMLTree_attribute


INDENT_BLOCK = '  '

if __name__ == '__main__':
    infile = "AndroidManifest.xml"
    outfile = "out.xml"

    # bulk infile to buf
    with open(infile, "rb") as fp:
        buf = fp.read()

    # create AML object for manipulation
    aml = AML(buf)



    while aml.hasnext():
        header, body = aml.next()
        if header.type == ResTypes.RES_XML_START_ELEMENT_TYPE and body.nodename == "application":
            # remove attributes if present
            for t in body.attributes:
                if str(t) == "android:allowBackup":
                #    body.attributes.remove(t)
                    pass
                if str(t) == "android:debuggable":
                    body.attributes.remove(t)

            # add atributes with desired parameters
            newAttribute = ResXMLTree_attribute.make(AML.ANDROID_NAMESPACE,aml.stringpool,"allowBackup",True)
            body.attributes.append(newAttribute)

    INDENT_BLOCK = '  '
    indent = 0
    namespaces = []
    # only checking
    buf2 = aml.tobytes()
    aml2 = AML(buf2)
    while aml2.hasnext():
        header, body = aml2.next()
        if header.type == ResTypes.RES_XML_START_ELEMENT_TYPE:
            print(INDENT_BLOCK * indent + '<%s%s>' % (
            body.nodename, ''.join(namespaces + [' %s="%s"' % (i, i.typedValue.value) for i in body.attributes])))
            namespaces = []
            indent += 1
        elif header.type == ResTypes.RES_XML_END_ELEMENT_TYPE:
            indent -= 1
            print(INDENT_BLOCK * indent + '</%s>' % body.nodename)
        elif header.type == ResTypes.RES_XML_START_NAMESPACE_TYPE:
            namespaces.append(' xmlns:%s="%s"' % (body.name, body.namespace))
        elif header.type == ResTypes.RES_XML_TYPE:
            print('<?xml version="1.0" encoding="utf-8"?>')










