 # image_encryption


A client-server interaction where server would send an encrypted image to the client and the client would decrypt
back the image using some algorithms.

#Image_server- 
  1) Uploads an image to be sent.
  2) Generates a random key matrix.
  3) Encrypts the image.
  4) Sends it to the client.

#Image_client-
  1) Shows the received encrypted image.
  2) Decrypts the image and prints it.

Encryption technique used-
 
 HILL CIPHER:-

 1: Converts uploaded image into a 250x250 monochrome image.
 2: Generates a random matrix called 'key' of same size of the input image.
 3: Multiplies both matrices to for encrypted image.
 4: Compute inverse of key matrix.
 5: Multiply this inverse with result of step 3 and the result will be your original image.

Client-Server interaction:
 
 Client and server are interacting through "pickling" and "unpickling" methods of python which makes
 matrix object transfer easy and feasible.
