################################################################################
#################                    Encoding                  #################
################################################################################

import pandas as pd
import time
import itertools
from tqdm import tqdm
from difflib import get_close_matches
import textwrap

from aaindex import aaindex1
from .model import Model
from .pyDSP import PyDSP
from .evaluate import Evaluate
from .pySAR import PySAR
from .utils import *
from .descriptors import Descriptors

class Encoding(PySAR):
    """
    The use-case of this class is when you have a dataset of protein sequences with
    a sought-after protein activity/fitness value and you want to measure this activity
    value for new and unseen sequences that have not had their activity value
    experimentally measured. Prior to protein sequences being passed into ML models, 
    the amino acids have to be numerically encoded. The encoding class allows for 
    evaluation of a variety of potential techniques at which to numerically encode the 
    protein sequences, allowing for the builiding of predictive regression ML models 
    that can ultimately predict the activity value of an unseen protein sequence by 
    mapping a relationship between sequence and activity/function. The strategies each 
    generate a huge number of potential models built an a plethora of available features 
    that you can then assess for performance and predictability, selecting the 
    best-performing model out of all those evaluated. This best-performing model should 
    then be used when you want to predict the activity/fitness value for new sequences.

    The encoding class inherits from the main PySAR module and allows for a
    dataset of protein sequences to be encoded through 3 main strategies: AAI Indices,
    protein Descriptors and AAI Indices + protein Descriptors. The encoding class
    and its methods differ from the PySAR class by allowing for the encoding using
    all available features, in comparison to the PySAR class which is mainly used for
    accessing individual or a small subset of features.
    
    To date, there are 566 indices supported in the AAI and pySAR supports 15 different 
    descriptors. The features can be encoded using different combinations, for example, 
    1, 2 or 3 descriptors can be used for the descriptor and AAI + Descriptor encoding 
    strategies. In total, this class supports over 410,000 possible ways at which to 
    numerically encode the protein sequences in the building of a predictive ML model 
    for mapping these sequences to a particular activity/function, known as a 
    Sequence-Activity-Relationship (SAR) or Sequence-Function-Relationship (SFR).

    Parameters
    ==========
    :config_file: (str)
        path to configuration file with all required parameters for the pySAR encoding
        pipeline.
    **kwargs: dict
        keyword arguments and values passed into constructor. The keywords should be 
        the same name and form of those in the configuration file. The keyword values
        input take precedence over those in the config files.

    Methods
    =======
    aai_encoding(aai_indices=None, sort_by='R2', output_folder=""):
        encoding protein sequences using indices from the AAI and aaindex package.
    descriptor_encoding(descriptors=None, desc_combo=1, sort_by='R2', output_folder=""):
        encoding protein sequences using protein descriptors from descriptors module and protpy package.
    aai_descriptor_encoding(aai_indices=None, descriptors=None, desc_combo=1, sort_by='R2', output_folder=""):
        encoding protein sequences using indices from the AAI in concatenation with 
        the protein descriptors from the descriptors module and protpy package.
    """
    def __init__(self, config_file="", **kwargs):

        self.config_file = config_file

        #pass config file and kwargs into parent pySAR class
        super().__init__(self.config_file, **kwargs)

    def aai_encoding(self, aai_indices=None, sort_by='R2', output_folder=""):
        """
        Encoding all protein sequences using each of the available indices in the
        AAI and aaindex package. The protein spectra of the AAI indices can be generated 
        if use_dsp is true when creating the Encodign instance, also utiilsied for the 
        DSP spectra are the instance attributes: spectrum, window and filter. If not true 
        then the encoced sequences from the AAI will directly be used - default. 
        
        Each encoding will be used as the feature data to build the predictive regression 
        ML models. To date, there are 566 indices in the AAI, therefore 566 total models 
        can be built using this encoding strategy. The metrics evaluated from the model 
        for each AAI encoding combination will be collated into a dataframe, saved and 
        returned, with the results sorted by R2 by default, this can be changed using 
        the sort_by parameter. You can sort the output dataframe via the other metrics, 
        including: RMSE, MSE, MAE, RPD and Explained Variance. 

        Parameters
        ==========
        :aai_indices: str/list (default=None)
            str/list of aai indices to use for encoding the predictive models, by default
            ALL AAI indices will be used if parameter remains as None.
        :sort_by: str (default=R2)
            sort output dataframe by specified column/metric value, results sorted by R2 
            score by default.
        :output_folder: str (default="")
            output folder to store results csv to, if empty then input will be stored in 
            the OUTPUT_FOLDER global var.

        Returns
        =======
        :aaindex_metrics_df: pd.DataFrame
            dataframe of calculated metric values from generated predictive models
            encoded using indices in the AAI for the AAI encoding strategy. Output will 
            be of the shape X x 8, where X is the number of indices that can be used
            for the encoding and 8 is the results/metric columns. If no indices are 
            passed in then this shape will be 566 x 8.
        """
        #initialise dataframe to store all output results of AAI encoding
        aaindex_metrics_df = pd.DataFrame(columns=['Index', 'Category', 'R2', 'RMSE',
            'MSE', 'MAE', 'RPD', 'Explained Variance'])

        #lists to store results for each predictive model
        index_ = []
        category_ = []
        r2_ = []
        mse_ = []
        rmse_ = []
        rpd_ = []
        mae_ = []
        explained_var_ = []

        #if no indices passed into aai_indices then use all indices by default
        if (aai_indices == None or aai_indices == [] or aai_indices == ""):
            all_indices = aaindex1.record_codes()
        elif (isinstance(aai_indices, str)):   #if single aai index input, cast to list
            if (',' in aai_indices):
                all_indices = aai_indices.replace(' ', '').split(',') #split comma seperated list of indices into list
            else:
                all_indices = [aai_indices]
        elif ((not isinstance(aai_indices, list)) and (not isinstance(aai_indices, str))):
            raise TypeError("Input AAI list is not of type list or str, got {}.".format(type(aai_indices)))
        else:
            all_indices = aai_indices

        #remove any duplicates from aai indices list, sort alphabetically
        all_indices = sorted(list(set(all_indices)))

        #validate each input AAI acession number is valid, if not raise error
        for index in all_indices:
            if not (index in aaindex1.record_codes()):
                raise ValueError("AAI record {} not found in list of available record codes.".format(index))
                      
        #create text wrapper for amino acid indices and model parameters text
        line_length = 90

        #create temp Model object to access the models' parameter values for use in display text below
        temp_model_parameters = Model([], self.activity, self.algorithm, parameters=self.model_parameters)
        
        print('\n##########################################################################################\n')
        print('# Encoding using {} AAI combination(s) with the parameters:\n'.format(len(all_indices)))
        #only output indices if there are 10 or less
        if (len(all_indices) <= 10):
            print(textwrap.fill('# AAI Indices: {}'.format(', '.join(all_indices)), line_length))
        else:
            print('# AAI Indices: {}'.format(len(all_indices)))
        if (self.use_dsp): 
            print('# DSP Parameters:\n#   Spectrum: {}\n#   Window Function: {}\n#   Filter Function: {}'.format(
                    self.spectrum, self.window_type, self.filter_type))   
        print('# Configuration File: {}\n# Dataset: {}\n# Number of Sequences/Sequence Length: {} x {}\n# Target Activity: {}\n# Algorithm: {}'.
              format(os.path.basename(self.config_file), os.path.basename(self.dataset), self.num_seqs, self.sequence_length, self.activity_col, repr(temp_model_parameters)))
        if (self.model_parameters == "" or self.model_parameters is None or self.model_parameters == {}):
            print(textwrap.fill('# Model Parameters: {}'.format(temp_model_parameters.model.get_params()), line_length))
        else:
            print(textwrap.fill('# Model Parameters: {}'.format(self.model_parameters), line_length))
        print('# Test Split: {}'.format(self.test_split)) 
        print('\n##########################################################################################\n')

        '''
        1.) Get AAI index encoding of protein sequences, if using DSP (use_dsp = True),
        create instance of pyDSP class and generate protein spectra from the AAI
        indices, according to instance parameters: spectrum, window and filter.
        2.) Build model using encoded AAI indices or protein spectra as features.
        3.) Predict and evaluate the model using the test data.
        4.) Append index, its category and calculated metrics to lists.
        5.) Repeat steps 1 - 4 for all indices.
        6.) Output results into a final dataframe, save to OUTPUT_DIR and return.
        '''
        #start time counter
        start = time.time() 

        #disable tqdm progress bar if 5 or less aai indices input
        tqdm_disable = False
        if (len(all_indices)) <= 5:
            tqdm_disable = True

        #using tqdm package to create a progress bar showing encoding progress
        for index in tqdm(all_indices[:int(len(all_indices))], unit=" indices", position=0, 
            desc="AAI Indices", disable=tqdm_disable, ncols=90):

            #get AAI indices encoding for sequences according to index var
            encoded_seqs = self.get_aai_encoding(index)

            #generate protein spectra from pyDSP class if use_dsp is true, pass in all DSP related parameters, use object as training data
            if (self.use_dsp):
                pyDSP = PyDSP(self.config_file, protein_seqs=encoded_seqs, spectrum=self.spectrum, window_type=self.window_type, filter_type=self.filter_type)
                pyDSP.encode_sequences()
                X = pd.DataFrame(pyDSP.spectrum_encoding)
            else:
                #aai index encoding set as training data
                X = pd.DataFrame(encoded_seqs)

            #renaming columns in format aai_X, where X is the encoded amino acid number in the sequence
            col_counter = 1
            for col in X.columns:
                X.rename(columns={col: "aai_" + str(col_counter)}, inplace=True)
                col_counter+=1

            #get observed activity values from the dataset
            Y = self.activity

            #create instance of model class
            model = Model(X, Y, self.algorithm, parameters=self.model_parameters)

            #split feature data and labels into train and test data
            X_train, X_test, Y_train, Y_test = model.train_test_split()

            #fit model to training data
            model_fit = model.fit()

            #predict activity values for the test data
            Y_pred = model.predict()

            #initialise instance of Evaluate class
            eval = Evaluate(Y_test, Y_pred)

            #append values/results from current AAI encoding iteration to lists
            index_.append(index)
            category_.append(aaindex1[index].category)
            r2_.append(eval.r2)
            rmse_.append(eval.rmse)
            mse_.append(eval.mse)
            rpd_.append(eval.rpd)
            mae_.append(eval.mae)
            explained_var_.append(eval.explained_var)

        #stop time counter, calculate elapsed time
        end = time.time()      
        elapsed = end - start

        print('\nElapsed time for AAI Encoding: {0:.2f} seconds.'.format(elapsed))
        print('\n##########################################################################################')

        #set columns in the output dataframe to each of the values/metrics lists
        aaindex_metrics_= aaindex_metrics_df.copy()
        aaindex_metrics_['Index'] = index_
        aaindex_metrics_['Category'] = category_
        aaindex_metrics_['R2'] = r2_
        aaindex_metrics_['RMSE'] = rmse_
        aaindex_metrics_['MSE'] = mse_
        aaindex_metrics_['RPD'] = rpd_
        aaindex_metrics_['MAE'] = mae_
        aaindex_metrics_['Explained Variance'] = explained_var_

        #convert index and category from default Object -> String datatypes
        aaindex_metrics_['Index'] = aaindex_metrics_['Index'].astype(pd.StringDtype())
        aaindex_metrics_['Category'] = aaindex_metrics_['Category'].astype(pd.StringDtype())

        #sort output dataframe by sort_by parameter, sorted by R2 by default
        if (sort_by not in aaindex_metrics_df.columns):
            sort_by = 'R2'

        #sort ascending or descending depending on sort_by metric
        sort_ascending = False
        if not (sort_by == "R2" or sort_by == "Explained Variance"):
            sort_ascending = True

        #sort results according to sort_by parameter (R2 by default)
        aaindex_metrics_ = aaindex_metrics_.sort_values(by=[sort_by], ascending=sort_ascending)

        #save results dataframe, saved to OUTPUT_DIR by default.
        save_results(aaindex_metrics_, 'aaindex_results', output_folder=output_folder)

        return aaindex_metrics_

    def descriptor_encoding(self, descriptors=[], desc_combo=1, sort_by='R2', output_folder=""):
        """
        Encoding all protein sequences using the available physiochemical, biochemical
        and structural descriptors from the custom-built protpy package. The sequences 
        can be encoded using combinations of 1, 2 or 3 of these descriptors, dictated 
        by the desc_combo input parameter: set this to 1, 2 or 3 for what encoding 
        combination to use, default is 1. 
        
        Each descriptor encoding will be used as the feature data to build the predictive 
        regression ML models. These models can then be used to predict the sought-after
        activity/fitness value for unseen test sequences. With 15 descriptors supported 
        by pySAR & protpy this means there can be 15, 105 and 455 total predictive models 
        built for 1, 2 or 3 descriptors, respecitvely. These totals may vary depending on 
        the meta-parameters on some of the descriptors e.g the lag or lambda for the 
        autocorrelation and pseudo amino acid descriptors, respectively. The metrics 
        evaluated from the model for each descriptor encoding combination will be collated 
        into a dataframe and saved and returned, with the results sorted by the R2 score 
        by default, this can be changed using the sort_by parameter.

        Parameters
        ==========
        :descriptors: str/list (default=[])
            str/list of descriptors to use for encoding, by default all available descriptors
            in the protpy package will be used for the encoding.
        :desc_combo: int (default=1)
            combination of descriptors to use, default of 1.
        :sort_by: str (default=R2)
            sort output dataframe by specified column/metric value, results sorted by R2 
            score by default.
        :output_folder: str (default="")
            output folder to store results csv to, if parameter not set then output will 
            be stored in the OUTPUT_FOLDER global var.

        Returns
        =======
        :desc_metrics_df_: pd.DataFrame
            dataframe of calculated metric values from generated predictive models
            encoded using all or selected input descriptors for the descriptors 
            encoding strategy. Output will be of the shape X x 8, where X is the 
            number of descriptors input and 8 is the results/metric columns. By 
            default the output shape will be 15 x 8, but with a desc_combo of 2 
            and 3, the shape will be 105 x 8 and 455 x 8, respectively.
        """
        #create dataframe to store output results from models
        desc_metrics_df = pd.DataFrame(columns=['Descriptor', 'Group', 'R2', 'RMSE',
            'MSE', 'MAE', 'RPD', 'Explained Variance'])

        #lists to store results for each predictive model
        descriptor = []
        descriptor_group_ = []
        r2_ = []
        mse_ = []
        rmse_ = []
        rpd_ = []
        mae_ = []
        explained_var_ = []

        #create instance of descriptors class using config file and any kwargs
        desc = Descriptors(self.config_file, **self.kwargs)

        #if no descriptors passed into descriptors input param then use all descriptors by default,
        #get list of all descriptors according to desc_combo value
        if ((not isinstance(descriptors, list)) and (not isinstance(descriptors, str))):
            raise TypeError("Input Descriptor parameter is not of type list or str, got {}.".format(type(descriptors)))
        elif (descriptors == [] or descriptors == ""):
            all_descriptors = desc.all_descriptors_list(desc_combo) #using all descriptors
        elif (isinstance(descriptors, str)):     #if single descriptor input, cast to list
            if (',' in descriptors):
                all_descriptors = descriptors.replace(' ', '').split(',') #split comma seperated list of descriptors into list
            else:
                all_descriptors = [descriptors]     
        else:
            if (desc_combo == 2):
                all_descriptors = list(itertools.combinations(descriptors, 2))
            elif (desc_combo == 3):
                all_descriptors = list(itertools.combinations(descriptors, 3))
            else:
                all_descriptors = descriptors     #using default combination of descriptors

        #remove any duplicates from descriptors list, sort alphabetically
        all_descriptors = sorted(list(set(all_descriptors)))

        #create text wrapper for descriptors and model parameters text
        line_length = 90

        #create temp Model object to access the models' parameter values for use in display text below
        temp_model_parameters = Model([], self.activity, self.algorithm, parameters=self.model_parameters)

        print('\n##########################################################################################\n')
        print('# Encoding using {} descriptor combination(s) with the parameters:\n'.format(len(all_descriptors)))
        print(textwrap.fill('# Descriptors: {}'.format(', '.join(all_descriptors)), line_length))
        print('# Configuration File: {}\n# Dataset: {}\n# Number of Sequences/Sequence Length: {} x {}\n# Target Activity: {}\n# Algorithm: {}'.format(
            os.path.basename(self.config_file), os.path.basename(self.dataset), len(self.data), self.data[self.sequence_col].str.len().max(), self.activity_col, repr(temp_model_parameters)))
        if (self.model_parameters == "" or self.model_parameters is None or self.model_parameters == {}):
            print('# Model Parameters: {}'.format(temp_model_parameters.model.get_params()))        
        else:
            print('# Model Parameters: {}'.format(self.model_parameters))       
        print('# Test Split: {}'.format(self.test_split))
        print('\n##########################################################################################')

        #start counter
        start = time.time()     

        '''
        1.) Get current descriptor value or combination of descriptors from all_descriptors list for 
            dataset of protein sequences.
        2.) Build model using calculated descriptor features from current descriptor(s).
        3.) Predict and evaluate the model using the test data protein sequences.
        4.) Append descriptor(s) and calculated metrics to lists.
        5.) Repeat steps 1 - 4 for all descriptors.
        6.) Output results into a final dataframe, save it and return, sorting by sort_by parameter.
        '''

        #disable tqdm progress bar if only 3 descriptors or less input
        tqdm_disable = False
        if (len(all_descriptors)) <= 3:
            tqdm_disable = True

        for descr in tqdm(all_descriptors[:int(len(all_descriptors))], unit=" descriptor", position=0, 
            desc="Descriptors", mininterval=30, disable=tqdm_disable, ncols=90):

            #reset descriptor DF and list
            desc_ = pd.DataFrame()           
            descriptors = []
       
            #if using 2 or 3 descriptors, append each descriptor & its category to list
            if (desc_combo == 2 or desc_combo == 3):
                for de in descr:
                    #get closest descriptor name match, required for appending its group name
                    desc_matches = get_close_matches(de, desc.valid_descriptors, cutoff=0.6)
                    if (desc_matches != []):
                        desc_name = desc_matches[0]  #set desc to closest descriptor match found
                    else:
                        desc_name = None
                    descriptors.append(getattr(desc, de))
                    if not (desc_name is None): #only append group name if valid group found
                        descriptor_group_.append(desc.descriptor_groups[desc_name])
                desc_ = pd.concat(descriptors, axis=1) #concatenate descriptors
            else:
                #get closest descriptor name match, required for appending its group name
                desc_matches = get_close_matches(descr, desc.valid_descriptors, cutoff=0.6)
                if (desc_matches != []):
                    desc_name = desc_matches[0]  #set desc to closest descriptor match found
                else:
                    desc_name = None
                desc_ = desc.get_descriptor_encoding(descr)
                if not (desc_name is None): #only append group name if valid group found
                    descriptor_group_.append(desc.descriptor_groups[desc_name])
            
            #set model training data to desc_ dataframe
            X = desc_   

            #get protein activity values - training labels
            Y  = self.activity
            
            '''
            Note: If using the PlsRegression algorithm and there is only 1 feature (1-dimension)
            in the feature data X (e.g SOCN) then create a new PLSReg model and manually set the
            n_components parameter to 1 instead of the default 2 - this stops the error:
            'ValueError - Invalid Number of Components: 2'
            '''
            #get train/test split, fit model and predict activity of test data
            if ((X.shape[1] == 1) and (self.algorithm.lower() == "plsregression")):
              tmp_model = Model(X, Y, self.algorithm, parameters={'n_components':1})
              X_train, X_test, Y_train, Y_test = tmp_model.train_test_split(test_split=self.test_split)
              model_fit = tmp_model.fit()
              Y_pred = tmp_model.predict()
            else:
              tmp_model = Model(X, Y, self.algorithm, parameters=self.model_parameters)
              X_train, X_test, Y_train, Y_test = tmp_model.train_test_split(test_split=self.test_split)
              model_fit = tmp_model.fit()
              Y_pred = tmp_model.predict()

            #create instance of Evaluate class
            eval = Evaluate(Y_test, Y_pred)

            #append values/results from current descriptor encoding iteration to lists
            descriptor.append(descr)
            r2_.append(eval.r2)
            rmse_.append(eval.rmse)
            mse_.append(eval.mse)
            rpd_.append(eval.rpd)
            mae_.append(eval.mae)
            explained_var_.append(eval.explained_var)

        #stop counter and calculate elapsed time
        end = time.time()           
        elapsed = end - start

        print('\nElapsed time for Descriptor Encoding: {0:.2f} seconds.\n'.format(elapsed))
        print('\n##########################################################################################')

        #if using combinations of 2 or 3 descriptors, group every 2 or 3 descriptor
        #groups into one element in the descriptor group list
        if (desc_combo == 2):
          descriptor_group_= [','.join(x) for x in zip(descriptor_group_[0::2],
            descriptor_group_[1::2]) ]
        elif (desc_combo == 3):
          descriptor_group_= [ ','.join(x) for x in zip(descriptor_group_[0::3],
            descriptor_group_[1::3],  descriptor_group_[2::3])]

        #set columns in the output dataframe to each of the values/metrics lists
        desc_metrics_df_= desc_metrics_df.copy()
        desc_metrics_df_['Descriptor'] = descriptor
        desc_metrics_df_['Group'] = descriptor_group_
        desc_metrics_df_['R2'] = r2_
        desc_metrics_df_['RMSE'] = rmse_
        desc_metrics_df_['MSE'] = mse_
        desc_metrics_df_['RPD'] = rpd_
        desc_metrics_df_['MAE'] = mae_
        desc_metrics_df_['Explained Variance'] = explained_var_

        #convert descriptor and group columns from default Object -> string datatype
        desc_metrics_df_['Descriptor'] = desc_metrics_df_['Descriptor'].astype(pd.StringDtype())
        desc_metrics_df_['Group'] = desc_metrics_df_['Group'].astype(pd.StringDtype())

        #sort output dataframe by sort_by parameter, sorted by R2 by default
        if (sort_by not in desc_metrics_df_.columns):
            sort_by = 'R2'

        #sort ascending or descending depending on sort_by metric
        sort_ascending = False
        if not (sort_by == "R2" or sort_by == "Explained Variance"):
            sort_ascending = True

        #sort results according to sort_by parameter (R2 by default)
        desc_metrics_df_ = desc_metrics_df_.sort_values(by=[sort_by], ascending=sort_ascending)

        #set save filename according to the descriptor combinations type
        if (desc_combo == 2):
            save_filename = 'desc_combo2_results'
        elif (desc_combo == 3):
            save_filename = 'desc_combo3_results'
        else:
            save_filename = 'desc_results'

        #save results dataframe to specified save_filename
        save_results(desc_metrics_df_, save_filename, output_folder=output_folder)

        return desc_metrics_df_

    def aai_descriptor_encoding(self, aai_indices=[], descriptors=[], desc_combo=1, sort_by='R2', output_folder=""):
        """
        Encoding all protein sequences using each of the available indices in the AAI and
        aaindex package in concatenation with the protein descriptors available via the 
        protpy pacakge. The sequences can be encoded using 1 AAI + 1 Descriptor, 2 
        Descriptors or 3 Descriptors, dictated by the desc_combo input parameter: set 
        this to 1, 2 or 3 for what encoding combination to use, default is 1. The protein 
        spectra of the AAI indices will be generated if the config param use_dsp is true, 
        also utilised for the DSP transformation is the class attributes: spectrum, window 
        and filter. 
        
        Each numerical encoding will be used as the feature data to build the predictive 
        regression ML models. To date, there are 566 indices and pySAR/protpy supports 
        15 descriptors so the encoding process will generate 8490, ~59000 and ~257000 
        models, when using 1, 2 or 3 descriptors + AAI indices, respectively. These values 
        may vary depending on the meta-parameters on some of the descriptors such as the 
        lag or lambda for the autocorrelation and pseudo amino acid descriptors, respectively. 
        The metrics evaluated from the model, accessing its accuracy and predictability for 
        each AAI + Descriptor encoding combination will be collated into a dataframe and saved 
        and returned, sorted by the R2 score by default.

        Parameters
        ==========        
        :aai_indices: str/list (default=[])
            str/list of aai indices to use for encoding the predictive models, by default
            ALL AAI indices will be used.
        :descriptors: list (default=[])
            str/list of descriptors to use for encoding, by default all available descriptors
            in the protpy package will be used for the encoding.
        :desc_combo: int (default=1)
            combination of descriptors to use.
        :sort_by: str (default=R2)
            sort output dataframe by specified column/metric value, results sorted by R2 
            score by default.
        :output_folder: str (default="")
            output folder to store results csv to, if empty input it will be stored in 
            the OUTPUT_FOLDER global var.

        Returns
        =======
        :aai_desc_metrics_df_: pd.DataFrame
            dataframe of calculated metric values from generated predictive models
            encoded using AAI indices + descriptors encoding strategy. The output will
            be of shape (X * Y) x 10, where X is the number of AAI indices input, Y is
            the number of descriptors input and 10 is the results/metrics columns of 
            the output dataframe. Using the default values and desc_combo of 1, 2 and 
            3, the output shapes will be (566 * 15) x 10, (566 * 105) x 10, or 
            (566 * 455) x 10.
        """
        #create dataframe to store output results from models
        aai_desc_metrics_df = pd.DataFrame(columns=['Index', 'Category', 'Descriptor',\
            'Group', 'R2', 'RMSE', 'MSE', 'RPD', 'MAE', 'Explained Variance'])

        #lists to store results for each predictive model
        index_ = []
        index_category_ = []
        descriptor_ = []
        descriptor_group_ = []
        r2_ = []
        mse_ = []
        rmse_ = []
        rpd_ = []
        mae_ = []
        explained_var_ = []

        #raise error if invalid parameter data types input
        if ((not isinstance(aai_indices, list)) and (not isinstance(aai_indices, str))):
            raise TypeError("Input AAI parameter is not of type list or str, got {}.".format(type(aai_indices)))
        #if no indices passed into aai_indices then use all indices by default
        elif (aai_indices == None or aai_indices == [] or aai_indices == ""):
            all_indices = aaindex1.record_codes()
        elif (isinstance(aai_indices, str)):   #if single descriptor input, cast comma seperated indices to list
            if (',' in aai_indices):
                all_indices = aai_indices.replace(' ', '').split(',')
            else:
                all_indices = [aai_indices]
        else:
            all_indices = aai_indices

        #remove any duplicates from aai indices list, sort alphabetically
        all_indices = sorted(list(set(all_indices)))

        #validate each input AAI ascession number is valid, if not raise error
        for index in all_indices:
            if not (index in aaindex1.record_codes()):
                raise ValueError("AAI record {} not found in list of available record codes.".format(index))
           
        #create instance of Descriptors class using config file and any kwargs
        desc = Descriptors(config_file=self.config_file, **self.kwargs)

        #raise error if invalid parameter data types input
        if ((not isinstance(descriptors, list)) and (not isinstance(descriptors, str))):
            raise TypeError("Input Descriptor parameter is not of type list or str, got {}.".format(type(descriptors)))
        #if no descriptors passed into descriptors then use all descriptors by default,
        elif (descriptors == None or descriptors == [] or descriptors == ""):
            all_descriptors = desc.all_descriptors_list(desc_combo)
        elif (isinstance(descriptors, str)):     #if single descriptor input, cast comma seperated descriptors to list
            if (',' in descriptors):
                all_descriptors = descriptors.replace(' ', '').split(',')
            else:
                all_descriptors = [descriptors]         
        else:
            #get list of all descriptors according to desc_combo value
            if (desc_combo == 2):
                all_descriptors = list(itertools.combinations(descriptors, 2))
            elif (desc_combo == 3):
                all_descriptors = list(itertools.combinations(descriptors, 3))
            else:
                all_descriptors = descriptors

        #remove any duplicates from descriptors list, sort alphabetically
        all_descriptors = sorted(list(set(all_descriptors)))

        #create text wrapper for amino acid indices and descriptors text, split to newline if surpasses line length
        line_length = 90

        #create temp Model object to access the models' parameter values for use in display text below
        temp_model_parameters = Model([], self.activity, self.algorithm, parameters=self.model_parameters)

        print('\n###########################################################################\n')
        print('# Encoding using {} AAI and {} descriptor combination(s) with the parameters:\n'.format(
            len(all_indices), len(all_descriptors)))
        #only output indices if there are 10 or less
        if (len(all_indices) <= 10):
            print(textwrap.fill('# AAI Indices: {}'.format(', '.join(all_indices)), line_length))
        else:
            print('# AAI Indices: {}'.format(len(all_indices)))
        if (self.use_dsp):
            print('# DSP Parameters:\n#   Spectrum: {}\n#   Window Function: {}\n#   Filter Function: {}'.format(
                    self.spectrum, self.window_type, self.filter_type)) 
        print(textwrap.fill('# Descriptors: {}'.format(', '.join(all_descriptors)), line_length))
        print('# Configuration File: {}\n# Dataset: {}\n# Number of Sequences/Sequence Length: {} x {}\n# Target Activity: {}\n# Algorithm: {}'.format(
            os.path.basename(self.config_file), os.path.basename(self.dataset), len(self.data), self.data[self.sequence_col].str.len().max(), self.activity_col, repr(temp_model_parameters)))
        if (self.model_parameters == "" or self.model_parameters is None or self.model_parameters == {}):
            print('# Model Parameters: {}'.format(temp_model_parameters.model.get_params()))        
        else:
            print('# Model Parameters: {}'.format(self.model_parameters))                   
        print('# Test Split : {}'.format(self.test_split))
        print('\n###########################################################################')

        #start counter
        start = time.time() 

        '''
        1.) Get AAI index encoding of protein sequences. If using DSP, create instance
            of pyDSP class and generate protein spectra from the AAI indices, according to
            instance parameters: spectrum, window and filter.
        2.) Get all descriptor values and concatenate to AAI encoding features.
        3.) Build model using concatenated AAI and Descriptor features as the training data.
        4.) Predict and evaluate the model using the test data unseen protein sequences.
        5.) Append index, descriptor and calculated metrics to lists.
        6.) Repeat steps 1 - 5 for all indices in the AAI.
        7.) Output results into a final dataframe, save it and return, sort by sort_by parameter.
        '''

        #disable tqdm progress bar if 2 or less aai indices input
        tqdm_disable = False
        if (len(all_indices)) <= 2:
            tqdm_disable = True
        
        for index in tqdm(all_indices[:int(len(all_indices))], unit=" indices", desc="AAI Indices", disable=tqdm_disable, ncols=90):

            #get AAI indices encoding for sequences according to index var
            encoded_seqs = self.get_aai_encoding(index)

            #generate protein spectra from pyDSP class if use_dsp is true, pass in all DSP related parameters, use object as training data
            if (self.use_dsp):
                pyDSP = PyDSP(self.config_file, protein_seqs=encoded_seqs, spectrum=self.spectrum, window_type=self.window_type, filter_type=self.filter_type)
                pyDSP.encode_sequences()
                X_aai = pd.DataFrame(pyDSP.spectrum_encoding)
            else:
                X_aai = pd.DataFrame(encoded_seqs)
            
            #renaming columns in format aai_X, where X is the encoded amino acid number in the sequence
            col_counter = 1
            for col in X_aai.columns:
                X_aai.rename(columns={col: "aai_" + str(col_counter)}, inplace=True)
                col_counter+=1

            #disable tqdm progress bar if only 1 descriptor being used
            tqdm_disable = False
            if (len(all_descriptors)) <= 1:
                tqdm_disable = True
    
            #iterate through all descriptors
            for descr in tqdm(all_descriptors, leave=False, unit=" descriptor", desc="Descriptors", disable=tqdm_disable, ncols=90):

                #reset descriptor DF and list
                desc_ = pd.DataFrame()
                descriptors = []

                #if using 2 or 3 descriptors, append each descriptor & its category to list
                if (desc_combo == 2 or desc_combo == 3):
                    for de in descr:
                        descriptors.append(getattr(desc, de)) #get descriptor attribute
                        descriptor_group_.append(desc.descriptor_groups[de])
                    desc_ = pd.concat(descriptors, axis=1) #concat to desc_ dataframe
                #if only using 1 descriptor
                else:
                    desc_ = getattr(desc, descr)    #get descriptor attribute
                    descriptor_group_.append(desc.descriptor_groups[descr])

                #set training data to cincatenated aai and descriptor feature dataframes
                X = pd.concat([desc_, X_aai], axis=1)

                #get protein activity values
                Y  = self.activity

                '''
                Note: If using the PlsRegression algorithm and there is only 1 feature (1-dimension)
                in the feature data X (e.g SOCN) then create a new PLSReg model with the n_components
                parameter set to 1 instead of the default 2 - this stops the error:
                'ValueError - Invalid Number of Components: 2.'
                '''

                #get train/test split, fit model and predict activity of test data
                if (X.shape[1] == 1 and self.algorithm.lower() == "plsregression"):
                  tmp_model = Model(X, Y, self.algorithm, parameters={'n_components':1})
                  X_train, X_test, Y_train, Y_test = tmp_model.train_test_split(X, Y, self.model_parameters, self.test_split)
                  model_fit = tmp_model.fit()
                  Y_pred = tmp_model.predict()
                else:
                  tmp_model = Model(X, Y, self.algorithm, self.model_parameters, self.test_split)  
                  X_train, X_test, Y_train, Y_test = tmp_model.train_test_split()
                  model_fit = tmp_model.fit()
                  Y_pred = tmp_model.predict()

                #create instance of Evaluate class
                eval = Evaluate(Y_test, Y_pred)

                #append values/results from current encoding iteration to lists
                index_.append(index)
                index_category_.append(aaindex1[index]['category'])
                descriptor_.append(descr)
                r2_.append(eval.r2)
                rmse_.append(eval.rmse)
                mse_.append(eval.mse)
                rpd_.append(eval.rpd)
                mae_.append(eval.mae)
                explained_var_.append(eval.explained_var)

        #stop counter and calculate elapsed time
        end = time.time()           
        elapsed = end - start

        print('Elapsed time for AAI + Descriptor Encoding: {0:.2f} seconds.'.format(elapsed))
        print('\n###########################################################################')

        #if using combinations of 2 or 3 descriptors, group every 2 or 3 descriptor
        #groups into one element in the descriptor group list
        if (desc_combo == 2):
          descriptor_group_= [ ','.join(x) for x in zip(descriptor_group_[0::2],
            descriptor_group_[1::2]) ]
        elif (desc_combo == 3):
          descriptor_group_= [ ','.join(x) for x in zip(descriptor_group_[0::3],
            descriptor_group_[1::3],  descriptor_group_[2::3]) ]

        #set columns in the output dataframe to each of the values/metrics lists
        aai_desc_metrics_df_= aai_desc_metrics_df.copy()
        aai_desc_metrics_df_['Index'] = index_
        aai_desc_metrics_df_['Category'] = index_category_
        aai_desc_metrics_df_['Descriptor'] = descriptor_
        aai_desc_metrics_df_['Group'] = descriptor_group_
        aai_desc_metrics_df_['R2'] = r2_
        aai_desc_metrics_df_['RMSE'] = rmse_
        aai_desc_metrics_df_['MSE'] = mse_
        aai_desc_metrics_df_['RPD'] = rpd_
        aai_desc_metrics_df_['MAE'] = mae_
        aai_desc_metrics_df_['Explained Variance'] = explained_var_

        #convert index, category, descriptor and group columns from default Object -> string datatype
        aai_desc_metrics_df_['Index'] = aai_desc_metrics_df_['Index'].astype(pd.StringDtype())
        aai_desc_metrics_df_['Category'] = aai_desc_metrics_df_['Category'].astype(pd.StringDtype())
        aai_desc_metrics_df_['Descriptor'] = aai_desc_metrics_df_['Descriptor'].astype(pd.StringDtype())
        aai_desc_metrics_df_['Group'] = aai_desc_metrics_df_['Group'].astype(pd.StringDtype())

        #sort output dataframe by sort_by parameter, sorted by R2 by default
        if (sort_by not in aai_desc_metrics_df_.columns):
            sort_by = 'R2'

        #sort ascending or descending depending on sort_by metric
        sort_ascending = False
        if not (sort_by == "R2" or sort_by == "Explained Variance"):
            sort_ascending = True

        #sort results according to sort_by parameter (R2 by default)
        aai_desc_metrics_df_ = aai_desc_metrics_df_.sort_values(by=[sort_by], ascending=sort_ascending)

        #set save filename according to the descriptor combinations type
        if (desc_combo == 2):
            save_filename = 'aai_desc_combo2_results'
        elif (desc_combo == 3):
            save_filename = 'aai_desc_combo3_results'
        else:
            save_filename = 'aai_desc_results'

        #save results dataframe to specified save_filename
        save_results(aai_desc_metrics_df_, save_filename, output_folder=output_folder)

        return aai_desc_metrics_df_

    def __str__(self):
        return "Instance of Encoding Class with attribute values: Configuration File: {}, Dataset: {},\
            Target Activity: {}, Algorithm: {}, Model Parameters: {}, Test Split: {}.".format(
                os.path.basename(self.config_file), os.path.basename(self.dataset), self.activity,self.algorithm, self.model_parameters, self.test_split)

    def __repr__(self):
        return "<{}>".format(self)