file_filelist = open('file_list.txt', 'r', encoding="utf-8")
filelist_lines = file_filelist.readlines()
file_exiflist = open("exif_comment_list.txt", "r")
exiflist_lines = file_exiflist.readlines()
file_metalist = open("booru_files_metadata.csv", "w")

#sort filelist by site-id text string
#Note that it is note ordered by id
for i in range(len(filelist_lines)):
    filelist_lines[i] = filelist_lines[i].replace('\n', '')
    if "Gelbooru-" in filelist_lines[i]:
        ii = filelist_lines[i].index("Gelbooru-") + 9
        site = "Gelbooru"
    elif "rule34.xxx-" in filelist_lines[i]:
        ii = filelist_lines[i].index("rule34.xxx-") + 11
        site = "rule34.xxx"
    else:
        ii = "bad"
        print("bad line")
    if ii != "bad":
        jj = filelist_lines[i].index(".",ii)
        if "s" in filelist_lines[i][ii:jj]:
            jj = jj - 1
        id = filelist_lines[i][ii:jj]
    filelist_lines[i] = site + id + " zzzzz" + filelist_lines[i]
    
filelist_lines.sort()
    
for i in range(len(filelist_lines)):
    o = filelist_lines[i].index(" zzzzz") + 6
    filelist_lines[i] = filelist_lines[i][o:len(filelist_lines[i])]
    #try:
    #    file_metalist.write(filelist_lines[i] + "\n")
    #except:
    #    print("error")

filelist_index = 0
exiflist_index = 0

while filelist_index < len(filelist_lines) and exiflist_index <len(exiflist_lines):
    
    filelist_siteid = ""
    exiflist_siteid = ""
    site = ""
    
    #Get site-id from filelist_lines
    if "Gelbooru-" in filelist_lines[filelist_index]:
        ii = filelist_lines[filelist_index].index("Gelbooru-")
    elif "rule34.xxx-" in filelist_lines[filelist_index]:
        ii = filelist_lines[filelist_index].index("rule34.xxx-")
    else:
        ii = "bad"
        print("bad line")
    if ii != "bad":
        jj = filelist_lines[filelist_index].index(".",ii+7)
        if "s" in filelist_lines[filelist_index][ii:jj]:
            jj = jj - 1
        filelist_siteid = filelist_lines[filelist_index][ii:jj]

    #Get site-id from exiflist_lines
    if "Image from Gelbooru" in exiflist_lines[exiflist_index]:
        site = "Gelbooru"
    elif "Image from rule34.xxx" in exiflist_lines[exiflist_index]:
        site = "rule34.xxx"
    else:
        ii = "bad"
        print("bad line")
    if ii != "bad":
        ii = exiflist_lines[exiflist_index].index(" id:") + 4
        jj = exiflist_lines[exiflist_index].index(" ",ii)
        if "s" in exiflist_lines[exiflist_index][ii:jj]:
            jj = jj - 1
        id = exiflist_lines[exiflist_index][ii:jj]
        exiflist_siteid = site + "-" + id
    
    match_found = False
    #if match, add entry
    if filelist_siteid == exiflist_siteid:
        #file_metalist.write("match found for " + filelist_siteid + "\n")
        filelist_index += 1
        exiflist_index += 1
        match_found = True
    elif "rul" in filelist_siteid and "Gel" in exiflist_siteid:
        filelist_index += 1
        exiflist_index += 1
    elif "Gel" in filelist_siteid and "rul" in exiflist_siteid:
        filelist_index += 1
        exiflist_index += 1
    elif filelist_siteid < exiflist_siteid:
        #file_metalist.write("filelist_siteid " + filelist_siteid + " is smaller than exiflist_siteid " + exiflist_siteid + ". advanced filelist_index by 1." + "\n")
        filelist_index += 1
    elif filelist_siteid > exiflist_siteid:
        #file_metalist.write("exiflist_siteid " + exiflist_siteid + " is smaller than filelist_siteid " + filelist_siteid + ". advanced exiflist_siteid by 1." + "\n")
        exiflist_index += 1
        
    if match_found:
        a = exiflist_lines[exiflist_index]
        output_line = ""
        try:
            output_line += "START|present|" + filelist_lines[filelist_index] + "|"
            ia = a.index("Image from ") + 11
            ib = a.index(" ",ia)
            b = a[ia:ib]
            output_line += b + "|"
            ia = a.index("id:") + 3
            ib = a.index(" ",ia)
            b = a[ia:ib]
            output_line += b + "|"
            ia = a.index("rating:",ib) + 7
            ib = a.index(" ",ia)
            b = a[ia:ib]
            output_line += b + "|"
            ia = a.index("md5:",ib) + 4
            ib = a.index(" ",ia)
            ic = a.index("(",ia)
            ib = min(ib,ic)
            b = a[ia:ib]
            output_line += b + "|"
            ia = a.index("sample:",ib) + 7
            ib = a.index(" ",ia)
            b = a[ia:ib]
            output_line += b + "|"
            ia = a.index("booru-source:",ib) + 13
            ib = a.index(" ",ia)
            b = a[ia:ib]
            output_line += b + "|"
            ia = a.index("booru-score:",ib) + 12
            ib = a.index(" ",ia)
            b = a[ia:ib]
            output_line += b + "|"
            ia = a.index("Copyrights:",ib) + 11
            ib = a.index("  ",ia)
            b = a[ia:ib]
            output_line += " " + b + " |"
            ia = a.index("Characters:",ib) + 11
            ib = a.index("  ",ia)
            b = a[ia:ib]
            output_line += " " + b + " |"
            ia = a.index("Artists:",ib) + 8
            ib = a.index("  ",ia)
            b = a[ia:ib]
            output_line += " " + b + " |"
            ia = a.index("General tags:",ib) + 13
            ib = a.index("  ",ia)
            b = a[ia:ib]
            output_line += " " + b + " |END\n"
        except:
            foo = 1
        try:
            file_metalist.write(output_line)
        except:
            file_metalist.write("line write fail occurred")

'''
for filelist_line in filelist_lines:
    filelist_line = filelist_line.replace('\n', '')
    site = "xxxxx"
    if "Gelbooru-" in filelist_line:
        ii = filelist_line.index("Gelbooru-") + 9
        site = "Gelbooru"
    elif "rule34.xxx-" in filelist_line:
        ii = filelist_line.index("rule34.xxx-") + 11
        site = "rule34.xxx"
    else:
        ii = "bad"
        print("bad line")
    if ii != "bad":
        jj = filelist_line.index(".",ii)
        if "s" in filelist_line[ii:jj]:
            jj = jj - 1
        id = filelist_line[ii:jj]
        
        a = "xxxxx"
        output_line = ""
        for exiflist_line in exiflist_lines:
            if "Image from " + site in exiflist_line and "id:" + id in exiflist_line:
                a = exiflist_line
        if a != "xxxxx":
            try:
                output_line += "START|present|" + filelist_line + "|"
                ia = a.index("Image from ") + 11
                ib = a.index(" ",ia)
                b = a[ia:ib]
                output_line += b + "|"
                ia = a.index("id:") + 3
                ib = a.index(" ",ia)
                b = a[ia:ib]
                output_line += b + "|"
                ia = a.index("rating:",ib) + 7
                ib = a.index(" ",ia)
                b = a[ia:ib]
                output_line += b + "|"
                ia = a.index("md5:",ib) + 7
                ib = a.index(" ",ia)
                ic = a.index("(",ia)
                ib = min(ib,ic)
                b = a[ia:ib]
                output_line += b + "|"
                ia = a.index("sample:",ib) + 7
                ib = a.index(" ",ia)
                b = a[ia:ib]
                output_line += b + "|"
                ia = a.index("booru-source:",ib) + 13
                ib = a.index(" ",ia)
                b = a[ia:ib]
                output_line += b + "|"
                ia = a.index("booru-score:",ib) + 12
                ib = a.index(" ",ia)
                b = a[ia:ib]
                output_line += b + "|"
                ia = a.index("Copyrights:",ib) + 11
                ib = a.index("  ",ia)
                b = a[ia:ib]
                output_line += " " + b + " |"
                ia = a.index("Artists:",ib) + 8
                ib = a.index("  ",ia)
                b = a[ia:ib]
                output_line += " " + b + " |"
                ia = a.index("General tags:",ib) + 13
                ib = a.index("  ",ia)
                b = a[ia:ib]
                output_line += " " + b + " |END\n"
            except:
                print("Processing the Silventurous comment failed for " + filelist_line)
        if a == "xxxxx":
            output_line = "START|notpresent|" + filelist_line + "|||||||||||END\n"
        try:
            file_metalist.write(output_line)
        except:
            print("line write fail occurred")
'''