import pandas as pd
from itertools import product, chain
from functools import reduce
from operator import and_
from pathlib import Path
from efficiencyCalculator import efficiencyCalculator


def addprefix(prefix, filepath, extension="csv"):
    file_path = Path(filepath)
    return file_path.with_name('{}_{}.{}'.format(prefix, file_path.stem, extension)).as_posix()


def addsuffix(suffix, filepath, extension="csv"):
    file_path = Path(filepath)
    return file_path.with_name('{}_{}.{}'.format(file_path.stem, suffix, extension)).as_posix()


def addElement(item, matrixelement):
    param, cplxpart = item.split("_")
    return param+matrixelement+"_"+cplxpart


class resultExporter:
    def __init__(self, number_, file_in, *args):

        # number_ is the number of rows of the square matrix (number of generators)
        self.number_el = number_*number_
        self.items_title = ["Y_real", "Y_imag","Z_real", "Z_imag", "S_real", "S_imag"]
        self.data_list = []

        if args:
            self._out = args[0]
        else:
            self._out = file_in.split(".")[0]+".csv"
        try:
            self.handle_in = open(file_in, "r")
        except IOError as e:
            print("Error with the files error_no:{} error_string:{}".format(e.errno, e.strerror))

    def exporter(self, sweep_param, computeEfficiencyType=None):

        if not len(self.sweep_params_names) > 1:
            self.dataframe.to_csv(self._out, index=None)
            if computeEfficiencyType:
                self.computeEfficiency(self.dataframe, self._out, sweep_param)
        else:
            if not sweep_param in self.sweep_params_names:
                print("not a valid sweep parameter")
            else:
                cross = self.sweep_params_names.copy()
                cross.remove(sweep_param)

                # combination of all the values
                for res in product(*[self.dataframe[name].unique() for name in cross]):

                    couplev = list(zip(cross, res))

                    conditions = [(self.dataframe[cpv[0]] == cpv[1])
                                  for cpv in couplev]
                    current_df = self.dataframe[reduce(and_, conditions)]
                    suffix_sweep_file = "_".join(map(str, chain(*couplev))).replace(".", "_")
                    filename_with_sweep_suffix = addsuffix(suffix_sweep_file, self._out)
                    current_df.to_csv(filename_with_sweep_suffix, index=None)

                    if computeEfficiencyType:
                        self.computeEfficiency(current_df, filename_with_sweep_suffix, sweep_param)

    def computeEfficiency(self, dataframe, outputfile, sweep_parameter):
        renamed_with_efficiency = addprefix('eff', outputfile)
        effcalc = efficiencyCalculator(dataframe, renamed_with_efficiency, sweep_parameter)
        effcalc.calculate_efficiency()

    def parser(self, items=None):

        notyetSet = True
        element_columns_names = []

        if notyetSet:
            if items:
                current_items_title = [el for idx, el in enumerate(self.items_title) if idx+1 in items]
            else:
                current_items_title = self.items_title

        while True:

            line1 = self.handle_in.readline().split()
            line1 = line1[1:]
            if not line1:
                break

            # Manage the sweep parameters from here
            temp_dict = {}
            temp_dict.update(zip(line1[0::2], map(float, line1[1::2])))

            line2 = self.handle_in.readline().split()
            freq_unit = line2[1]

            line3 = []

            for i in range(self.number_el):
                # all items
                current_line = self.handle_in.readline().split()
                if i == 0:
                    line3.append(current_line[0])

                # The matrix elements couple (i.e. 11,12,21,22) as prefix
                current_element = current_line[-8:-6]
                current_element_prefix = "".join(current_element)

                lines = current_line[-6:]
                if items:
                    lines = [el for idx, el in enumerate(lines) if idx+1 in items]

                line3 += lines

                if notyetSet:
                    current_items_title_with_element = [addElement(item, current_element_prefix) for item in current_items_title]
                    element_columns_names += current_items_title_with_element

            if notyetSet:
                freq_name = "frequency_"+freq_unit
                self.sweep_params_names = line1[0::2]
                other_elements = [freq_name]+element_columns_names
                self.all_columns_names = self.sweep_params_names+other_elements

            notyetSet = False

            temp_dict.update(zip(other_elements, line3))
            self.data_list.append(temp_dict)

        # close the file handles
        print("File parse reached the end!")
        self.handle_in.close()
        print("input file handle closed successfully!")
        self.dataframe = pd.DataFrame(self.data_list, columns=self.all_columns_names).astype('float64')
        print("Dataframe created with success!")