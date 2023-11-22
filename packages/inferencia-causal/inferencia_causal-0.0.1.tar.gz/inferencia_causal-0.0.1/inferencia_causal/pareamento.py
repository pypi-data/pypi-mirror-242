import pandas as pd
import numpy as np

class Match:
    """Faz o pareamentos do grupo controle.
    
    O retorno e um DataFrame contendo o indice do grupo estudo e o correspontende do grupo controle.  
    
    Parameters
    ----------
    data : DataFrame.
    groups :'study = 1 e Control = 2'
    pscore: 'propensity score'
    .
    .
    .
    """
    
    def __init__(self, data, groups, pscore):
        self.data = data
        self.groups = groups
        self.pscore = pscore
     
                  
    def fit (self, error=0.05 ,replacement= False):
        """Realiza o Matcher.
        .
        .
        .
        Parameters
        ----------
        error : 
        replacement :
        pscore:
        .
        .
        .
        """
        study_n = self.data[self.groups].sum()
        ctrl_n = len(self.data[self.groups]) - study_n

        study_scores = self.data.loc[lambda f:f[self.groups] == 1][self.pscore]
        ctrl_scores = self.data.loc[lambda f:f[self.groups] == 0][self.pscore]   

        match = pd.Series(np.empty(study_n))
        match[:] = np.NAN

        # makes the study group random
        study_r = np.random.permutation(study_n)

        for i in study_r:
            dist = abs(study_scores.iloc[i] - ctrl_scores)
            if dist.min() <= error:
                match[i] = dist.idxmin()
                if replacement:
                    continue
                ctrl_scores = ctrl_scores.drop(match[i])

        match= match[match.notnull()]    
        study = pd.DataFrame(study_scores).reset_index()
        study.columns = ['study_indx', 'study_pscore']
        control = pd.DataFrame(self.data.iloc[match][self.pscore]).reset_index()
        control.columns = ['ctl_indx', 'ctl_pscore']

        final_df = study.join(control)
        print(f'Pareamentos concluido! \
        \nFoi possivel parear {round(len(match)/study_n,4)*100}% do grupo estudo com o grupo controle!')

        return final_df 