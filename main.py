import requests
import os
from PIL import Image
import iptcinfo3, os, sys, random, string
from os.path import exists

def download_file(url_name,filename):
    url = url_name
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    
def webpage_to_string(url_name):
    url = url_name
    r = requests.get(url, allow_redirects=True)
    return r.text

def rename_gelbooru_file_using_source(file_name,source):
    
    #get tags and types from source and put in arrays
    tags = ['foo'] * 1000
    tag_types = ['foo'] * 1000
    tag_amount = 0
    source_contains_tags_not_added_to_arrays = True
    index_of_tag_area = 0
    while source_contains_tags_not_added_to_arrays:
        try:
            index_of_tag_area = source.index("class=\"tag-type",index_of_tag_area+1)
            tag_types[tag_amount] = source[index_of_tag_area+16:source.index("\">",index_of_tag_area+17)]
            index_of_tag_name_start = source.index("\">",index_of_tag_area+1)
            index_of_tag_name_start = source.index("\">",index_of_tag_name_start+1)
            index_of_tag_name_start = source.index("\">",index_of_tag_name_start+1)
            index_of_tag_name_start = source.index("\">",index_of_tag_name_start+1)
            tags[tag_amount] = source[index_of_tag_name_start+2:source.index("</a>",index_of_tag_name_start)]
            tag_amount += 1
        except:
            source_contains_tags_not_added_to_arrays = False
    print("Number of tags: " + str(tag_amount))
    for i in range(tag_amount):
        tags[i] = tags[i].replace(" ","_")
        tags[i] = tags[i].replace("/","_")
        tags[i] = tags[i].replace("\\","_")
        tags[i] = tags[i].replace(":","_")
        tags[i] = tags[i].replace("?","_")
        tags[i] = tags[i].replace("|","_")
        tags[i] = tags[i].replace("<","_")
        tags[i] = tags[i].replace(">","_")
        tags[i] = tags[i].replace("*","_")
        tags[i] = tags[i].replace("\"","_")
        tags[i] = tags[i].replace("&#039;","'")
        tags[i] = tags[i].replace("&auml;","ä")
        tags[i] = tags[i].replace("&amp;","&")
        if tag_types[i] == "metadata":
            tag_types[i] = "general"
        #print(tags[i] + " " + tag_types[i])
    
    #Acquire other necessary info from webpage
    rating = "undetermined"
    if "Rating: Explicit" in source:
        rating = "explicit"
    if "Rating: Questionable" in source:
        rating = "questionable"
    if "Rating: Safe" in source:
        rating = "safe"
    id_start = source.index("Id: ")
    id_end = source.index("<", id_start)
    id = source[id_start+4:id_end]
    extension = file_name[file_name.index("."):len(file_name)+1]
    md5 = "foo"
    if "data-md5=" not in source:
        md5 = file_name[0:file_name.index('.')]
    else:
        md5 = source.index("data-md5=") + 10
        md5 = source[md5:source.index("\"",md5)]
    Gelbooru_source = "none"
    if "Source: <a hr" in source:
        Gelbooru_source = source.index("Source: <a hr")+17
        Gelbooru_source = source[Gelbooru_source:source.index("\"",Gelbooru_source)]
    Gelbooru_score = source.index("Score: <s")
    Gelbooru_score = source.index(">",Gelbooru_score)+1
    Gelbooru_score = source[Gelbooru_score:source.index("<",Gelbooru_score)]
    is_sampled = False
    if "sample" in file_name:
        is_sampled = True
    
    #read in implication list
    file4 = open('implications.txt', 'r')
    lines = file4.readlines()
    implication_source = ['foo'] * 1000
    implication_target = ['foo'] * 1000
    implication_target_type = ['foo'] * 1000
    implication_count = 0
    for line in lines:
        divider_loc = line.index(" ")
        divider_loc2 = line.index(" ",divider_loc+1)
        implication_source[implication_count] = line[0:divider_loc]
        implication_target[implication_count] = line[divider_loc+1:divider_loc2]
        implication_target_type[implication_count] = line[divider_loc2+1:len(line)-1]
        implication_count += 1
        
    #apply implications
    for x in range(implication_count):
        if implication_source[x] in tags:
            if implication_target[x] not in tags:
                tags[tag_amount] = implication_target[x]
                tag_types[tag_amount] = implication_target_type[x]
                tag_amount += 1
        
    
    #Can be used to rename Gelbooru images that contains the id
    '''
    file_name = id + extension
    file_name = file_name.replace("jpeg","jpg")
    if not exists(file_name):
        file_name = file_name.replace("jpg","png")
        extension = '.png'
    if not exists(file_name):
        file_name = file_name.replace("png","jpg")
        extension = '.jpg'
    if not exists(file_name):
        file_name = file_name.replace("webm","mp4")
        extension = '.mp4'
    if not exists(file_name):
        file_name = file_name.replace("mp4","webm")
        extension = '.webm'
    if not exists(file_name):
        file_name = file_name.replace("gif","webm")
        extension = '.webm'
    if not exists(file_name):
        print("Warning: File was still not found despite the existing countermeasures. Possible cause is that it is a unanimated sample of an animated file.")
        return
    '''
    
    #Add EXIF user comment
    if file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png"):
        im = Image.open(file_name)
        exif = im.getexif()
        exif_comment = "COMMENT EXIF_COMMENT_START   EXIF comment generated by SilverVenturous ___ Image from Gelbooru"
        exif_comment += " id:" + id + " "
        if rating == "safe":
            exif_comment += "   rating:safe"
        if rating == "questionable":
            exif_comment += "   rating:questionable"
        if rating == "explicit":
            exif_comment += "   rating:explicit"
        exif_comment += "   md5:" + md5 + (" (of the unsampled file) ")
        if is_sampled:
            exif_comment += " sample:yes"
        else:
            exif_comment += " sample:no"
        exif_comment += "   Gelbooru-source:" + Gelbooru_source
        exif_comment += "   Gelbooru-score:" + Gelbooru_score
        exif_comment += "   Copyrights:"
        for i in range(tag_amount):
            if tag_types[i] == "copyright":
                exif_comment += " " + tags[i]
        exif_comment += "   Characters:"
        for i in range(tag_amount):
            if tag_types[i] == "character":
                exif_comment += " " + tags[i]
        exif_comment += "   Artists:"
        for i in range(tag_amount):
            if tag_types[i] == "artist":
                exif_comment += " " + tags[i]
        exif_comment += "   General tags:"
        for i in range(tag_amount):
            if tag_types[i] == "general":
                exif_comment += " " + tags[i]
        exif_comment += "   EXIF_COMMENT_END"
        exif[0x9286] = exif_comment
        im.save(file_name, exif=exif)
        im.close()
        
    #Add XP tags if it is a JPG file
    if file_name.endswith(".jpg") or file_name.endswith(".jpeg"):
        # Path to the file, open a IPTCInfo object
        path = os.path.join(sys.path[0], file_name)
        info = iptcinfo3.IPTCInfo(path)
        # Show the keywords
        #print(info['keywords'])
        # Add a keyword and save
        xp_keywords = []
        for x in range(tag_amount):
            xp_keywords.append(tags[x])
        info['keywords'] = xp_keywords
        #Note: It appears the XP author tag cannot be edited using the iptcinfo3 package
        info.save()
        # Remove the weird ghost file created after saving
        os.remove(path + '~')
    
    #retrieve the tag reclassify list, tag reorder list, and rename list
    file1 = open('reclassify_tags.txt', 'r')
    lines = file1.readlines()
    reclassify_names = ['foo'] * 1000
    reclassify_types = ['foo'] * 1000
    reclassify_count = 0
    for line in lines:
        divider_loc = line.index(" ")
        reclassify_names[reclassify_count] = line[0:divider_loc]
        reclassify_types[reclassify_count] = line[divider_loc+1:len(line)-1]
        #print(reclassify_names[reclassify_count] + " " + reclassify_types[reclassify_count])
        reclassify_count += 1
    file2 = open('rename_tags.txt', 'r')
    lines = file2.readlines()
    rename_list_original = ['foo'] * 1000
    rename_list_target = ['foo'] * 1000
    rename_list_type = ['foo'] * 1000
    rename_list_count = 0
    for line in lines:
        divider_loc = line.index(" ")
        rename_list_original[rename_list_count] = line[0:divider_loc]
        #print(rename_list_original[rename_list_count])
        divider_loc2 = line.index(" ",divider_loc+1)
        rename_list_target[rename_list_count] = line[divider_loc+1:divider_loc2]
        rename_list_type[rename_list_count] = line[divider_loc2+1:len(line)-1]
        rename_list_count += 1
    file3 = open('tags_order.txt', 'r')
    lines = file3.readlines()
    xxx_tag_order = ['foo'] * 1000
    xxx_tag_order_count = 0
    for line in lines:
        xxx_tag_order[xxx_tag_order_count] = line[0:len(line)-1]
        #print(xxx_tag_order[xxx_tag_order_count] + "|")
        xxx_tag_order_count += 1
        
    #use the instrucions from reclassify_tags.txt to reclassify tags
    for x in range(tag_amount):
        for y in range(reclassify_count):
            if reclassify_names[y].endswith("*"):
                if tags[x].startswith(reclassify_names[y][0:len(reclassify_names[y])-1]):
                    tag_types[x] = reclassify_types[y]
            else:
                if tags[x] == reclassify_names[y]:
                    tag_types[x] = reclassify_types[y]
                
    #use the instrucions from rename_tags.txt to rename tags
    for x in range(tag_amount):
        for y in range(rename_list_count):
            if tag_types[x] == rename_list_type[y]:
                #print(rename_list_original[y][1:len(rename_list_original[y])-1])
                if rename_list_target[y] == "REMOVE":
                    if rename_list_original[y].startswith("*") and tags[x].endswith(rename_list_original[y][1:len(rename_list_original[y])]):
                        tags[x] = tags[x][0:len(tags[x])-len(rename_list_original[y])+1]
                    #I did not bother writing code for cases where the beginning is removed
                elif not rename_list_original[y].startswith("*") and not rename_list_original[y].endswith("*"):
                    if tags[x] == rename_list_original[y]:
                        tags[x] = rename_list_target[y]
                elif rename_list_original[y].startswith("*") and not rename_list_original[y].endswith("*"):
                    if tags[x].endswith( rename_list_original[y][1:len(rename_list_original[y])] ):
                        tags[x] = tags[x][0:len(tags[x])-len(rename_list_original[y])+1] + rename_list_target[y]
                elif not rename_list_original[y].startswith("*") and rename_list_original[y].endswith("*"):
                    if tags[x].startswith(rename_list_original[y][0:len(rename_list_original[y])-1]):
                        tags[x] = rename_list_target[y] + tags[x][len(rename_list_original[y])-1:len(tags[x])]
                elif rename_list_original[y].startswith("*") and rename_list_original[y].endswith("*"):
                    tags[x] = tags[x].replace(rename_list_original[y][1:len(rename_list_original[y])-1],rename_list_target[y])
    
    for x in range(tag_amount):
        #print( tags[x] + " " + tag_types[x] )
        foo = 0
    
    #eliminate duplicates
    for x in range(tag_amount):
        for y in range(tag_amount):
            if x != y and tag_types[x] != "duplicate":
                if tags[x] == tags[y] and tag_types[x] == tag_types[y]:
                    tag_types[y] = "duplicate"
                    
    #alphebetical sort
    for x in range(tag_amount):
        for y in range(tag_amount-1):
            if tags[y] > tags[y+1]:
                holder1 = tags[y]
                holder1_type = tag_types[y]
                tags[y] = tags[y+1]
                tag_types[y] = tag_types[y+1]
                tags[y+1] = holder1
                tag_types[y+1] = holder1_type
    
    #assemble new file name 
    new_name = ""
    if rating == "explicit" or rating == "questionable":
        new_name = "Explicit -"
    number_of_copyrights = 0
    for x in range(tag_amount):
        if tag_types[x] == "copyright":
            number_of_copyrights += 1
    if number_of_copyrights <= 4:
        for x in range(tag_amount):
            if tag_types[x] == "copyright" and len(new_name) < 140:
                if len(new_name) != 0:
                    new_name += " "
                new_name += tags[x]
    else:
        if rating == "explicit" or rating == "questionable": 
            new_name += " many_copyrights"
        else:
            new_name += "many_copyrights"
    new_name += " -"
    number_of_characters = 0
    for x in range(tag_amount):
        if tag_types[x] == "character":
            number_of_characters += 1
    if number_of_characters <= 6:
        for x in range(tag_amount):
            if tag_types[x] == "character" and len(new_name) < 140:
                new_name += " " + tags[x]
    else:
        new_name += " many_characters"
    new_name += " -"
    for x in range(tag_amount):
        if tag_types[x] == "artist" and (len(new_name) + len(tags[x])) < 160:
            new_name += " " + tags[x]
    new_name += " -"
    for y in range(xxx_tag_order_count-1): #add xxx ordered tags first
        for x in range(tag_amount):
            #print(tags[x] + " " + xxx_tag_order[y])
            if tag_types[x] == "general" and tags[x] == xxx_tag_order[y] and len(new_name) < 140:
                new_name += " " + tags[x]
    for x in range(tag_amount): #add the rest of the general tags
        if tag_types[x] == "general" and len(new_name) < 140:
            not_added_yet = True
            y = 0
            while not_added_yet and y < xxx_tag_order_count:
                if xxx_tag_order[y] == tags[x]:
                    not_added_yet = False
                y += 1
            if not_added_yet and tags[x] != "censor":
                new_name += " " + tags[x]
    for x in range(tag_amount):
        if tags[x] == "censor":
            new_name += " " + tags[x]
    new_name += " - Gelbooru-" + id
    if is_sampled:
        new_name += "s"
    if extension == ".jpeg":
        extension = ".jpg"
    new_name += extension
    print(new_name)
    
    os.rename(file_name,new_name)

    
def download_image_from_gelbooru_webpage(url_name):
    print("downloading image from " + url_name)
    webpage_string = webpage_to_string(url_name)
    original_image_url_start_index = "foo";
    try:
        original_image_url_start_index = webpage_string.index("meta property=\"og:image\"")
    except:
        print("Original image URL not detected. Canceled.")
        return 1
    #print(original_image_url_start_index)
    original_image_url_end_index = webpage_string.index("\"", original_image_url_start_index+34)
    #print(original_image_url_end_index)
    original_image_url = webpage_string[(original_image_url_start_index+34):original_image_url_end_index]
    print("Original file: " + original_image_url)
    is_big_animated_file = False
    file_name = "foo"
    download_url = "foo"
    refrained_from_downloading = False
    
    if original_image_url.endswith(".webm") or original_image_url.endswith(".mp4") or original_image_url.endswith(".gif"):
        file_size = requests.head(original_image_url).headers.get('content-length', None)
        #print(file_size)
        #maximum filesize of animated file
        if int(file_size) > 5000000:
            print("Did not download: Animated with a file size of " + file_size)
            f = open("big_animated_images_found.txt", "a")
            f.write(url_name)
            f.close()
            is_big_animated_file = True
            refrained_from_downloading = True
    if not is_big_animated_file:
        download_url = original_image_url
        file_name = original_image_url[40:len(original_image_url)]
        if "Click here to expand image." in webpage_string:
            if original_image_url.endswith(".jpg") or original_image_url.endswith(".jpeg") or original_image_url.endswith(".png"):
                download_url = "https://img3.gelbooru.com//samples/" + original_image_url[34:39] + "/sample_" + original_image_url[40:72] + ".jpg"
                file_name = "sample_" + original_image_url[40:72] + ".jpg"
        #comment out the following line if you want to rename existing images
        download_file(download_url,file_name)
    if not refrained_from_downloading:
        print("Downloaded " + download_url)
        rename_gelbooru_file_using_source(file_name,webpage_string)
    return 1

def rename_existing_gelbooru_image():
    #load list from file, do generate_gelbooru_filename_from_url, rename
    return 1
    
def download_all_on_gelbooru_search_page(page_url):
    webpage_string = webpage_to_string(page_url)
    undownloaded_images_left_on_page = True
    id_index_start = 0
    while undownloaded_images_left_on_page:
        try:
            id_index_start = webpage_string.index("<a id=\"",id_index_start)+8
            id_endex_end = webpage_string.index("\"",id_index_start)
            id = webpage_string[id_index_start:id_endex_end]
            pic_page_url = "https://gelbooru.com/index.php?page=post&s=view&id=" + str(id)
            print("Initiating download and rename from: |" + pic_page_url + "|")
            download_image_from_gelbooru_webpage(pic_page_url)
        except:
            undownloaded_images_left_on_page = False
  
#download_image_from_gelbooru_webpage("https://gelbooru.com/index.php?page=post&s=view&id=6982751")
#download_all_on_gelbooru_search_page("https://gelbooru.com/index.php?page=post&s=list&tags=all")

file = open('gelbooru_image_page_links.txt', 'r')
lines = file.readlines()
for line in lines:
    download_image_from_gelbooru_webpage(line)