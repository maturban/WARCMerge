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
* Two options:
(1)
```python
 %python WARCMerge.py <WARCs-path>
```

 This will merge all WARC files located in "WARCs-path" and store the result in new directory inside ./merging-WARCs/. The program also will check whether or not the resulting WARCs are valid!

(2) 
```python
 %python WARCMerge.py  <Source-WARC-file-path>  <Dest-WARC-file-path>
```

 This will append source WARC file to the end of dest. WARC file. Also, here the resulting dest. file will be checked to see if it is valid WARC file or not!

 
		
Example:
========

(1) Merging WARC files into a new WARC file:
```python
 %python WARCMerge.py ./smallCollectionExample/

	Merging the following WARC files: 
	----------------------------------: 
	[ Yes ]./smallCollectionExample/world-cup-2014/20140707174317773.warc
	[ Yes ]./smallCollectionExample/about-warcs/20140707160258526.warc
	[ Yes ]./smallCollectionExample/about-warcs/20140707160041872.warc
	[ Yes ]./smallCollectionExample/world-cup-2014/20140707183044349.warc

	Validating the resulting WARC files: 
	----------------------------------: 
	- [ valid ]     ./merging-WARCs/WARCMerge20140713113532151317/WARCMerge20140713113532152003.warc
```	

(2) Appending WARC file to another WARC file:
```python
	%python WARCMerge.py ./testAppendCollection/source/20140707160258526.warc 
	                     ./testAppendCollection/dest/20140707160041872.warc

	The resulting Dest: (./TestAppend/dest/20140707160041872.warc) is valid WARC file
```



The following are links to the archived pages in the example above:
```	
	https://github.com/iipc/openwayback/wiki/How-OpenWayback-handles-revisit-records-in-WARC-files
	http://www.openplanetsfoundation.org/blogs/2014-03-24-arc-warc-migration-how-deal-de-duplicated-records
	http://econpapers.repec.org/paper/innwpaper/2014-17.htm
	http://articles.latimes.com/2013/mar/26/sports/la-sp-sn-us-mexico-soccer-game-updates-20130326	
```	
