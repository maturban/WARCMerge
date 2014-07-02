#!/usr/bin/env python

import uuid
import sys 
import os  

# from https://github.com/internetarchive/warctools/  (check if .warc is valid)
from hanzo.warctools  import WarcRecord, expand_files
#from : http://warc.readthedocs.org/en/latest/         (read WARC records)
import warc 

MaxWarcSize = 500.0 # in MB

# return a list of all WARC files in the given directory
# from http://stackoverflow.com/questions/3964681/find-all-files-in-# directory-with-extension-txt-with-python
def list_files(startPath):
	l = []
	for root, dirs, files in os.walk(startPath):
		for file in files:
			if file.endswith(".warc"):
				l.append(os.path.join(root, file))
	return l

# Create "worcinfo" record header and content
def createWarcInfoReacord(filename):
	H = warc.WARCHeader({"WARC-Type": "warcinfo", \
                     "WARC-Filename" : filename}, \
					 defaults=True)
	Content = "software: WARMerge/1.0" + "\r\n" \
      + "format: WARC File Format 1.0" + "\r\n" \
	  + "description: "+" Merging WARC files into a single one " + "\r\n" + \
	  "robots: ignore" + "\r\n"	
	R = warc.WARCRecord(H, Content)
	return R

# Sort file list by size
# from : http://stackoverflow.com/questions/20252669/get-files-from-directory-argument-sorting-by-size
def sortFiles(fileList):
	for i in xrange(len(fileList)):
		fileList[i] = (fileList[i], os.path.getsize(fileList[i]))
	fileList.sort(key=lambda filename: filename[1], reverse=False)
	
	for i in xrange(len(fileList)):
		fileList[i] = fileList[i][0]
	return fileList	

# check if .warc is valid
# from https://github.com/internetarchive/warctools/
def isWarcValid(warcfile):

    correct=True
    fh=None
    errorMSG = ''
    try:
        fh = WarcRecord.open_archive(warcfile, gzip="auto")

        for (offset, record, errors) in fh.read_records(limit=None):
            if errors:
                errorMSG += str("warc errors at %s:%d"%(warcfile, offset))
                errorMSG += str(errors)
                correct=False

                break
            elif record is not None and record.validate(): # ugh name, returns errorsa
                errorMSG += str("warc errors at %s:%d"%(warcfile, offset))
                errorMSG += str(record.validate())
                correct=False
                break
                
    except Exception as e:
        errorMSG += str("Exception: %s"%(str(e)))
        correct=False
    finally:
        if fh: fh.close()
    
    if correct:
        return (0, errorMSG)
    else:
        return (-1, errorMSG) # failure code
		

		                        ############################################
		                        ############################################								

if len(sys.argv) != 2:
	print '\n  Usage: $python mergewarcs.py <path-to-warc-files> \n'
	sys.exit(0)

if os.path.isdir(sys.argv[1]) == False:
	print('\n  No such directory: '+sys.argv[1]+' \n')
	sys.exit(0)

dirTree = list_files(sys.argv[1])

if len(dirTree) == 0:
	print('\n  No WARCs found in the directory: '+sys.argv[1]+' \n')
	sys.exit(0)


outputPath = "./merging-WARCs/"
if not os.path.exists(outputPath):
    os.makedirs(outputPath)
# create a new folder 	
outputPath = outputPath + str(uuid.uuid1())
os.makedirs(outputPath)
	
# generate new warc file name
newFile = str(uuid.uuid1())+'.warc'
newFileFullPath = outputPath+'/'+newFile
filePtr = warc.open(newFileFullPath, "w")
flag = 0

forConvertToMB = float(2<<19)

outputFileSize = os.path.getsize(newFileFullPath) / forConvertToMB

# Sorting files by sizes
sortFiles(dirTree)

print '\n'
print 'Merging the following WARC files: ' 
print '----------------------------------: ' 

for warcFile in dirTree:
	outputFileSize = os.path.getsize(newFileFullPath) / forConvertToMB
	fileSize = os.path.getsize(warcFile) / forConvertToMB
	if ((fileSize + outputFileSize) > MaxWarcSize) and (outputFileSize != 0) :
		filePtr.close()
		# generate new warc file name if current file exceeds WARC file size limit
		newFile = str(uuid.uuid1())+'.warc'
		newFileFullPath = outputPath+'/'+newFile
		filePtr = warc.open(newFileFullPath, "w")
		flag = 0
		
	f = warc.WARCFile(warcFile, "rb")
	try:
		for record in f:
			if flag == 0:
				R = createWarcInfoReacord(newFile)
				filePtr.write_record(R)
				flag = 1
			R = warc.WARCRecord(payload=record.payload.read(), headers=record.header)
			filePtr.write_record(R)
		print '[ Yes ]' + warcFile	
	except Exception as e:
		#print("Exceptionq: %s"%(str(e)))
		print '[ No ]' + warcFile
		pass
filePtr.close()
outputFileSize = os.path.getsize(newFileFullPath) / forConvertToMB
if outputFileSize == 0:
	os.remove(newFileFullPath)

print '\nValidating the resulting WARC files: ' 
print '----------------------------------: ' 

dirTreeCheckWARCs = list_files(outputPath)

for filePath in dirTreeCheckWARCs:
	(correct,msg) = isWarcValid(filePath)
	if correct == 0:
		print '- [ valid ]\t\t'+filePath+''
	else:
		print '- [ Invalid ]\t\t'+filePath+''
		print msg
		print '- ----------------------------'
print	

'''
	record['WARC-Type']
'''
