
--------- ReadMe:

1. About ----

* Python Runtime and Package Installation
First of it, it is assumed that python3 and pip3 are installed. And
cvdastwrapper package is installed by pip3. The python3 command can sometimes
just be "python" if your default python installation is version 3 or above.
Please run "python --version" to find out. If you are running python 3 or above
by default, please simply substitute the "python3" commands in examples provided
in the remainder of this document.

Ensure cvdast is available and up-to date, please run:
   pip3 install -U cvdast
   
To ensure cvdastwrapper is up-to-date, please run:
   pip3 install -U cvdastwrapper

* Test Directory
Create a Test directory where the spec files and config file can be placed. 
Please feel free to rename the test directory. The subdirectory structure is
important for the test run. All files generated will be put under the test directory.

* Config:
The file cv_config.yaml is used to specify the authentication API endpoint and
the credentials to get the access token which is used to fuzz other APIs.
 
There will be information such as the URL of your test application (API endpoint),
the list of the fuzz attacks to try etc. in the cv_config.yaml which can be customized
as per user environment. The same file contains all of the custom variables one needs
to change. Current values are provided as examples. 

In the Test directory create a folder called 'specs' and place all the APIspecs (JSON
version only) here.
 
After the test is complete (details in sections below), the summary-<timestamp>.html
file will contain pointers to all the test results. In addition, a file called
fordev-apis.csv is generated. This is a highlevel summary for consumption of a
dev team. It highlight just the API endpoints that seem to "fail" the test, ie.
responding positively instead of rejecting the fuzz calls. Please feel free to
import such CSV report to a spreadsheet. 

The test results are stored in
    results
    results/perapi
    results/perattack

Test can run for a long time, so one can adjust the spec and the
collection of attacks in cv_config.yaml to stage each run. Test results
of different test will not over-write each other. You can regenerate
test report after the test run.

2. Generate fuzzing test for all the specs ----

With a given cvdast version and a set of specs, you need to only run
this once.

cvdastwrapper --generate-tests 

A successfully run fuzzallspecs will generate as output a list of spec
title names (taken from the spec's title) that can be used to update runall.py
list for test control (later 4. Control test)

3. Running Tests -----------

To start the tests execute below command: 

 cvdastwrapper test

Above cvdastwrapper also takes a "regen" argument. Regen will tells it not to
run the long test, but just run the cloudVectorDAST.generate_fuzz_report to
again generate the report (it copies the saved report.json from results
directory)

It creates a summary-<timestamp>.html in the test. It contains tables allowing convenient
access to all the reports

Results are saved in a directory called results

  results
    results/perapi
    results/perattack

After the test is finished you can find subdirectories with the Spec names under
each of these results directories.
There are .html files that are the report html pointed to by the summary.

Under the perapi directory there are files that are named after the API
name (chopped from the test directory long "for_fuzzing.py" name). The
report.json of the test run is saved with <apiname>-report.json