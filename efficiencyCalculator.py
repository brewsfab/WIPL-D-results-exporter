import numpy as np
import pandas as pd


class efficiencyCalculator:

	def __init__(self, dataframe, output_file, relative_sweep_param):
		#'Z11_real','Z11_imag','Z12_real','Z12_imag','Z21_real','Z21_imag','Z22_real','Z22_imag'
		#'S11_real','S11_imag','S12_real','S12_imag','S21_real','S21_imag','S22_real','S22_imag'
		self.dataframe = dataframe.reset_index(drop=True)
		self.output_file = output_file
		self.sweep_param = relative_sweep_param
		self.dataframe_cols = dataframe.columns

		if "Z11_real" in self.dataframe_cols:
			self.cols_to_select =['Z11_real','Z11_imag','Z12_real','Z12_imag','Z21_real','Z21_imag','Z22_real','Z22_imag']
			self.efficiencyFunction = self.efficiencyZparam
		else:
			self.cols_to_select =['S11_real','S11_imag','S12_real','S12_imag','S21_real','S21_imag','S22_real','S22_imag']
			self.efficiencyFunction = self.efficiencySparam

	def calculate_efficiency(self):
		efficiency_dict={}
		for i in range(len(self.dataframe)):
			currentline = self.dataframe.loc[i]
			# step = str(currentline[self.stepper]) #must str from now before finding the way to solve the precision

			sweep_param = currentline[self.sweep_param]
			p11= currentline[self.cols_to_select[0]]+1j*currentline[self.cols_to_select[1]]
			p12= currentline[self.cols_to_select[2]]+1j*currentline[self.cols_to_select[3]]
			p21= currentline[self.cols_to_select[4]]+1j*currentline[self.cols_to_select[5]]
			p22= currentline[self.cols_to_select[6]]+1j*currentline[self.cols_to_select[7]]

			efficiency_dict.update(((sweep_param, self.efficiencyFunction(p11,p12,p21,p22)),))

		#export from here
		eff_df =  pd.Series(efficiency_dict).to_frame()
		eff_df.to_csv(self.output_file, header=False)

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
