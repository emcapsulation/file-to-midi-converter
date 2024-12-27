from PIL import Image



class ImageFile:
	def __init__(self, filename, dimensions):
		self.filename = filename
		self.dimensions = dimensions

		self.im = Image.new("RGB", (dimensions[0], dimensions[1]))

		self.position = [0, 0]
		self.pixel = [0, 0, 0]
		self.pix_ind = 0


	def increment_position(self):
		self.position[0] += 1
		if self.position[0] >= self.dimensions[0]:
			self.position[0] = 0
			self.position[1] += 1

		if self.position[1] >= self.dimensions[1]:
			# Save the image, we ran out of space
			self.complete_image()


	def drawCompletedPixel(self):
		if self.pix_ind > 2:
			self.im.putpixel(tuple(self.position), tuple(self.pixel))

			self.pix_ind = 0
			self.pixel = [0, 0, 0]
			self.increment_position()


	def write_i_byte_to_image(self, i):
		self.pixel[self.pix_ind] = i
		self.pix_ind += 1
		self.drawCompletedPixel()


	def write_b_byte_to_image(self, b):
		i = int.from_bytes(b, byteorder="big")
		self.write_i_byte_to_image(i)


	def write_word_to_image(self, word):
		for c in word:
			self.write_i_byte_to_image(ord(c))
		

	def complete_image(self):
		self.im.putpixel(tuple(self.position), tuple(self.pixel))
		self.im.save(self.filename + ".png")



def write_file_extension(file_extension, im):
	# Write the file extension length
    ext_length = str(len(file_extension))
    im.write_i_byte_to_image(ord(ext_length))

    # Write the file extension
    im.write_word_to_image(file_extension)



def file_to_image(filename, file_extension):
	dimensions = [1280, 720]
	im = ImageFile(filename, dimensions)

	write_file_extension(file_extension, im)

	# Write the file as a MIDI
	f = open(filename+file_extension, "rb")
	byte = f.read(1)
	while byte:
		im.write_b_byte_to_image(byte)
		byte = f.read(1)

	f.close()

	# Write it to disk
	im.complete_image()