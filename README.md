WARCMerge
=========

Merging WARC files into a single WARC file 


Dependencies
==================
* Tested on Linux Ubuntu 
* Python 2.7+ 
* Java to run Jwattools for validating WARC files
* "warc" is a Python library to work with WARC files. It is used here for reading WARC records.
       It can be downloaded from https://github.com/internetarchive/warc

To run WARCMerge.py
=====================
* Three options:

(1)
```python
 %python WARCMerge.py <input-directory> <output-directory>
```

 This will merge all WARC files found in <input-directory> and store the resulting output file(s) in <output-directory>.

(2)
```python
 %python WARCMerge.py <file1> <file2> <file3> ... <output-directory>
```

 This will merge all listed WARC files and store the resulting output file(s) in <output-directory>. 

(3) 
```python
 %python WARCMerge.py  -a <source-file> <dest-file>
```

 This will append the source WARC file <source-file> to the end of destination WARC file <dest-file>.
 
 In all cases, the program checks to see whether or not the resulting WARCs are valid! 

Example:
========

(1) Merging WARC files (found in <input-directory>) into a new WARC file:
```python
 %python WARCMerge.py ./collectionExample/ my-output-dir

	Merging the following WARC files: 
	----------------------------------: 
	[ Yes ]./collectionExample/world-cup/20140707174317773.warc
	[ Yes ]./collectionExample/warcs/20140707160258526.warc
	[ Yes ]./collectionExample/warcs/20140707160041872.warc
	[ Yes ]./collectionExample/world-cup/20140707183044349.warc

	Validating the resulting WARC files: 
	----------------------------------: 
	- [ valid ]     my-output-dir/WARCMerge20140806040712197944.warc
```	

(2) Appending WARC file to another WARC file:

maturban:~/GitHub/WARCMerge$ python WARCMerge.py -a ./testAppendCollection/source/20140707160258526.warc ./testAppendCollection/dest/20140707160041872.warc

         
		 
```python
	%python WARCMerge.py -a ./testAppend/source/20258526.warc ./testAppend/dest/20141872.warc

	The resulting (./testAppend/dest/20141872.warc) is valid WARC file
```

(4) Giving incorrect arguments, the following message will be shown: 
```python
  %python WARCMerge.py -n 20160041872.warc new-dir

	usage: WARCMerge [ -a <source-file> <dest-file> ]
					 [ <input-directory> <output-directory> ]
					 [ <file1 file2 file3 ... > <output-directory> ] 
```


The following are links to the archived pages in the example above:
```	
	https://github.com/iipc/openwayback/wiki/How-OpenWayback-handles-revisit-records-in-WARC-files
	http://www.openplanetsfoundation.org/blogs/2014-03-24-arc-warc-migration-how-deal-de-duplicated-records
	http://econpapers.repec.org/paper/innwpaper/2014-17.htm
	http://articles.latimes.com/2013/mar/26/sports/la-sp-sn-us-mexico-soccer-game-updates-20130326	
```	
