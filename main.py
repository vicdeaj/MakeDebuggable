#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libaml.aml import *
import zipfile2 as zipfile
import shutil
from apk_signer.apksigner import remove_meta_inf, zipalign, apksign


if __name__ == '__main__':
    # copy input to output
    infile = "base.apk"
    outfile = "out.apk"

    shutil.copy(infile, outfile)
    x = zipfile.ZipFile(outfile, "a")
    manifest = x.open("AndroidManifest.xml","r")

    # create AML object for manipulation
    aml = AML(manifest.read())
    manifest.close()

    while aml.hasnext():
        header, body = aml.next()

        if header.type == ResTypes.RES_XML_START_ELEMENT_TYPE and body.nodename == "application":
            # remove attributes if present
            for t in body.attributes:
                if str(t) == "android:allowBackup":
                    body.attributes.remove(t)
                if str(t) == "android:debuggable":
                    body.attributes.remove(t)

            androidns = ResourceRef.create(stringpool=aml.stringpool, value=AML.ANDROID_NAMESPACE)
            allowBackupValue = ResourceRef.create(stringpool=aml.stringpool, value="allowBackup")
            debuggableValue = ResourceRef.create(stringpool=aml.stringpool, value="debuggable")

            # add atributes with desired parameters
            newAttribute = ResXMLTree_attribute.make(androidns, aml.stringpool, allowBackupValue, True)
            body.attributes.append(newAttribute)

            newAttribute2 = ResXMLTree_attribute.make(androidns, aml.stringpool, debuggableValue, True)
            body.attributes.append(newAttribute2)

    print(aml.tobytes())
    exit(0)
    x.remove("AndroidManifest.xml")
    manifest = x.open("AndroidManifest.xml", "w")
    manifest.write(aml.tobytes())
    manifest.close()
    x.close()

    remove_meta_inf(outfile)
    zipalign(outfile)
    apksign(outfile)
















