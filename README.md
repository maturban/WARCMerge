mergewarc
=========

Merging WARCs into a single WARC file


Dependencies
==================
* Python 2.7+ on Linux
* "warc" is a Python library to work with WARC files. It is used here for reading WARC records.
       It can be downloaded from https://github.com/internetarchive/warc
* "warctools" is used also to work with WARC files. One part of this library checks whether WARCs are valid!
       To download https://github.com/internetarchive/warctools

To run mergewarcs.py
=====================
```python
 $python mergewarcs.py <WARCs-path>
```

 This will merge all WARC files located in "WARCs-path" and store the result in ./merging-WARCs/. The program also will check whether or not the resulting WARCs are valid!
 
		
Example:
========

```python
 $python mergewarcs.py ./smallCollectionExample/

	Merging the following WARC files: 
	----------------------------------: 
	[ Yes ]./smallCollectionExample/world-cup-2014/20140707174317773.warc
	[ Yes ]./smallCollectionExample/about-warcs/20140707160258526.warc
	[ Yes ]./smallCollectionExample/about-warcs/20140707160041872.warc
	[ Yes ]./smallCollectionExample/world-cup-2014/20140707183044349.warc

	Validating the resulting WARC files: 
	----------------------------------: 
	- [ valid ]             ./merging-WARCs/679c1c08-060a-11e4-b7ca-782bcb0f034c/679eac98-060a-11e4-b7ca-782bcb0f034c.warc
```	

The following are links to the archived pages in the example above:
```	
	https://github.com/iipc/openwayback/wiki/How-OpenWayback-handles-revisit-records-in-WARC-files
	http://www.openplanetsfoundation.org/blogs/2014-03-24-arc-warc-migration-how-deal-de-duplicated-records
	http://econpapers.repec.org/paper/innwpaper/2014-17.htm
	http://articles.latimes.com/2013/mar/26/sports/la-sp-sn-us-mexico-soccer-game-updates-20130326	
```	
