#!/usr/bin/env python
# Author: Mohamed Aturban, Old Dominion University, CS department, WS-DL Group
import datetime
import sys 
import os
  
import warc # from : http://warc.readthedocs.org/en/latest/         (read WARC records)

MaxWarcSize = 500.0 # in MB
forConvertToMB = float(2<<19)

# return a list of all WARC files in the given directory
# from http://stackoverflow.com/questions/3964681/find-all-files-in-# directory-with-extension-txt-with-python
def list_files(startPath):
	l = []
	for root, dirs, files in os.walk(startPath):
		for file in files:
			if file.endswith(".warc"):
				l.append(os.path.join(root, file))
	return l

def timeStampedFilename(fn):
	tstr = fn+''+str(datetime.datetime.utcnow())
	tstr = tstr.replace(':', '').replace('-', '').replace('.', '').replace(' ', '')
	return tstr
	
# Create "worcinfo" record header and content
def createWarcInfoReacord(filename):
	H = warc.WARCHeader({"WARC-Type": "warcinfo", \
                     "WARC-Filename" : filename}, \
					 defaults=True)
	Content = "software: WARCMerge/1.0" + "\r\n" \
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

# check if WARC file is valid
# from https://bitbucket.org/nclarkekb/jwat-tools/downloads
def isWarcValid(warcfile):
	flagV = 0 # valid
	str = "java -Xms256m -Xmx1048m -XX:PermSize=64M -XX:MaxPermSize=256M -jar target/jwat-tools-*-jar-with-dependencies.jar -t "+warcfile	
	res = os.popen(str).read().split()
	try:
		resIndex = res.index('Errors:')
		if(res[resIndex + 1] == '0'):
			flagV = 0 # WARC valid
		else:
			flagV = -1 # WARC invalid
	except Exception as e:
		flagV = -2 # not working
		print ("Warning: WARC validator (jwattools.sh) cannot be run")
		pass
	return flagV	

		                        ############################################								

# Merging to an existing WARC file
if len(sys.argv) == 3:
	Sfile = sys.argv[1]
	Dfile = sys.argv[2]
	if not os.path.isfile(Sfile):
		print('\n  No such file: '+Sfile+' \n')
		sys.exit(0)	
	if not os.path.isfile(Dfile):
		print('\n  No such file: '+Dfile+' \n')
		sys.exit(0)
	if (not Sfile.endswith(".warc")):
		print ("\n Source file ("+Sfile+") is not WARC file")
		sys.exit(0)
	if (not Dfile.endswith(".warc")):
		print ("\n Dest file ("+Dfile+") is not WARC file")
		sys.exit(0)
	correct = isWarcValid(Sfile)
	if correct == -2:
		print ("Warning: WARC validator (jwattools.sh) cannot be run")
	else:
		if correct != 0:
			print ("\n Source file ("+Sfile+") is not valid WARC file")
			sys.exit(0)		
	correct = isWarcValid(Dfile)
	if correct == -2:
		print ("Warning: WARC validator (jwattools.sh) cannot be run")
	else:
		if correct != 0:
			print ("\n Dest file ("+Dfile+") is not valid WARC file")
			sys.exit(0)
	if (( (os.path.getsize(Sfile)/ forConvertToMB) + (os.path.getsize(Dfile)/ forConvertToMB)) > MaxWarcSize):
		print ("\n Connot merge <Souce> file with <Dest> file: [Maximum <Dest> WARC file is "+str(MaxWarcSize)+" MB].")
		sys.exit(0)
	try:
		filePtr = warc.open(Dfile, "a")
	except Exception as e:
		print 'Error in writing in:' + Dfile
		sys.exit(0)
	try:
		f = warc.WARCFile(Sfile, "rb")
		for record in f:
			if ("warcinfo" in record['WARC-Type']):
				New_Payload = record.payload.read().strip()+ "\r\n" +"WARC-appended-by-WARCMerge: "+datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ') + "\r\n"
				record['Content-Length'] = str(len(New_Payload))
				R = warc.WARCRecord(record.header , New_Payload, defaults=False)
			else:	
				R = warc.WARCRecord(payload=record.payload.read(), headers=record.header, defaults=False)
			filePtr.write_record(R)
	except Exception as e:
		print 'Error in reading:' + Sfile
		sys.exit(0)
	f.close()		
	filePtr.close()
	correct = isWarcValid(Dfile)
	if correct ==0:
		print ("\n\t The resulting Dest: ("+Dfile+") is valid WARC file")
	if correct != 0:
		print ("\n The resulting Dest file ("+Dfile+") is not valid WARC file")
		sys.exit(0)			
else:	
	# Merging to new WARC file(s)
	if len(sys.argv) == 2:
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
		outputPath = outputPath + timeStampedFilename("WARCMerge")
		os.makedirs(outputPath)
	
		# generate new warc file name
		newFile = timeStampedFilename("WARCMerge")+'.warc'
		newFileFullPath = outputPath+'/'+newFile
		filePtr = warc.open(newFileFullPath, "w")
		flag = 0

		outputFileSize = os.path.getsize(newFileFullPath) / forConvertToMB

		# Sorting files by sizes
		sortFiles(dirTree)

		print 
		print 'Merging the following WARC files: ' 
		print '----------------------------------: ' 

		for warcFile in dirTree:
			outputFileSize = os.path.getsize(newFileFullPath) / forConvertToMB
			fileSize = os.path.getsize(warcFile) / forConvertToMB
			if ((fileSize + outputFileSize) > MaxWarcSize) and (outputFileSize != 0) :
				filePtr.close()
				# generate new warc file name if current file exceeds WARC file size limit
				newFile = timeStampedFilename("WARCMerge")+'.warc'
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
					if ("warcinfo" in record['WARC-Type']):
						New_Payload = record.payload.read().strip()+ "\r\n" +"WARC-appended-by-WARCMerge: "+datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ') + "\r\n"
						record['Content-Length'] = str(len(New_Payload))
						R = warc.WARCRecord(record.header , New_Payload, defaults=False)
					else:	
						R = warc.WARCRecord(payload=record.payload.read(), headers=record.header, defaults=False)
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
			correct = isWarcValid(filePath)
			if correct == -2:
				break
			if correct == 0:
				print '- [ valid ]\t'+filePath+''
			else:
				if correct == -1:
					print '- [ Invalid ]\t'+filePath+''
				else:
					print '- [ WARC validator (jwattools.sh) cannot be run ]\t\t'+filePath+''
		print	
	else:	
		print '\n  Usage:   %python WARCMerge.py <Path-to-directory-of-WARC-files> \n          Or'
		print '           %python WARCMerge.py <Path-to-SOURCE-warc-file> <Path-to-DEST-WARC-file> \n'
		sys.exit(0)
	
if os.path.isfile("./v.out"):
	os.remove("./v.out")
if os.path.isfile("./e.out"):
	os.remove("./e.out")
'''
	record['WARC-Type']
'''
