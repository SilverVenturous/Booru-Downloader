#WIP
#Generate in booru_files_metadata.csv a database of all the attributes of the files listed in file_list.txt
#The output is printed in booru_files_metadata.csv

from PIL import Image

#Todo: Delete contents of booru_files_metadata.csv

file = open('file_list.txt', 'r', encoding="utf-8")
lines = file.readlines()
f = open("booru_files_metadata.csv", "w")
a = ""
for line in lines:

    #get id
    if "Gelbooru-" in line:
        ii = line.index("Gelbooru-") + 9
    if "rule34.xxx-" in line:
        ii = line.index("rule34.xxx-") + 11
    jj = line.index(".",ii)
    if "s" in line[ii:jj]:
        jj = jj - 1
    id = line[ii:jj]
    line = line.replace('\n', '')
    #print(line)
    output_line = ""
    has_silverventurous_comment = True
    if ".jpg" in line or ".jpeg" in line or ".png" in line:
        try:
            im = Image.open(line)
        except:
            print("Error occurred while trying to open the file for EXIF reading")
        exif = im.getexif()
        if 0x9286 not in exif.keys():
            has_silverventurous_comment = False
        elif "Silver" not in exif[0x9286]:
            has_silverventurous_comment = False
        if has_silverventurous_comment:
            try:
                a = exif[0x9286]
            except:
                has_silverventurous_comment = False
    else:
        has_silverventurous_comment = False
        file_animeta = open('animated_metadata_database.txt', 'r', encoding="utf-8")
        animeta_lines = file_animeta.readlines()
        for animeta_line in animeta_lines:
            kk = "id:" + id + "  "
            if kk in animeta_line:
                a = animeta_line
                has_silverventurous_comment = True
    
    if has_silverventurous_comment:
        try:
            output_line += "START|present|" + line + "|"
            ia = a.index("Image from ") + 11
            ib = a.index(" ",ia)
            b = a[ia:ib]
            output_line += b + "|"
            ia = a.index("id:") + 4
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
            has_silverventurous_comment = False
            #print("Processing the Silventurous comment failed for " + line)
    if not has_silverventurous_comment:
        output_line = "START|notpresent|" + line + "|||||||||||END\n"
    try:
        f.write(output_line)
    except:
        print("line write fail occurred")
f.close()