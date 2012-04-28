#/usr/bin/python
'''
@author: chengzhenyu@baidu.com
@date: 2012-03-31
'''

import os
import sys
import string
import getopt
import traceback
from datetime import datetime

VERION = "1.0"
debug = False

targetpackage = None
casepath = None
applicationname = None
certificate = None
activity = None
activityfullname = None

def gettargetpackage():
    if (targetpackage != None):
        logm("targetpackage = " + targetpackage)
        return targetpackage
    else:
        raise Exception,  "[casegen]exception:\n targetpackage is None"

def getcasepath():    
    casepath = targetpackage.replace(r".", r"/") + r"/tests"
    if (casepath != None):
        logm("casepath = " + casepath)
        return casepath
    else:
        raise Exception,  "[casegen]exception:\n casepath is None"
    
def getapplicationname():
    strlist = gettargetpackage().split('.')
    applicationname = strlist[len(strlist) - 1]
    applicationname = applicationname.capitalize()
    if (applicationname != None):
        logm("applicationname = " + applicationname)
        return applicationname
    else:
        raise Exception,  "[casegen]exception:\n applicationname is None"

def getcertificate():
    if (certificate != None):
        logm("certificate = " + certificate)
        return "LOCAL_CERTIFICATE := " + certificate
    else:
        logm("certificate = None")
        return ""

def getactivity():
    strlist = getactivityfullname().split('.')
    activity = strlist[len(strlist) - 1]
    
    if (activity != None):
        logm("activity = " + activity)
        return activity
    else:
        raise Exception,  "[casegen]exception:\n activity is None"

def getactivityfullname():
    if (activityfullname != None):
        logm("activityfullname = " + activityfullname)
        return activityfullname
    else:
        raise Exception,  "[casegen]exception:\n activityfullname is None" 

def getdatetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getcomment():
    return "The code was generated by CAFE casegen tool " + VERION + " on " + getdatetime()
    
def foldergen():    
    os.makedirs(r"Cafe" + getapplicationname() + "Test/cafe_tests/src/" + getcasepath())
    os.makedirs(r"Cafe" + getapplicationname() + "Test/cafe_tests/res/values")

def manifestgen():
    template = \
        "<?xml version=\"1.0\" encoding=\"utf-8\"?>" + "\n" + \
        "<!-- " + getcomment() + " -->" + "\n" + \
        "<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\"" + "\n" + \
        "    package=\"" + gettargetpackage() + ".tests\">" + "\n" + \
        "    <application>" + "\n" + \
        "        <uses-library android:name=\"android.test.runner\" />" + "\n" + \
        "    </application>" + "\n" + \
        "    <instrumentation android:name=\"com.baidu.cafe.junitreport.JUnitReportTestRunner\" android:targetPackage=\"" + gettargetpackage() + "\"/>"  + "\n" + \
        "    <instrumentation android:name=\"com.baidu.cafe.cafetestrunner.InstrumentationTestRunner\" android:targetPackage=\"" + gettargetpackage() + "\"/>"  + "\n" + \
        "    <instrumentation android:name=\"android.test.InstrumentationTestRunner\""  + "\n" + \
        "        android:targetPackage=\"" + gettargetpackage() + "\""  + "\n" + \
        "        android:label=\"" + getapplicationname() + " test\">"  + "\n" + \
        "    </instrumentation>"+ "\n" + \
        "</manifest>" + "\n"
    
    f = open(r"Cafe" + getapplicationname() + "Test/cafe_tests/AndroidManifest.xml",'w')
    f.writelines(template)
    f.close()

def mkgen():
    template = \
        "# " + getcomment() + "\n" + \
        "LOCAL_PATH:= $(call my-dir)" + "\n" + \
        "include $(CLEAR_VARS)" + "\n" + \
        "\n" + \
        "LOCAL_MODULE_TAGS := tests" + "\n" + \
        "LOCAL_STATIC_JAVA_LIBRARIES := libCafe" + "\n" + \
        "LOCAL_JAVA_LIBRARIES := framework-yi android.test.runner" + "\n" + \
        "LOCAL_USE_YI_RES := true" + "\n" + \
        "\n" + \
        "LOCAL_SRC_FILES := $(call all-java-files-under, src)" + "\n" + \
        "LOCAL_PACKAGE_NAME := " + getapplicationname() + "Tests" + "\n" + \
        "LOCAL_INSTRUMENTATION_FOR := " + getapplicationname() + "\n" + \
        getcertificate() + "\n" + \
        "include $(BUILD_PACKAGE)" + "\n" + \
        "LOCAL_PREBUILT_STATIC_JAVA_LIBRARIES := libCafe:../../../for_development/cafe.jar" + "\n" + \
        "include $(BUILD_MULTI_PREBUILT)" + "\n"
    
    f = open(r"Cafe" + getapplicationname() + "Test/cafe_tests/Android.mk",'w')
    f.writelines(template)
    f.close()

def stringgen():
    template = \
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + "\n" + \
        "<!-- " + getcomment() + "-->" + "\n" + \
        "<resources xmlns:android=\"http://schemas.android.com/apk/res/android\"" + "\n" + \
        "    xmlns:xliff=\"urn:oasis:names:tc:xliff:document:1.2\">" + "\n" + \
        "    <string name=\"sample\">\"sample\"</string>" + "\n" + \
        "</resources>" + "\n"
    
    f = open(r"Cafe" + getapplicationname() + "Test/cafe_tests/res/values/strings.xml",'w')
    f.writelines(template)
    f.close()

def casegen():
    template = \
        "// " + getcomment() + "\n" + \
        "package " + gettargetpackage() + ".tests;" + "\n" + \
        "\n" + \
        "import android.test.suitebuilder.annotation.LargeTest;" + "\n" + \
        "import android.test.suitebuilder.annotation.MediumTest;" + "\n" + \
        "import android.test.suitebuilder.annotation.SmallTest;" + "\n" + \
        "import com.baidu.cafe.CafeTestCase;" + "\n" + \
        "import com.baidu.cafe.annotation.None;" + "\n" + \
        "import com.baidu.cafe.annotation.BaiduAccountMust;" + "\n" + \
        "import com.baidu.cafe.annotation.NoBaiduAccountMust;" + "\n" + \
        "import com.baidu.cafe.annotation.Danger;" + "\n" + \
        "import android.util.Log;" + "\n" + \
        "import " + getactivityfullname() + ";" + "\n" + \
        "\n" + \
        "/*" + "\n" + \
        " * adb shell am instrument -w " + gettargetpackage() + ".tests/android.test.InstrumentationTestRunner" + "\n" + \
        " * */" + "\n" + \
        "\n" + \
        "public class " + getapplicationname() + "Test extends CafeTestCase<" + getactivity() + "> {" + "\n" + \
        "    public " + getapplicationname() + "Test()" + "\n" + \
        "    {" + "\n" + \
        "        super(\"" + gettargetpackage() + "\", " + getactivity() + ".class);" + "\n" + \
        "    }" + "\n" + \
        "\n" + \
        "    @Override" + "\n" + \
        "    protected void setUp() throws Exception {" + "\n" + \
        "        super.setUp();" + "\n" + \
        "    }" + "\n" + \
        "\n" + \
        "    @Override" + "\n" + \
        "    protected void tearDown() throws Exception {" + "\n" + \
        "        super.tearDown();" + "\n" + \
        "    }" + "\n" + \
        "\n" + \
        "    @SmallTest" + "\n" + \
        "    @None" + "\n" + \
        "    public void test_casename()" + "\n" + \
        "    {" + "\n" + \
        "        Log.i(\"TAG here\", \"log sample\");" + "\n" + \
        "    }" + "\n" + \
        "}" + "\n"
    
    f = open(r"Cafe" + getapplicationname() + "Test/cafe_tests/src/" + getcasepath() + "/" + getapplicationname() + "Test.java",'w')
    f.writelines(template)
    f.close()

def usage():
    print "CAFE casegen Tool version " + VERION
    print "Usage: python casegen.py [-h]<-p target package name><-a activity full name><-c LOCAL_CERTIFICATE>"
    print "Example: python caseGen.py -p com.android.contacts -a com.android.contacts.activities.DialtactsActivity -c shared"

def logm(line):
    if(debug):
        print line
        
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], 'hdp:a:c:')
    for opt,arg in opts:
        if opt in ('-h'):
            usage()
            sys.exit()
        if opt in ('-d'):
            debug = True
        if opt in ('-p'):
            targetpackage = arg
        if opt in ('-a'):
            activityfullname = arg
        if opt in ('-c'):
            certificate = arg

    try:        
        foldergen()
        manifestgen()
        mkgen()
        stringgen()        
        casegen()
    except Exception, data:
        raise Exception, "[casegen]exception:\n %s"%traceback.format_exc()
        sys.exit()
