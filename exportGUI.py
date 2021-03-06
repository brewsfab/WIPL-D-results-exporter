from tkinter import *
from tkinter.filedialog import askopenfilenames,asksaveasfilename

from resultExplorer import resultExporter
from efficiencyCalculator import efficiencyCalculator

from pathlib import Path


def addprefix(prefix, filepath, extension="csv"):
	file_path = Path(filepath)
	return file_path.with_name('{}_{}.{}'.format(prefix,file_path.stem,extension)).as_posix()

class App:
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
		
		for idx, file in enumerate(files_list):

			if not self.current_folder:

				self.current_folder = Path(file).parent.as_posix()
				input_file_list = "Folder:\n\t{}\n Files:\n".format(self.current_folder)

			current_file = "{}. {}".format(idx+1,Path(file).name)
			input_file_list += "\t{}\n".format(current_file)
		self.message_widget_content.set(input_file_list)



	def process(self):
		for file in self.file_in:
			#renamed file
			renamed_with_param = addprefix(self.param_prefix,file)	
			
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

			if file and self.file_out: 
				resultExporterz = resultExporter(2,file,self.file_out)
				# resultExporterz.parser([3,4]) #Z-parameters
				# resultExporterz.parser([5,6]) #S-parameters
				# resultExporterz.parser([1,2]) #S-parameters
				resultExporterz.parser(self.parse_item) #Saved the parsed input to the output csv (self.file_out)

				#After the parsing display the sweep parameters and choose the one to export relative to
				sweep_param_list = resultExporterz.sweep_params_names
				if len(sweep_param_list) > 1:
					print(sweep_param_list)
					self.display_sweep_selector(sweep_param_list)
					selected_sweep_param = sweep_param_list[self.sweep_selector_var.get()]
					print(selected_sweep_param)
				else:
					selected_sweep_param = sweep_param_list[0]
					
				if self.efficiency_compute.get(): #If the efficiency calculation is selected
					resultExporterz.exporter(selected_sweep_param,1)
				else:
					resultExporterz.exporter(selected_sweep_param,0)
					# self.computeEfficiency(self.file_out)

	def display_sweep_selector(self, sweep_param_list):
		print(sweep_param_list)
		self.sweep_selector_var = IntVar()
		popup = Toplevel()
		popup.title("Sweep")
		Label(popup, text="""Select the relative sweep parameter""",font=("Arial",20),
				justify=LEFT, padx=20).pack()

		for idx,sweep_param in enumerate(sweep_param_list):
			Radiobutton(popup, 
                  text=sweep_param,
                  padx = 20, 
                  variable=self.sweep_selector_var, 
                  command=self.select_sweep_param,
                  value=idx).pack(anchor=W)#fill=X,anchor=W)

		Button(popup, text="Choose", command=popup.destroy).pack(padx=10,pady=10)

		popup.grab_set()
		self.window.wait_window(popup)

	def select_sweep_param(self):
		print("selected is : {}".format(self.sweep_selector_var.get()))

	def getparameterchoice(self):
		self.current_param_choice = self.params_choice.get()
		self.parse_item = self.parse_items_dict[self.current_param_choice]
		self.param_prefix = self.param_prefixs_dict[self.current_param_choice]
		print(self.current_param_choice)
		if self.current_param_choice == 3:
			#disable and gray the efficiency calculation because no formula for Y-parameters
			self.efficiency_compute.set(FALSE)
			self.efficiency_check_button.config(state=DISABLED)
		else:
			self.efficiency_check_button.config(state=NORMAL)


	def displayit(self):
		self.window = Tk()
		self.window.title("WIPL-D Data exporter")
		self.window.geometry("300x300")
		self.window.minsize(640,600)
		self.window.config(background='gray')

		self.params_choice = IntVar()
		self.params_choice.set(self.current_param_choice)

		#creer la frame
		frame = Frame(self.window,bg='gray')

		self.label_title = Label(frame,text="WIPL-D result exporter", font=("Arial",20),bg='gray', fg='white')
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
		self.efficiency_check_button = Checkbutton(frame, text="compute the efficiency", 
								variable=self.efficiency_compute
								)
		self.efficiency_check_button.pack(fill=X,anchor=W)
		self.efficiency_compute.set(True)


		self.file_in_button = Button(frame,
								text="Process", 
								font=("Arial",20),
								bg='white', 
								fg='gray', 
								command = self.process)

		self.file_in_button.pack(pady=25, 
								fill=X)

		frame.pack(expand=YES)
		#displays the window
		self.window.mainloop()



if __name__=="__main__":
	App = App()
