from tkinter import *
from tkinter.filedialog import askopenfilenames,asksaveasfilename

from resultExplorer import resultExporter
from efficiencyCalculator import efficiencyCalculator

from pathlib import Path


class parser:
	def __init__(self):
		self.file_in =  ""
		self.file_out =  ""
		self.parameter_out_list = [
		("Z-parameters",1),
		("S-parameters",2),
		("Y-parameters",3)
		]
		self.current_param_choice = 1
		self.parse_items_dict = {1: [3,4],2:[5,6],3:[1,2]}
		self.current_folder = ""
		self.param_prefixs_dict = {1: "zparam",2: "sparam",3: "yparam"}
		self.param_prefix = self.param_prefixs_dict[self.current_param_choice]
		self.parse_item = self.parse_items_dict[self.current_param_choice]

		self.displayit()

	def OpenFile(self):
		self.current_folder = ""
		self.file_in = askopenfilenames(filetypes =[("WIPL-D results", "*.ad1"),("All Files","*.*")],
	                           title = "Choose a file."
	                           )
		self.displayfiles(self.file_in)

	def displayfiles(self, files_list):
		# input_file_display = []
		for idx, file in enumerate(files_list):

			if not self.current_folder:

				self.current_folder = Path(file).parent.as_posix()
				input_file_list = "Folder:\n\t{}\n Files:\n".format(self.current_folder)

			current_file = "{}. {}".format(idx+1,Path(file).name)
			input_file_list += "\t{}\n".format(current_file)
		# print(input_file_list)
		self.message_widget_content.set(input_file_list)
			# self.file_selected_display.insert(END, current_file)
		# print(files_list[0])
		# to_insert = "\n".join(files_list)
		# print(to_insert)
		 # self.file_selected_display. idx,file in enumerate(files_list):


	def parse(self):
		for file in self.file_in:
			#renamed file
			renamed_with_param = self.addprefix(self.param_prefix,file)	
			
			# Check if a list of file and save automatically to the save folder 
			# by substituting .ad1 to .csv for the export of the parameter files
			if(len(self.file_in)) > 1:
				self.file_out = renamed_with_param

			else:
				#ask for a single file name for saving
				self.file_out = asksaveasfilename(title = "Select file",
					defaultextension=".csv",
					initialfile=renamed_with_param,
					filetypes = [("Comma separated files(csv)","*.csv"),("all files","*.*")])

			print(self.file_out)

			if file and self.file_out:
				resultExporterz = resultExporter(2,file,self.file_out)
				# resultExporterz.parser([3,4]) #Z-parameters
				# resultExporterz.parser([5,6]) #S-parameters
				# resultExporterz.parser([1,2]) #S-parameters
				resultExporterz.parser(self.parse_item)
				if self.efficiency_compute.get():
					print("is selected {}".format(self.efficiency_compute.get()))
					#start the efficiency calculation
					renamed_with_efficiency = self.addprefix('eff', self.file_out)
					effcalc = efficiencyCalculator(self.file_out, renamed_with_efficiency, self.current_param_choice)
					effcalc.calculate_efficiency()
					effcalc.exportefficiency()


	def addprefix(self, prefix, filepath):
		file_path = Path(filepath)
		return file_path.with_name('{}_{}.csv'.format(prefix,file_path.stem)).as_posix()


	def getparameterchoice(self):
		self.current_param_choice = self.params_choice.get()
		self.parse_item = self.parse_items_dict[self.current_param_choice]
		self.param_prefix = self.param_prefixs_dict[self.current_param_choice]
		print(self.current_param_choice)


	def displayit(self):
		window = Tk()
		window.title("WIPL-D Data exporter")
		window.geometry("300x300")
		window.minsize(640,600)
		window.config(background='gray')

		self.params_choice = IntVar()
		self.params_choice.set(self.current_param_choice)

		self.compute_efficiency_choice = IntVar()
		self.compute_efficiency_choice.set(1) #automatic selection of the efficiency calculation


		#creer la frame
		frame = Frame(window,bg='gray')

		self.label_title = Label(frame,text="WIPL-D result parser", font=("Arial",20),bg='gray', fg='white')
		self.label_title.pack(expand=YES)

		self.message_widget_content = StringVar()
		self.message_widget_content.set("No selected files")
		self.file_selected_display = Message(frame,textvariable=self.message_widget_content, font=("Arial",9),bg='white', fg='black', width=600, aspect=2)
		self.file_selected_display.pack(fill=X,anchor=W,expand=YES)

		self.file_in_button = Button(frame,text="Select WIPL-D results file", font=("Arial",20),bg='white', fg='gray', command = self.OpenFile)
		self.file_in_button.pack(pady=25, fill=X)

		self.param_title = Label(frame,text="Choose parameter to save", font=("Arial",20),bg='gray', fg='white')
		self.param_title.pack(expand=YES)

		for parameter,val in self.parameter_out_list:
			Radiobutton(frame, 
                  text=parameter,
                  # padx = 200, 
                  variable=self.params_choice, 
                  command=self.getparameterchoice,
                  value=val).pack(fill=X,anchor=W) 

		self.efficiency_title = Label(frame,text="Save efficiency?", 
								font=("Arial",20),
								bg='gray', 
								fg='white')
		self.efficiency_title.pack(expand=YES)


		self.efficiency_compute = IntVar()
		Checkbutton(frame, text="compute the efficiency", 
								variable=self.efficiency_compute
								).pack(fill=X,anchor=W)
		self.efficiency_compute.set(True)


		self.file_in_button = Button(frame,
								text="Parse", 
								font=("Arial",20),
								bg='white', 
								fg='gray', 
								command = self.parse)

		self.file_in_button.pack(pady=25, 
								fill=X)

		frame.pack(expand=YES)
		#displays the window
		window.mainloop()



if __name__=="__main__":
	parser = parser()