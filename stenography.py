# ## Problem 2:  steganography
# 
# This function will enable the user to embed arbitrary text (string) messages into an image (if there is enough room!)

import numpy as np
from matplotlib import pyplot as plt
import cv2


# Part A: here is a signature for the decoding
# remember - you will want helper functions!
def desteg_string( image_name):
    """
    This will take in a image, and using the lowest-bit (found from the last binary number),
    this code will decode a message from the binary numbers
    """
    if type(image_name) == type(''):
        raw_image = cv2.imread(image_name,cv2.IMREAD_COLOR)
    else: 
        raw_image = image_name
    image = raw_image.copy()
    num_rows, num_cols, num_chans = image.shape
    
    return_string = ""
    answer_string = ""
    
    for row in range(num_rows):
        for col in range(num_cols):
            for chan in range(num_chans):
                rgb = image[row,col,chan]
                bin_rgb = bin(rgb)
                last_bit = bin_rgb[-1]
                return_string += last_bit
    print("the binary of the string is", return_string)
    counter = 0
    for i in range(1,len(return_string)):
        
        if (i%8 == 0):
            c = return_string[i-8:i]
            print(c)
            
            num = int( c, 2 )
            if num == 0:
                return answer_string
            
            character = chr(num)
            answer_string += character
    
    return answer_string



message = desteg_string('small_flag_with_message_rgb.png')
print(message)


# Part B: here is a signature for the encoding/embedding
# remember - you will want helper functions!

# create helper function:
# helper function should go through each character in the message, get the number, and convert it into binary
# do binary of [2:]
# add binary of [2:]+ zeroes = '0'*(8-len(binary of [2:]))
# then add that binary function to a string + 16 zeroes

# go through each pixel as usual
# have a counter i and make sure that when i is equal to the length of binary function string, it stops
# go through each pixel, and see if all of the if cases pass

def stenograph_help(message):
    """
    This is a helper function, that converts the message into binary
    """
    return_string = ""
    for i in message:
        o = ord(i)
        b = bin(o)
        b = b[2:]
        zeroes = '0'*(8-len(b))
        binpiece = zeroes + b
        return_string += binpiece
    return return_string + 16*'0'

def steganographize( image_name, message ):
    """ 
    This will take the message, use the helper function to create a binary string, and use each implementation to change
    pixels to match the secret message 
    """
    raw_image = cv2.imread(image_name,cv2.IMREAD_COLOR)
    raw_image = cv2.cvtColor(raw_image,cv2.COLOR_BGR2RGB)
    image = raw_image.copy()
    num_rows, num_cols, num_chans = image.shape
    
    hidden_message = stenograph_help(message)
    #print(hidden_message)
    
    return_string = ""
    i = 0
    
    for row in range(num_rows):
        for col in range(num_cols):
            for chan in range(num_chans):
                if i == len(hidden_message):
                    return image
                else:
                    pixel = image[row,col,chan]
                    if hidden_message[i] == '1' and pixel%2 == 0:
                        new_pixel = pixel + 1
                        i += 1
                    elif hidden_message[i] == '0' and pixel%2 == 1:
                        new_pixel = pixel - 1
                        i += 1
                    else:
                        new_pixel = pixel
                        i += 1
                    #print(pixel, new_pixel)
                    image[row,col,chan] = new_pixel

from matplotlib import pyplot as plt
new_image = steganographize('shark.jpg', "There once was a boy named harry destined to be a star his parents were killed by Voldemort who gave him a lightning scar Yo, Harry! You're a wizard! Harry goes to Hogwarts he meets Ron and Hermione McGonagall requires he play for Gryffindor Draco is a Daddy's boy Quirrell becomes unemployed The sorcerer's stone is destroyed by Dumbledore Ron breaks his wand now Ginny's gone and Harry's in Mortal danger Tom Riddle hides his snake inside his ginormous secret chamber Harry blows up Aunt Marge The dementors come and take charge Lupin is a wolf The rat's a man and now the prisoner is at large They use time travel so they can save the prisoner of Azkaban who just so happens to be Harry's godfather. I don't really get it either. Harry gets put in the Triwizard Tournament With dragons and mermaids Oh no; Edward Cullen gets slayed He's back. Harry, Harry, it's getting scary. Voldemort's back and you're a revolutionary Harry Dumbledore, Dumbledore, Why is he ignoring your constant attempts to contact him? He is forced to leave the school Umbridge arrives, Draco's a tool Kids break into the Ministry Sirius Black is dead as can be, oh Split your soul, seven parts of a whole they're horcruxes, it's Dumbledore's end There once was a boy named Harry who constantly conquered death. But in one final duel between good and bad He may take his final breath")
plt.imshow(new_image)
plt.show() 
#to see the secret message use shark2.png (which was developed from shark.png!!!