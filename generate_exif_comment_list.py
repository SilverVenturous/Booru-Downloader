from PIL import Image

file = open('file_list.txt', 'r', encoding="utf-8")
lines = file.readlines()
f = open("exif_comment_list.txt", "w")

for line in lines:
    line = line.replace('\n', '')
    a = line
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
        a = a.replace('\n', '')
        f.write(a + "\n")
    else:
        try:
            f.write("failure for " + line + "\n")
        except:
            print("line write fail occurred")