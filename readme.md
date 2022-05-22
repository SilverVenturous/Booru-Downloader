## SilverVenturous Booru Downloader

This tool can be used to download files from Gelbooru. I created this tool for personal use according to my very specific preferences. I created this tool because I wanted some features that Bionus' booru grabber does not have:
* When downloading files using the Bionis' grabber, it uses much more wi-fi data than the total file size of the files it downloaded. This tool does not make that mistake.
* Tag implication list in implications.txt, because the Gelbooru developers still have not created an interface for users to submit their own.
* The following customizations on the file name that it will generate:
	* Automatically rename tags (according to preferences in rename.txt).
	* Automatically change the tag type to a different one or ignore the tag (according to preferences in reclassify.txt).
	* prefered order for general tags in tag_order.txt
* This tool prints all metadata (tags, md5, source, rating, site name, score) into the image's user-comment EXIF metadata tag. This is only done for JPG and PNG files. I implemented this so that I can search for tags windows.
* This tool prints all the tags into the XP-tags metadaa (only for JPG files).

How to use:
* Install python
* Install a few things using using the "pip install" command in the command line. I don't recall what exactly you need to install but the command prompt will inform you which packages you need to install when you try to run the tool.
* put the links to the gelbooru pages you want to download (which have a format like this: https://gelbooru.com/index.php?page=post&s=view&id=7222955) in the gelbooru_image_page_links.txt file, one on each line
* in the folder where the python files are located, enter "python main.py" on the command line
* the files will be downloaded in that folder
* line 399 in main.py can be edited to change the maximum file size

Additionally, two tools are included to search the files you have downloaded:
* generate_metadata_list.py can be used to generate a database of the files you have downloaded using the downloader. You have to provide it the list of files it needs to scan. Put absolute reference file paths in file_list.txt
* search_metadata_file.py is a template for searching through the database. Basic python know-how is required to edit this file according to what you are trying to accomplish. The outputs are printed in search_results.txt

To-do:
* Implement the ability to download from sankakucomplex.
* Create a blacklist for tags to add to the file name when the rating is safe. I don't need to add tags like "breasts" and "ass" to the names of files that are safe.

I cannot be arsed to do stuff like make this tool more customizable or add a user interface. Sometimes I wonder why I go to such lengths to organize my collection of hentai pictures.

V1.1 changes:
* rule34.xxx links are now also accepted
* The database generator and search tool was added.