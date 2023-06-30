from PIL import Image,ImageDraw
import random
import ast


def encryption(imagePath, word, imageName,encryptedDir):
    img = Image.open(imagePath)
    draw = ImageDraw.Draw(img)
    width,height = img.size
    max_pixels = width*height
    
    # list of keys 
    encryptionKeys = [] 

    #if size of the text biger than quantity of pixels exit 
    if(len(word)>max_pixels):
        return "What with size?"

    #transfrom to list of char in ASCII from words
    bin_word = []

    for char in word:
        temp = ord(char)
        bin_word.append(temp)
 
    def rand():#generate positions of pixel on the map
  
        for ordChar in bin_word:
      
            min = ordChar - 50
            max = ordChar + 50
            def generator():
                x = random.randint(0,width)
                y = random.randint(0,height)

                if ((x,y) in encryptionKeys):
                    generator()
                else:
                    rgb = img.getpixel((x,y))
                    result = None

                    for index,color in enumerate(rgb):#check how close to char from text
                        if(min  <= color <= max):
                            result = (x,y, index)###* result = ((x,y), index)
                            break
                        
                    if(result != None): #add key if passed
                        encryptionKeys.append(result)
                        data = list(rgb)
                        data[result[2]] = ordChar
                        data = tuple(data)
                        draw.point((x,y),data)

                    else:#recursion
                        generator()    
            generator()
    rand()
    # save encrypted image
    img.save(encryptedDir+imageName)
    path = (encryptedDir+imageName)
    # img.save(imagePath)
    passwd = str()
    for item in encryptionKeys:
        passwd +=(str(item)+"##")
    return passwd





def decode(imagePath, stringOfKeys):
    decodeKeys = []

    text = str(stringOfKeys)
    text = text.rstrip('#')
    key = (text.split('##'))
    for key in key:
      
        key=ast.literal_eval(key)
        decodeKeys.append(key)
       
    decodedPhrase = []
    img = Image.open(imagePath)

    for xyz in decodeKeys:
        x = xyz[0]
        y = xyz[1]
        z = xyz[2]
        rgb = img.getpixel((x,y))
        decodedPhrase.append(chr(rgb[z]))
    
    decodedPhrase="".join(decodedPhrase)
    return decodedPhrase

