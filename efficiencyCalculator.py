import numpy as np
import pandas as pd
import cmath


class efficiencyCalculator:

	def __init__(self, input_file, output_file, efficiencytype):
		self.input_file = input_file
		self.output_file = output_file
		self.efficiency_dict = {}
		self.efficiencytype = efficiencytype

		self.processdata()

	def processdata(self):
		#handling later the error
		self.dataframe_in = pd.read_csv(self.input_file, header=None)
		self.nb_of_el = len(self.dataframe_in)
		self.stepper = 1 #stepper
		self.first_index = 4 #start of parameter values

	def calculate_efficiency(self):
		for i in range(self.nb_of_el):
			currentline = self.dataframe_in.loc[i]
			# step = str(currentline[self.stepper]) #must str from now before finding the way to solve the precision

			step = currentline[self.stepper] #use this now as it seems that for negative values the np.Series works wrong with str()

			p11= currentline[self.first_index]+1j*currentline[self.first_index+1]
			p12= currentline[self.first_index+2]+1j*currentline[self.first_index+3]
			p21= currentline[self.first_index+4]+1j*currentline[self.first_index+5]
			p22= currentline[self.first_index+6]+1j*currentline[self.first_index+7]

			# effmax.append(eff_max*100)
			if self.efficiencytype == 1:
				self.efficiency_dict[step] = self.efficiencyZparam(p11,p12,p21,p22)
			elif self.efficiencytype == 2:
				self.efficiency_dict[step] = self.efficiencySparam(p11,p12,p21,p22)


	def exportefficiency(self):
		dfout =  pd.Series(self.efficiency_dict).to_frame()
		dfout.to_csv(self.output_file, header=False)


	def efficiencyZparam(self, *parameters):
		z11, z12, z21, z22 = parameters

		kQ = (np.imag(z21)*np.imag(z12))/(np.real(z11)*np.real(z22))
		eff_max = 1-(2/(1+np.sqrt(1+kQ)))
		# eff_max = 1-(2/(1+np.real(cmath.sqrt(1+kQ))))
		# print("here is the efficiency: {}".format(eff_max*100))

		return eff_max*100

	def efficiencySparam(self, *parameters):
		s11, s12, s21, s22 = parameters

		Knum = 1-np.abs(s11)**2-np.abs(s22)**2+np.abs((s11*s22)-(s12*s21))**2
		Kden = 2*(np.abs(s12*s21))
		K = Knum/Kden

		# alpha = np.sqrt(2/(K-1))
		# eff_max_alpha = 1-(2/(1+np.sqrt(1+alpha**2)))
		eff_max = K - np.sqrt(K**2-1)
		
		return eff_max*100
