## path inclusions
import sys
sys.path.append('Lib')

## libraries
from difflib import SequenceMatcher
import json
import time
import datetime
from JiphyLib import Jiphy

## functions
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def Get_IssueID(issueIDs, tcName):
    for index in range(0,len(issueIDs)):
        if tcName.lower() == issueIDs[index]['name'].lower():
            return json.dumps(issueIDs[index]['issueID']).strip('\"')
    for index in range(0,len(issueIDs)):
        if similar(tcName.lower(), issueIDs[index]['name'].lower()) >= 0.80:
            return json.dumps(issueIDs[index]['issueID']).strip('\"')        
    for index in range(0,len(issueIDs)):
        if tcName.lower() in issueIDs[index]['name'].lower():
            return json.dumps(issueIDs[index]['issueID']).strip('\"')
    for index in range(0,len(issueIDs)):
        if issueIDs[index]['name'].lower() in tcName.lower():
            return json.dumps(issueIDs[index]['issueID']).strip('\"')        
    return 0

if __name__ == "__main__":
	## constructor
	this = Jiphy("www.thisjira.com","thisuser","thispass")
	
	## constants
	projectName = "This Project"
	projectCode = "PROJECTCODE"
	versionName = "This Release"
		
	## processors
	projectID = this.Get_ProjectID(projectName)
	today = datetime.datetime.today().strftime('%d_%b_%y_%H%M%S')
	versionID = this.Get_VersionID(projectID, versionName)
	cycleName = "AutoTest_" + str(today)
	print "cycleName: " + cycleName	
	
	cycleID = this.Get_Test_CycleID(projectID, cycleName, versionID)
	issueIDs = this.Get_All_IssueID(projectCode)
	
	## main iterator
	outputjson = this.parse_xml('output.xml')
	for result in range(0,len(outputjson)):
		for testname in range(0,len(outputjson[result])):
			tcName = outputjson[result][testname]['name']
			status = outputjson[result][testname]['status']
			print tcName + ": " + status
			issueID = Get_IssueID(issueIDs, tcName)
			executionID = this.Create_ExecutionID(projectID, cycleID, issueID)
			tries = 3
			while True:
				try:
					this.Update_Test_Case_Execution_Status(executionID, status)
				except:
					if tries > 0:
						tries -= 1
						continue
					else:
						raise
				break
				
			