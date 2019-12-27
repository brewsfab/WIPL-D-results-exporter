class resultExporter:
	def __init__(self, number_,file_in,*args):
		self.sep = ","
		self.new_line = "\n"
		self.number_el = number_*number_ #TODO redefine the number_el
		if args:
			self._out = args[0]
		else:
			self._out = file_in.split(".")[0]+".csv"
		try:
			self.handle_in = open(file_in,"r")
			self.handle_out = open(self._out,"w+")
		except IOError as e:
			print("Error with the files error_no:{} error_string:{}".format(e.errno, e.strerror))


	def parser(self,items=None):
		while True:
			#line 1: Sweep parameter (<Parameter> <value>)
			# ['>>', 'Lp', '4.49000e+001']
			line1 = self.handle_in.readline().split()
			if not line1:
				break
			#line 2: Frequency unit (kHz or Mhz or Ghz)
			# ['>', 'MHz']
			line2 = self.handle_in.readline().split()
			#line 3: Results (<Frequency> <matrix element i> <matrix element j> <real part admittance Y-real[mS]> <imaginary part admittance Y-imag[mS]> <real part impedance Z-real[Ohm]> <imaginary part impedance Z-imag[Ohm]> <real part S-parameter S-real> <imaginary part S-parameter S-imag>)
			# ['0.135600000000000E+02', '1', '1', '0.113064980506897E+01', '-0.129274616241455E+02', '0.671416616439819E+01', '0.767674713134766E+02', '0.377433866262436E+00', '0.842696487903595E+00']
			#Would like to export one line for each parameters as for z11,z12,z21,z22
			line3=[]
			for i in range(self.number_el):
				#all items
				current_line = self.handle_in.readline().split()
				if i == 0:
					line3.append(current_line[0])
				lines = current_line[-6:]
				if items:
					lines=[el for idx,el in enumerate(lines) if idx+1 in items]

				line3 += lines
			line_to_write1 = self.sep.join(line1[1:])
			line_to_write2 = self.sep.join(line2[1:])
			line_to_write3 = self.sep.join(line3)
			self.handle_out.write((line_to_write1+self.sep+line_to_write2+self.sep+line_to_write3+self.new_line).replace("NaN","0"))

		#close the file handles
		print("File parse reached the end!")
		self.handle_in.close()
		print("input file handle closed successfully!")
		self.handle_out.close()
		print("output file handle closed successfully!")




# if __name__=="__main__":
# 	resultExporter = resultExporter(2,"single_segment_gaps_steps.ad1")#,"huile.csv")
# 	# resultExporter.parser()
# 	resultExporter.parser([3,4])