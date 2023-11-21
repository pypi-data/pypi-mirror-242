import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import MultiComparison
from statsmodels.stats.anova import AnovaRM
from statsmodels import api
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns 
import numpy as np
import re as repattern

LINE = "|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"

class Stat_Manager:
    def __init__(self, dataframe: pd.DataFrame, id: str = None):
        self.df = dataframe
        self.filtered_df = None
        self.result = None
        self.selector = None
        self.link = '*****\n↓↓ 상세한 정보는 Documentation link를 확인하세요! ↓↓\nhttps://cslee145.notion.site/statmanager-kr-Documentation-c9d0886f29ea461d9d0f44449a145f8a?pvs=4 \n*****\n'
        
        self.menu_for_howtouse = {
            '목적': {'Kolmogorov-Smirnov Test': '정규성 검정',
                   'Shapiro-Wilks Test': '정규성 검정',
                   'z-skeweness & z-kurtosis test': '정규성 검정',
                   'Levene Test': '등분산성 검정',
                   'F-max Test': '등분산성 검정',
                   'Chi-Square Test': '빈도분석',
                   "Fisher's Exact Test": '빈도분석',
                   '상관분석: Pearson r': '상관분석-모수검정',
                   '상관분석: Spearman rho': '상관분석-비모수검정',
                   "상관분석: Kendall's tau-b": '상관분석-비모수검정',
                   'Indenpendent Samples T-test': '차이비교 (2집단)-모수검정',
                   'Dependent Samples T-test': '차이비교 (집단 내 2시점)-모수검정',
                   'Mann-Whitney U Test': '차이비교 (2집단)-비모수검정',
                   'Brunner-Munzel Test': '차이비교 (2집단)-비모수검정',
                   'Wilcoxon-Signed Ranksum Test': '차이비교 (집단 내 2시점)-비모수검정',
                   'Bootstrap Resampling (Resampling NO. = 1,000)': '데이터프레임 반환',
                   'Bootstrap Resampling (Resampling NO. = 10,000)': '데이터프레임 반환',
                   'Bootstrap percentile method: Resampling No. = 1,000': '차이비교 (2집단 or 2시점)',
                   'Bootstrap percentile method: Resampling No. = 10,000': '차이비교 (2집단 or 2시점)',
                   'One-way ANOVA': '차이비교 (3집단 이상)-모수검정',
                   'One-way Repeated Measures ANOVA': '차이비교 (집단 내 3시점 이상)-모수검정',
                   'Kruskal-Wallis Test': '차이비교 (3집단 이상)-비모수검정',
                   'Friedman Test': '차이비교 (집단 내 3시점 이상)-비모수검정',
                   'N-way ANOVA': '차이비교-모수검정',
                   'N-way Repeated Measures ANOVA': '차이비교-모수검정',
                   'Linear Regression': '회귀분석',
                   'Logistic Regression': '회귀분석'},
            'method': {'Kolmogorov-Smirnov Test': 'kstest',
                       'Shapiro-Wilks Test': 'shapiro',
                       'z-skeweness & z-kurtosis test': 'z_normal',
                       'Levene Test': 'levene',
                       'F-max Test': 'fmax',
                       'Chi-Square Test': 'chi2_contingency',
                       "Fisher's Exact Test": 'fisher',
                       '상관분석: Pearson r': 'pearsonr',
                       '상관분석: Spearman rho': 'spearmanr',
                       "상관분석: Kendall's tau-b": 'kendallt',
                       'Indenpendent Samples T-test': 'ttest_ind',
                       'Dependent Samples T-test': 'ttest_rel',
                       'Mann-Whitney U Test': 'mannwhitneyu',
                       'Brunner-Munzel Test': 'brunner',
                       'Wilcoxon-Signed Ranksum Test': 'wilcoxon',
                       'Bootstrap Resampling (Resampling NO. = 1,000)': 'bootstrap1000_df',
                       'Bootstrap Resampling (Resampling NO. = 10,000)': 'bootstrap10000_df',
                       'Bootstrap percentile method: Resampling No. = 1,000': 'bootstrap1000',
                       'Bootstrap percentile method: Resampling No. = 10,000': 'bootstrap10000',
                       'One-way ANOVA': 'f_oneway',
                       'One-way Repeated Measures ANOVA': 'f_oneway_rm',
                       'Kruskal-Wallis Test': 'kruskal',
                       'Friedman Test': 'friedman',
                       'N-way ANOVA': 'f_nway',
                       'N-way Repeated Measures ANOVA': 'f_nway_rm',
                       'Linear Regression': 'linearr',
                       'Logistic Regression': 'logisticr'},
            'vars': {'Kolmogorov-Smirnov Test': '정규성을 검정할 변수 (str)',
                     'Shapiro-Wilks Test': '정규성을 검정할 변수 (str)',
                     'z-skeweness & z-kurtosis test': '정규성을 검정할 변수 (str)',
                     'Levene Test': '등분산성을 검정할 변수 (str)',
                     'F-max Test': '등분산성을 검정할 변수 (str)',
                     'Chi-Square Test': '빈도차이를 확인할 변수들 (list)',
                     "Fisher's Exact Test": '빈도차이를 확인할 변수들 (list)',
                     '상관분석: Pearson r': '상관관계를 확인할 변수들 (list)',
                     '상관분석: Spearman rho': '상관관계를 확인할 변수들 (list)',
                     "상관분석: Kendall's tau-b": '상관관계를 확인할 변수들 (list)',
                     'Indenpendent Samples T-test': '차이를 확인할 변수 (str)',
                     'Dependent Samples T-test': '차이를 확인할 변수들 (list)',
                     'Mann-Whitney U Test': '차이를 확인할 변수 (str)',
                     'Brunner-Munzel Test': '차이를 확인할 변수 (str)',
                     'Wilcoxon-Signed Ranksum Test': '차이를 확인할 변수들 (list)',
                     'Bootstrap Resampling (Resampling NO. = 1,000)': '리샘플링을 실시할 변수 (str) 혹은 샘플링을 실시할 변수들 (list)',
                     'Bootstrap Resampling (Resampling NO. = 10,000)': '리샘플링을 실시할 변수 (str) 혹은 샘플링을 실시할 변수들 (list)',
                     'Bootstrap percentile method: Resampling No. = 1,000': '리샘플링을 실시할 변수 (str) 혹은 샘플링을 실시할 변수들 (list)',
                     'Bootstrap percentile method: Resampling No. = 10,000': '리샘플링을 실시할 변수 (str) 혹은 샘플링을 실시할 변수들 (list)',
                     'One-way ANOVA': '차이를 확인할 변수 (str)',
                     'One-way Repeated Measures ANOVA': '차이를 확인할 변수들 (list)',
                     'Kruskal-Wallis Test': '차이를 확인할 변수 (str)',
                     'Friedman Test': '차이를 확인할 변수들 (list)',
                     'N-way ANOVA': '차이를 확인할 변수 (str)',
                     'N-way Repeated Measures ANOVA': '차이를 확인할 변수들 (list)',
                     'Linear Regression': "['종속변수', ['독립변수1', '독립변수2', ...., ] ]",
                     'Logistic Regression': "['종속변수', ['독립변수1', '독립변수2', ...., ] ]"},
            'group_vars': {'Kolmogorov-Smirnov Test': np.nan,
                           'Shapiro-Wilks Test': np.nan,
                           'z-skeweness & z-kurtosis test': np.nan,
                           'Levene Test': '기준이 될 집단 변수 (str)',
                           'F-max Test': '기준이 될 집단 변수 (str)',
                           'Chi-Square Test': np.nan,
                           "Fisher's Exact Test": np.nan,
                           '상관분석: Pearson r': np.nan,
                           '상관분석: Spearman rho': np.nan,
                           "상관분석: Kendall's tau-b": np.nan,
                           'Indenpendent Samples T-test': '기준이 될 집단 변수 (str)',
                           'Dependent Samples T-test': np.nan,
                           'Mann-Whitney U Test': '기준이 될 집단 변수 (str)',
                           'Brunner-Munzel Test': '기준이 될 집단 변수 (str)',
                           'Wilcoxon-Signed Ranksum Test': np.nan,
                           'Bootstrap Resampling (Resampling NO. = 1,000)': '리샘플링의 기준이 될 집단 변수 혹은 생략',
                           'Bootstrap Resampling (Resampling NO. = 10,000)': '리샘플링의 기준이 될 집단 변수 혹은 생략',
                           'Bootstrap percentile method: Resampling No. = 1,000': '리샘플링의 기준이 될 집단 변수 혹은 생략',
                           'Bootstrap percentile method: Resampling No. = 10,000': '리샘플링의 기준이 될 집단 변수 혹은 생략',
                           'One-way ANOVA': '기준이 될 집단 변수 (str)',
                           'One-way Repeated Measures ANOVA': np.nan,
                           'Kruskal-Wallis Test': '기준이 될 집단 변수 (str)',
                           'Friedman Test': np.nan,
                           'N-way ANOVA': '기준이 될 집단 변수들 (list)',
                           'N-way Repeated Measures ANOVA': '기준이 될 집단 변수들 (list)',
                           'Linear Regression': np.nan,
                           'Logistic Regression': np.nan},
            'posthoc': {'Kolmogorov-Smirnov Test': np.nan,
                        'Shapiro-Wilks Test': np.nan,
                        'z-skeweness & z-kurtosis test': np.nan,
                        'Levene Test': np.nan,
                        'F-max Test': np.nan,
                        'Chi-Square Test': np.nan,
                        "Fisher's Exact Test": np.nan,
                        '상관분석: Pearson r': np.nan,
                        '상관분석: Spearman rho': np.nan,
                        "상관분석: Kendall's tau-b": np.nan,
                        'Indenpendent Samples T-test': np.nan,
                        'Dependent Samples T-test': np.nan,
                        'Mann-Whitney U Test': np.nan,
                        'Brunner-Munzel Test': np.nan,
                        'Wilcoxon-Signed Ranksum Test': np.nan,
                        'Bootstrap Resampling (Resampling NO. = 1,000)': np.nan,
                        'Bootstrap Resampling (Resampling NO. = 10,000)': np.nan,
                        'Bootstrap percentile method: Resampling No. = 1,000': np.nan,
                        'Bootstrap percentile method: Resampling No. = 10,000': np.nan,
                        'One-way ANOVA': 'True: posthoc 진행',
                        'One-way Repeated Measures ANOVA': 'True: posthoc 진행',
                        'Kruskal-Wallis Test': 'True: posthoc 진행',
                        'Friedman Test': 'True: posthoc 진행',
                        'N-way ANOVA': 'True: posthoc 진행',
                        'N-way Repeated Measures ANOVA': 'True: posthoc 진행',
                        'Linear Regression': np.nan,
                        'Logistic Regression': np.nan}}
        self.menu_for_howtouse = pd.DataFrame(self.menu_for_howtouse)
        self.menu_for_howtouse.reset_index(inplace = True)
        self.menu_for_howtouse.rename(columns = {'index' : '분석명'}, inplace=True)
        
        self.selector_for_howtouse = {
            'python 식': {
                0: 'if a == b:',
                1: 'if a != b:',
                2: 'if a > b:',
                3: 'if a >= b:',
                4: 'if a < b:',
                5: 'if a <= b:'
                },
            '의미': {
                0: 'a가 b인 데이터만',
                1: 'a가 b가 아닌 데이터만',
                2: 'a가 b 초과인 데이터만',
                3: 'a가 b 이상인 데이터만',
                4: 'a가 b 미만인 데이터만',
                5: 'a가 b 이하인 데이터만'
                },
            'selector 인자 형식': {
                0: "{'a' : 'b'}",
                1: "{'a' : {'!=', 'b'} }",
                2: "{'a' : {'>', 'b'} }",
                3: "{'a' : {'>=', 'b'} }",
                4: "{'a' : {'<', 'b'} }",
                5: "{'a' : {'<=', 'b'} }"
                },
            'pandas 식': {
                0: "df.loc['a' == 'b']",
                1: "df.loc['a' != 'b']",
                2: "df.loc['a' > 'b']",
                3: "df.loc['a' >= 'b']",
                4: "df.loc['a' < 'b']",
                5: "df.loc['a' <= 'b']"
                }
            }
        self.selector_for_howtouse = pd.DataFrame(self.selector_for_howtouse)
        self.selector_for_howtouse.set_index('python 식', inplace=True)
        
        
        self.notation = '.howtouse()에 분석과 관련해 검색할 키워드를 입력하세요.\n\n예시 1. ANOVA의 적용 방법이 궁금한 경우 sm.howtouse("ANOVA")\n예시 2. 정규성 검정이 궁금한 경우 sm.howtouse("정규성")\n예시 3. 비모수 검정이 궁금한 경우 sm.howtouse("비모수")\n\n데이터 필터링 방법을 확인하고 싶다면 sm.howtouse("selector")를 입력하세요! \n\n아래 표는 statmanager-kr에 구현된 통계분석 방법별로 구현 방법을 요약한 것입니다. '
        
        
        
        if self.df.index.name == None:
            self.df.set_index(id, inplace=True)
        
        else:
            pass
        
        self.id_var = self.df.index.name

        self.menu = {
        'kstest' : {
            'name' : 'Kolmogorov-Smirnov Test',
            'type' : '정규성',
            'group' : 1,
            'testfunc' : stats.kstest,
            'division' : None,
        },
        
        'shapiro' : {
            'name' : 'Shapiro-Wilks Test',
            'type' : '정규성',
            'group' : 1,
            'testfunc' : stats.shapiro,
            'division' : None,
        },
        
        'levene' : {
            'name' : 'Levene Test',
            'type' : '등분산성',
            'group' : 2,
            'testfunc' : stats.levene,
            'division' : None,
        },
        
        'ttest_ind' : {
            'name' : 'Indenpendent Samples T-test',
            'type' : '차이비교_집단간',
            'group' : 2,
            'testfunc' : stats.ttest_ind,
            'division' : '모수'
        },
        
        'ttest_rel' : {
            'name' : 'Dependent Samples T-test',
            'type' : '차이비교_집단내',
            'group' : 1,
            'testfunc' : stats.ttest_rel,
            'division' : '모수'
        },
        
        'mannwhitneyu' : {
            'name' : 'Mann-Whitney U Test',
            'type' : '차이비교_집단간',
            'group' : 2,
            'testfunc' : stats.mannwhitneyu,
            'division' : '비모수'
        },
        'brunner' :{
            'name' : 'Brunner-Munzel Test',
            'type' : '차이비교_집단간',
            'group' : 2,
            'testfunc' : stats.brunnermunzel,
            'division' : '비모수'
        },        
        
        'wilcoxon' : {
            'name' : 'Wilcoxon-Signed Ranksum Test',
            'type' : '차이비교_집단내',
            'group' : 1,
            'testfunc' : stats.wilcoxon,
            'division' : '비모수'        
        },
        
        
        'f_oneway' : {
            'name' : 'One-way ANOVA',
            'type' : '차이비교_집단간',
            'group' : 3,
            'testfunc' : stats.f_oneway,
            'division' : '모수'
            
        },
        
        'kruskal' : {
            'name' : 'Kruskal-Wallis Test',
            'type' : '차이비교_집단간',
            'group' : 3,
            'testfunc' : stats.kruskal,
            'division' : '비모수'
            
        },
        
        'chi2_contingency' : {
            'name' : 'Chi-Square Test',
            'type' : '빈도분석',
            'group': 1,
            'testfunc' : stats.chi2_contingency,
            'division' : None
            },
        'fisher' : {
            'name' : "Fisher's Exact Test",
            'type' : '빈도분석',
            'group' : 1,
            'testfunc' : stats.fisher_exact,
            'division' : None
        },
        
        'z_normal' : {
            'name' : 'z-skeweness & z-kurtosis test',
            'type' : '정규성_예외',
            'group' : 1,
            'testfunc' : self.zscore_normality,
            'division' : None
            },
        
        'fmax' : {
            'name' : 'F-max Test',
            'type' : '등분산성_예외',
            'group' : 2,
            'testfunc' : self.fmax_test,
            'division' : None,
            },
        
        'pearsonr' : {
            'name' : '상관분석: Pearson r',
            'type' : '상관분석',
            'group' : 1,
            'testfunc' : self.r_forargs,
            'division' : None,
        },
        
        'spearmanr' : {
            'name' : '상관분석: Spearman rho',
            'type' : '상관분석',
            'group' : 1,
            'testfunc' : self.r_forargs,
            'division' : None,
        },
        'kendallt' : {
          'name' : "상관분석: Kendall's tau-b",
          'type' : '상관분석',
          'group' : 1,
          'testfunc' : self.r_forargs,
          'division' : None,   
        },
        'friedman' : {
            'name' : 'Friedman Test',
            'type' : '차이비교_집단내',
            'group' : 1,
            'testfunc' : stats.friedmanchisquare,
            'division' : '비모수'
        },
        'f_oneway_rm' : {
            'name' : 'One-way Repeated Measures ANOVA',
            'type' : '차이비교_집단내',
            'group' : 1,
            'testfunc' : AnovaRM,
            'division' : '모수'
        },
        'bootstrap1000' : {
            'name' : 'Bootstrap percentile method: Resampling No. = 1,000',
            'type' : '차이비교_예외',
            'group' : 1,
            'testfunc' : self.percentile_method,
            'division' : None,
        },
        'bootstrap10000' : {
            'name' : 'Bootstrap percentile method: Resampling No. = 10,000',
            'type' : '차이비교_예외',
            'group' : 1,
            'testfunc' : self.percentile_method,
            'division' : None,
        },
        'bootstrap1000_df' : {
            'name' : 'Bootstrap dataframe returning (Resampling NO. = 1,000)',
            'type' : '데이터반환',
            'group' : 1,
            'testfunc' : self.bootstrap_to_dataframe,
            'division' : None,
        },
        'bootstrap10000_df' : {
            'name' : 'Bootstrap dataframe returning (Resampling NO. = 10,000)',
            'type' : '데이터반환',
            'group' : 1,
            'testfunc' : self.bootstrap_to_dataframe,
            'division' : None,
        },
        'linearr' : {
            'name' : 'Linear Regression',
            'type' : '회귀',
            'group' : 1,
            'testfunc' : api.OLS,
            'division' : None,
        },
        'logisticr' : {
            'name' : 'Logistic Regression',
            'type' : '회귀',
            'group' : 1,
            'testfunc' : api.Logit,
            'division' : None
        },
        'f_nway' : {
            'name' : "-way ANOVA",
            'type' : '차이비교_WAYS',
            'group' : 2,
            'testfunc' : ols,
            'division' : '모수'
        },
        'f_nway_rm' : {
            'name' : "-way Repeated Measures ANOVA",
            'type' : '차이비교_WAYS',
            'group' : 2,
            'testfunc' : ols,
            'division' : '모수'
        }
    }
        
    def progress(self, method: str, vars: list, group_vars: str = None, group_names: list = None, effectsize: bool = False, posthoc: bool = False, posthoc_method: str = 'bonf', selector: dict = None):
        """
        Args:
            method (str): 적용할 분석 방법을 입력하십시오. 
            vars (list): 분석을 적용할 변수
            group_vars (str, optional): 집단 변수가 요구되는 분석에 한하여, 집단으로 삼을 변수
            group_names (list, optional): 집단으로 삼을 변수 중 일부 집단만 한정하고자 하는 경우, 한정할 변수들입니다.
            effectsize (bool, optional): True 시 효과크기가 함께 출력됩니다. 
            posthoc (bool, optional): True 시 post-hoc이 실시되어 결과가 출력됩니다. 
            posthoc_method (str, optional): post-hoc 방법을 지정합니다. 기본적으로 bonferroni correction이 적용됩니다 (posthoc_method = 'bonf'). Tukey HSD 방법을 사용하고자 하는 경우 'tukey'를 적용하십시오. 
            selector (dict, optional): 데이터 필터링을 진행하고자 하는 경우 인자를 제공하십시오. 구체적인 내용은 documentation을 참고하시기 바랍니다. 

        display:
            분석 결과가 출력됩니다. 
        """
        
        testtype = self.menu[method]['type']
        
        if selector == None:
            self.selector = None
            df = self.df
            self.filtered_df = None          
            
        else:
            df = self.df
            self.selector = selector
            self.filtered_df = None 
            conditions  = []
            conditions_notification = []
            for key, value in selector.items():
                if isinstance(value, dict):  # 만약 값이 dictionary 형태라면 비교 연산자를 적용
                    for op, op_value in value.items():
                        if op == '<=':
                            conditions.append(df[key] <= op_value)
                            conditions_notification.append(f"{key} <= {op_value}")
                        elif op == '>=':
                            conditions.append(df[key] >= op_value)
                            conditions_notification.append(f"{key} >= {op_value}")
                        elif op == '<':
                            conditions.append(df[key] < op_value)
                            conditions_notification.append(f"{key} < {op_value}")
                        elif op == '>':
                            conditions.append(df[key] > op_value)
                            conditions_notification.append(f"{key} > {op_value}")
                        elif op == '=' or op == '==':
                            conditions.append(df[key] == op_value)
                            conditions_notification.append(f"{key} == {op_value}")
                        elif op == '!=':
                            conditions.append(df[key] != op_value)
                            conditions_notification.append(f"{key} != {op_value}")

                else: #아닌 경우에는 그냥 진행 
                    conditions.append(df[key] == value)
                    conditions_notification.append(f"{key} == {value}")
            
            combined_condition = conditions[0]
            
            if len(conditions) == 1: #selector 하나만 붙인 경우에는 그냥 진행 
                pass
            
            else: # selector가 2개 이상인 경우 
                for cond in conditions[1:]:
                    combined_condition &= cond
                    
            df = df.loc[combined_condition]
            self.filtered_df = df
            conditions_notification_texts = "\n".join(conditions_notification)
            
        if testtype == '회귀':
            df = df.dropna(axis=0, how = 'any', subset = vars[1])
        
        else:
            df = df.dropna(axis=0, how = 'any', subset = vars)
        
        testfunc = self.menu[method]['testfunc']
        group_fill = self.menu[method]['group']
        
        testname = self.menu[method]['name']
        if selector != None:
            testname = f"*****\nNote: 아래 조건에 부합하는 데이터에 한해서만 분석이 진행됩니다.\n{conditions_notification_texts}\n*****\n\n{testname}"
        
        testdivision = self.menu[method]['division']
        
        n = len(df)
        
        if testtype == '빈도분석':
            
            ser = pd.crosstab(df[vars[0]], df[vars[1]])
            number_of_rows = len(df[vars[0]].unique())
            number_of_columns = len(df[vars[1]].unique())
            number_of_cells = number_of_rows * number_of_columns
            
            try:
                re = testfunc(ser)
                s = re[0]
                p = re[1]
                s = round(s, 3)
                p = round(p, 3)
            
            except:
                print("Error: Fisher's Exact Test는 2 x 2인 경우에만 작동합니다. ")
            
            try: 
                predicted_value = re[3]
                
                values = []
                for row in range(number_of_rows):
                    for columns in range(number_of_columns):
                        value = predicted_value[row][columns]
                        values.append(value)
                
                under_five_values = 0
                for n in values:
                    if n < 5:
                        under_five_values += 1
                        
                percentage_of_under_five_values =  under_five_values / number_of_cells
            except:
                pass
            
            
            print(LINE)
            print(f"{testname}")
            print(f"변수 : {vars[0]}, {vars[1]}")
            
            try:
                print(f"\n검정통계치 χ² = {s:.3f}, p = {p:.3f}\n")
                print("Crosstab : ")
            except:
                pass
            
            
            self.showing(ser)
            
            try:
                print(f"기대빈도 5 미만의 cell이 차지하는 비율: {round(percentage_of_under_five_values * 100, 2):.2f}%")
                
                if percentage_of_under_five_values >= 0.25:
                    print("Warning: 기대빈도 5미만의 cell이 차지하는 비율이 25% 이상입니다. Fisher's Exact Test 수행을 권고합니다. .progress(method = 'fisher')")
            except:
                pass
            
            print(LINE)
            
        if testtype == '정규성':
            
            if type(vars) == list:
                dv = vars[0]
            elif type(vars) == str:
                dv = vars
            
            ser = df[dv]
            print(LINE)
            print(f"{testname}")
            
            if method == 'kstest':
                s, p = testfunc(ser, 'norm')
                
                if n < 30:
                    print("주의: 표본 수가 30보다 적습니다. 다른 분석을 고려하십시오. ")
                
            else:
                s, p = testfunc(ser)
                
                if n >= 30:
                    print("주의: 표본 수가 30보다 많습니다. 다른 분석을 고려하십시오.")
            
            
            s = round(s, 3)
            p = round(p, 3)
            
            print(f"변수 : {dv}")
            print(f"n = {n}\n")
            print(f"검정통계치 = {s:.3f}, p = {p:.3f}\n결론: ")
            
            if p <= .05 : 
                print("정규성 가정 미충족")
                
            else:
                print('정규성 가정 충족')
            print(LINE)
        
        if testtype == '등분산성':
            if type(vars) == list:
                dv = vars[0]
            elif type(vars) == str:
                dv = vars
            
            if group_names == None:
                group_names = list(df[group_vars].unique())
            
            
            series = []
            for n in range(len(group_names)):
                ser = df.loc[df[group_vars] == group_names[n], dv]
                series.append(ser)
            
            s, p = testfunc(*series)
            s = round(s, 3)
            p = round(p, 3)
            
            print(LINE)
            print(f"{testname}")
            print(f"집단변수 : {group_vars}")
            print(f"비교집단 : {group_names}\n")
            print(f"검정통계치 = {s:.3f}, p = {p:.3f}\n결론: ")
            
            if p <= .05 :
                print('등분산성 가정 미충족')
            else:
                print('등분산성 가정 충족')
            print(LINE)
            
        if testtype == '차이비교_집단내':
            
            if method == 'friedman' or method == 'f_oneway_rm':
                series = []
                
                for n in range(len(vars)):
                    ser = df[vars[n]]
                    series.append(ser)

                dict_var = {}
                
                for n in range(len(vars)):
                    dict_var[vars[n]] = {
                        'n' : "{:.2f}".format(series[n].count()), 
                        'mean' : "{:.2f}".format(series[n].mean().round(2)),
                        'median' : "{:.2f}".format(series[n].median().round(2)),
                        'sd' : "{:.2f}".format(series[n].std().round(2)),                        
                    }
                dict_var = pd.DataFrame(dict_var)
                print(LINE)
                print(f"{testname}")
                print(f"변수 : {vars}, 시점 = {len(vars)}")
                print("기술통계치: ")
                print(f"변수별 기술통계치: \n")
                self.showing(dict_var)
                
                if method == 'friedman':
                    s, p = testfunc(*series)
                    s = round(s, 3)
                    p = round(p, 3)
                    print(f"검정통계치 = {s:.3f}, p = {p:.3f}")
                
                elif method == 'f_oneway_rm':
                    reset_df = df.reset_index().melt(id_vars= self.id_var, value_vars = vars)
                    result = AnovaRM(data = reset_df, depvar = 'value', subject = self.id_var, within = ['variable']).fit()
                    s = result.anova_table['F Value']
                    p = result.anova_table['Pr > F']
                    s = round(s, 3)
                    p = round(p, 3)

                    for f, s, p in zip(result.anova_table.index, s, p):
                        print(f"검정통계치 F = {s:.3f}, p = {p:.3f}")

                if posthoc == True:
                    posthoc_df = df.reset_index().melt(id_vars=self.id_var, value_vars=vars)
                    mc = MultiComparison(posthoc_df['value'], posthoc_df['variable'])
                    print(LINE)
                    print('Posthoc 실시: ')
                    
                    if posthoc_method == 'bonf':
                        if testdivision == '모수':
                            result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
                            self.showing(result[0])
                            print(LINE)
                        
                        else: 
                            result = mc.allpairtest(stats.mannwhitneyu, method = 'bonf')
                            self.showing(result[0])
                            print(LINE)
                        
                    elif posthoc_method == 'tukey':
                        result = mc.tukeyhsd()
                        print(result)
                        print(LINE)
                        
                if effectsize == True:
                    eta, grade = self.calculate_etasquared(series)
                    print("효과크기 계산: \n")
                    print(f"Eta-Sqaured (η2) =  {eta:.2f}\n수준 : {grade}")
            
            else:
                series = []
                for n in range(len(vars)):
                    ser = df[vars[n]]
                    series.append(ser)
                
                dict_var = {}
                for n in range(len(vars)):
                    dict_var[vars[n]] = {
                        'mean' : series[n].mean().round(2),
                        'median' : series[n].median().round(2),
                        'sd' : series[n].std().round(2),                        
                    }
                
                dict_var = pd.DataFrame(dict_var)
                
                s, p = testfunc(*series)
                s = round(s, 3)
                p = round(p, 3)
                degree_of_freedom = len(df) - 1
                
                n = len(df)
                print(LINE)
                print(f"{testname}")
                print(f"변수 : {vars[0]}, {vars[1]}")
                print(f"n = {n}\n")
                print('기술통계치: ')
                self.showing(dict_var)
                
                print(f"\n검정통계치 = {s:.3f}, df(자유도) = {degree_of_freedom}, p = {p:.3f}\n")
                if method == 'wilcoxon':
                    z = (s - n * (n + 1) / 4) / (n * (n + 1) * (2 * n + 1) / 24)**0.5
                    print(f"z-statistic = {z:.3f}\n")
                
                if effectsize == True:
                    cohen_d, grade = self.calculate_cohen(series)
                    print(f"Cohen's d = {cohen_d:.2f}\n수준 : {grade}")
                
        if testtype == '차이비교_WAYS' :
            
            if method == 'f_nway_rm':
                
                melted_df = df.reset_index().melt(id_vars = self.id_var, value_vars = vars, var_name = 'time').set_index(self.id_var)
                df = df.drop(columns = vars).merge(melted_df, how = 'outer', on = self.id_var)
                
                if type(group_vars) == str:
                    group_vars = [group_vars]
                
                elif type(group_vars) == list:
                    pass
                
                group_vars.append('time')
                dv = 'value'
                
                way_len = len(group_vars)
                new_testname = f'{way_len}-way Repeated Measures ANOVA'
                
                if self.selector == None:
                    testname = new_testname
                
                else:
                    pattern = repattern.compile('-way Repeated Measures ANOVA')
                    new_testname = pattern.sub(new_testname, testname)
                    testname = new_testname
                
                df, interaction_columns = self.create_interaction_columns(df, group_vars)
                
                print(LINE)
                print(f"{testname}\n")
                print(f"종속변수 : {vars} ")
                print(f"독립변인 : {group_vars}")
                print("기술통계치: \n")
                
                for n in group_vars:
                    result_table = df.groupby(n)[dv].agg(['count', 'mean', 'median', 'std']).rename(columns = {'count' : "n"}).round(2)
                    print(f"{n} 기준 {dv}")
                    self.showing(result_table)
                    
                for n in interaction_columns:
                    result_table = df.groupby(n)[dv].agg(['count', 'mean', 'median', 'std']).rename(columns = {'count' : "n"}).round(2)
                    print(f"{n} 기준 {dv}")
                    self.showing(result_table)
                    
                iv_str = self.custom_join(group_vars)
                method_str = f"{dv} ~ {iv_str}"
                
                model = testfunc(method_str, data = df).fit()
                table = api.stats.anova_lm(model)
                
                result = table
                result.rename(columns = {'PR(>F)': 'p-value'}, inplace=True)
                

                
                print(f"{testname} 검정통계치:\n")
                if effectsize == True:
                    result['eta_squared'] = result['sum_sq'] / result['sum_sq']['Residual']
                    print("Effectsize가 함께 계산됩니다: ")
                result = result.round(3)
                self.showing(result)
                print(LINE)
                
            elif method == 'f_nway': 
                df, interaction_columns = self.create_interaction_columns(df, group_vars)
                
                if type(vars) == list:
                    dv = vars[0]
                elif type(vars) == str:
                    dv = vars
                
                
                way_len = len(group_vars)
                new_testname = f'{way_len}-way ANOVA'
                
                if self.selector == None:
                    testname = new_testname
                
                else:
                    pattern = repattern.compile('-way ANOVA')
                    new_testname = pattern.sub(new_testname, testname)
                    testname = new_testname
                
                print(LINE)
                print(f"{testname}\n")
                print(f"종속변수 : {dv}")            
                print(f"독립변인 (요인) : {group_vars}")            
                print("기술통계치: \n")
                
                for n in group_vars:
                    result_table = df.groupby(n)[dv].agg(['count', 'mean', 'median', 'std']).rename(columns = {'count' : "n"}).round(2)
                    print(f"{n} 기준 {dv}")
                    self.showing(result_table)
                    
                for n in interaction_columns:
                    result_table = df.groupby(n)[dv].agg(['count', 'mean', 'median', 'std']).rename(columns = {'count' : "n"}).round(2)
                    print(f"{n} 기준 {dv}")
                    self.showing(result_table)
                    
                iv_str = self.custom_join(group_vars)
                method_str = f"{dv} ~ {iv_str}"
                
                model = testfunc(method_str, data = df).fit()
                table = api.stats.anova_lm(model)
                
                result = table
                result.rename(columns = {'PR(>F)': 'p-value'}, inplace=True)
                

                
                print(f"{testname} 검정통계치:\n")
                
                if effectsize == True:
                    result['eta_squared'] = result['sum_sq'] / result['sum_sq']['Residual']
                    print("Effectsize: Eta-squared (η2) 가 함께 계산됩니다: ")
                    
                result = result.round(3)
                self.showing(result)
                print(LINE)
                
            if posthoc == True:
                print("Post-Hoc 실시:")
                for n in group_vars:
                    mc = MultiComparison(df[dv], df[n])
                    
                    if posthoc_method == 'bonf':
                        result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
                        print(f"\n{n}의 주효과에 대한 사후검정")
                        self.showing(result[0])
                    
                    elif posthoc_method == 'tukey':
                        result = mc.tukeyhsd()                
                        print(f"\n{n}의 주효과에 대한 사후검정")
                        print(f"\n{result}\n")

                for n in interaction_columns:
                    mc = MultiComparison(df[dv], df[n])
                    
                    if posthoc_method == 'bonf':
                        result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
                        print(f"\n{n}에 대한 사후검정")
                        self.showing(result[0])
                    
                    elif posthoc_method == 'tukey':
                        result = mc.tukeyhsd()                
                        print(f"\n{n}에 대한 사후검정")
                        print(f"\n{result}\n")

        if testtype == '차이비교_집단간':
            
            if type(vars) == list:
                dv = vars[0]
                
            elif type(vars) == str:
                dv = vars
            
            if group_names == None:
                group_names = list(df[group_vars].unique())
            
            series = []
            for n in range(len(group_names)):
                ser = df.loc[df[group_vars] == group_names[n], dv]
                series.append(ser)
            
            dict_var = {}
            for n in range(len(group_names)):
                dict_var[group_names[n]] = {
                    'n' : len(series[n]),
                    'mean' : series[n].mean().round(2),
                    'median' : series[n].median().round(2),
                    'sd' : series[n].std().round(2),
                    }
            
            dict_var = pd.DataFrame(dict_var)
            
            s, p = testfunc(*series)
            s = round(s, 3)
            p = round(p, 3)
            print(LINE)
            print(f"{testname}")
            print(f"변수 : {dv}")
            print(f"집단변수 : {group_vars}")
            print(f"비교집단 : {group_names}\n")
            print("기술통계치:")
            self.showing(dict_var)
            print(f"검정통계치 = {s:.3f}, p = {p:.3f}")
            
            if method != 'kruskal' and method != 'f_oneway': #ttest 혹은 mannwhitney, brunner
                degree_of_freedom = 0
                for n in range(len(group_names)):
                    value = series[n].count()
                    degree_of_freedom += value
                
                degree_of_freedom = degree_of_freedom - 2
                print(f"자유도(df) = {degree_of_freedom}")
                
                if method == 'mannwhitneyu':
                    n1 = len(series[0])
                    n2 = len(series[1])
                    z = (s - n1 * n2 / 2) / ((n1 * n2 * (n1 + n2 + 1)) / 12)**0.5
                    print(f"z-statistic = {z:.3f}\n")
                    
                elif method == 'brunner':
                    n1 = len(series[0])
                    n2 = len(series[1])
                    z = s / ((n1 * n2)**0.5)
                    print(f"z-statistic = {z:.3f}\n")
            
            
            else:
                degree_of_freedom_between_group = len(group_names) - 1
                degree_of_freedom = 0
                for n in range(len(group_names)):
                    value = series[n].count()
                    degree_of_freedom += value
                
                degree_of_freedom = degree_of_freedom - len(group_names)
                print(f"집단 간 자유도 = {degree_of_freedom_between_group}, 집단 내 자유도 = {degree_of_freedom}")

            print(LINE)
            
            if posthoc == True:
                
                cond_list = []
                for n in range(len(group_names)):
                    cond = df[group_vars] == group_names[n]
                    cond_list.append(cond)
                
                
                selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
                selected_df = df[selected_rows]
                
                mc = MultiComparison(selected_df[dv], selected_df[group_vars])
                
                if posthoc_method == 'bonf':
                
                    if testdivision == '모수':
                        result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
                    
                    else: 
                        result = mc.allpairtest(stats.mannwhitneyu, method = 'bonf')
                    print('Post-hoc 실시:')
                    self.showing(result[0])
                    print(LINE)
                
                elif posthoc_method == 'tukey':
                    print('Post-hoc 실시:\n')
                    result = mc.tukeyhsd()
                    print(result)
                    print(LINE)
        
            if effectsize == True:
                print("효과크기 계산 : \n")
                
                if method != 'kruskal' and method != 'f_oneway': #ttest 혹은 뭐시기일때
                    
                    cohen_d, grade = self.calculate_cohen(series)
                    print(f"Cohen's d = {cohen_d:.2f}\n수준 : {grade}")
                    
                else:
                    eta, grade = self.calculate_etasquared(series)
                    print(f"Eta-Sqaured (η2) =  {eta:.2f}\n수준 : {grade}")
            
        if testtype == '차이비교_예외':
            
            if method == 'bootstrap1000':
                resampling_no = 1000
                
            elif method == 'bootstrap10000':
                resampling_no = 10000
            
            if group_vars == None:
                print(LINE)
                print(f"{testname}: \n")
                
                ser1 = self.bootstrap(series = df[vars[0]], n_bootstrap=resampling_no)
                ser2 = self.bootstrap(series = df[vars[1]], n_bootstrap=resampling_no)
                bootstrap_df = self.bootstrap_to_dataframe(ser1, ser2, label = vars)
                testfunc(data = bootstrap_df, a_var = vars[0], b_var = vars[1])
                
            else:
                if type(vars) == list:
                    dv = vars[0]
                elif type(vars) == str:
                    dv = vars
                
                
                print(LINE)
                print(f"{testname}: \n")
                
                ser1 = self.bootstrap(series= df.loc[df[group_vars] == group_names[0], dv], n_bootstrap=resampling_no)
                ser2 = self.bootstrap(series= df.loc[df[group_vars] == group_names[1], dv], n_bootstrap=resampling_no)
                a_var = f"{group_names[0]}_{dv}"
                b_var = f"{group_names[1]}_{dv}"
                bootstrap_df = self.bootstrap_to_dataframe(ser1, ser2, label = [a_var, b_var])
                testfunc(data = bootstrap_df, a_var = a_var, b_var = b_var)
        
        if testtype == '데이터반환':
            if method == 'bootstrap1000_df':
                resampling_no = 1000
            
            elif method == 'bootstrap10000_df':
                resampling_no = 10000
            
            print(LINE)
            print(f"{testname}: \n")
                
            if group_vars == None:
                
                ser1 = self.bootstrap(series = df[vars[0]], n_bootstrap=resampling_no)
                ser2 = self.bootstrap(series = df[vars[1]], n_bootstrap=resampling_no)
                bootstrap_df = testfunc(ser1, ser2, label = vars)
            
            else: 
                if type(vars) == list:
                    dv = vars[0]
                elif type(vars) == str:
                    dv = vars
                    
                ser1 = self.bootstrap(series= df.loc[df[group_vars] == group_names[0], dv], n_bootstrap=resampling_no)
                ser2 = self.bootstrap(series= df.loc[df[group_vars] == group_names[1], dv], n_bootstrap=resampling_no)
                a_var = f"{group_names[0]}_{dv}"
                b_var = f"{group_names[1]}_{dv}"
                bootstrap_df = testfunc(ser1, ser2, label = [a_var, b_var])
                
            print("\nbootstrap된 DataFrame이 반환되었습니다.\n특정 변수에 선언한 후 활용하세요.\n")
            
            return bootstrap_df
        
        if testtype == '정규성_예외':
            if type(vars) == list:
                dv = vars[0]
            elif type(vars) == str:
                dv = vars            
            
            
            print(LINE)
            print(f"{testname}")
            print(f"변수: {dv}")
            testfunc(df[dv])
            
        if testtype == '등분산성_예외':
            if type(vars) == list:
                dv = vars[0]
            elif type(vars) == str:
                dv = vars  
            
            if group_names == None:
                group_names = list(df[group_vars].unique())
            
            print(LINE)
            print(f"{testname}")
            print(f"변수: {dv}")
            testfunc(vars = dv, group_vars = group_vars, group_names = group_names)
            
        if testtype == '상관분석':
            print(LINE)
            print(f"{testname}\n")
            testfunc(method = method, vars = vars)
            print(LINE)
    
        if testtype == '회귀':
            dv = vars[0]
            iv = vars[1]
            print(LINE)
            print(f"{testname}")
            
            if method == 'logisticr':
                dv_list = df[dv].astype('category').cat.categories.to_list()
                dv_len = len(dv_list)
                
                mapper = {}
                for number in range(dv_len):
                    mapper[dv_list[number]] = number
                
                dummy_label = f'dummy_{dv}'
                df[dummy_label] = df[dv].map(mapper)
                y = df[dummy_label]
                
                if dv_len >= 3:
                    testfunc = api.MNLogit
                    print("Note: 다항로지스틱회귀(Multinominal Logistic Regression)이 진행됩니다. ")
                
                print(f"\n종속변수: {dv}")
                print(f"dummy_coding 되었습니다 : {mapper}\n")
            
            else:
                y = df[dv]
                print(f"\n종속변수: {dv}")
            
            print(f"독립변수: {iv}\n")

            x = df[iv]
            
            x = api.add_constant(x)
            model = testfunc(y, x).fit()
            
            self.showing(model.summary())
            self.showing(model.summary2())
            
            odd_ratio = np.exp(model.params)
            print('변수별 odds ratio (OR): \n')
            self.showing(odd_ratio)          
            print(LINE)
    
    def zscore_normality(self, series):
        n = series.count()
        
        skewness = series.skew().round(3)
        skewness_se = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3))).round(3)
        
        kurtosis = series.kurtosis().round(3)
        kurtosis_se = (np.sqrt((n**2 - 1) / ((n-3)*(n+5))) * skewness_se * 2).round(3)
        
        z_skewness = (skewness/skewness_se).round(3)
        z_kurtosis = (kurtosis/kurtosis_se).round(3)
        
        if n < 50:
            cutoff = 1.96
        elif n < 200:
            cutoff = 2.59
        elif n > 200:
            cutoff = 3.13
        
        print(f"skewness = {skewness}\nstandard error of skewness = {skewness_se}\nz-skewness = {z_skewness}\n\nkurtosis = {kurtosis}\nstandard error of kurtosis = {kurtosis_se}\nz-kurtosis = {z_kurtosis}\n\nsample n = {n}, corresponding absolute cutoff score of z-skewenss and z-kurtosis = {cutoff}")
        
        z_skewness = abs(z_skewness)
        z_kurtosis = abs(z_kurtosis)
        
        print("\n결론: ")
        if z_skewness < cutoff and z_kurtosis < cutoff:
            print("\n정규성 가정 충족")
        else:
            print("\n정규성 가정 미충족")
            
            
        print("\nReferences:\n[1] Ghasemi, A., & Zahediasl, S. (2012). Normality tests for statistical analysis: a guide for non-statisticians. International journal of endocrinology and metabolism, 10(2), 486. \n[2] Moon, S. (2019). Statistics for the Social Sciences: Moving Toward an Integrated Approach. Cognella Academic Publishing.")
        print(LINE)

    def fmax_test(self, vars, group_vars, group_names):
        
        if self.selector == None:
            df = self.df
        
        else:
            df = self.filtered_df
        
        df = df.loc[df[group_vars].isin(group_names)]
        group_n = len(group_names)
        
        max_variance = df.groupby(group_vars)[vars].var().max().round(3)
        min_variance = df.groupby(group_vars)[vars].var().min().round(3)
        
        f_max = max_variance / min_variance
        f_max = round(f_max, 3)
        
        
        print(f"\n집단 수 = {group_n}")
        print(f"집단 구분 : {group_names}\n")
        print(f"Max variance among group = {max_variance}")
        print(f"Min variance among group = {min_variance}")
        print(f"F-max statistics = {f_max}\n")
        print("\n결론:")
        
        if f_max < 10:
            print("등분산성 가정 충족")
        else:
            print("등분산성 가정 미충족")
            
        print("\nReference:\n[1] Fidell, L. S., & Tabachnick, B. G. (2003). Preparatory data analysis. Handbook of psychology: Research methods in psychology, 2, 115-141.\n")
        print(LINE)
        
    def r_forargs(self, method, vars):
        
        if self.selector == None:
            df = self.df
        
        else:
            df = self.filtered_df
            
        
        df = df.dropna(axis=0, how = 'any', subset = vars)
        number_of_rows = len(df)
        
        statistic_valuedict = {
            'pearsonr' : "Pearson's r",
            'spearmanr' : "Spearman's rho",
            'kendallt' : "Kendall's tau-h"
        }
        
        if method == 'pearsonr':
            tf = stats.pearsonr
        
        elif method == 'spearmanr':
            tf = stats.spearmanr
            
        elif method == 'kendallt':
            tf = stats.kendalltau
        
        correlation_table = df[vars].corr().round(3)
        
        num = len(vars)
        sets = []
        
        statistic_value = statistic_valuedict[method]
        
        print(f'포함된 n수 = {number_of_rows}\nNote: 입력된 모든 변수에서 결측값이 없는 데이터만 포함됩니다.\n')
        summary_correlation_table = pd.DataFrame()
        
        for i in range(num -1):
            for j in range(i +1, num):
                sets.append((df[vars[i]], df[vars[j]]))
            
        for n in sets:
            s, p = tf(n[0], n[1])
            s = round(s, 3)
            p = round(p, 3)
            var1 = n[0].name
            var2 = n[1].name
            
            if p <= .05:
                significant_r = '*'
                s_with_significancy = f'{s:.3f}{significant_r}'
            else:
                significant_r = ''
                s_with_significancy = s
            
            
            
            summary_correlation_table.loc[f"{var1} & {var2}", statistic_value] = s_with_significancy
            summary_correlation_table.loc[f"{var1} & {var2}", 'p-value'] = f"{p:.3f}"
            
            print(f"{var1} & {var2}  :  {statistic_value} = {s:.3f}, p = {p:.3f}{significant_r}")
            
            correlation_table.loc[var1, var2] = s_with_significancy
            correlation_table.loc[var2, var1] = s_with_significancy
            
            # if method != 'pearsonr':
            #     correlation_table.loc[var1, var2] = s
        
        self.showing(correlation_table)
        self.showing(summary_correlation_table)
        print("* p < .05")
            
    def bootstrap(self, series, n_bootstrap=1000, statistic=np.mean):
        
        n = len(series)
        bootstrap_results = []
        for _ in range(n_bootstrap):
            bootstrap_sample = series.sample(n, replace=True)  # 재표집
            statistic_value = statistic(bootstrap_sample)
            bootstrap_results.append(statistic_value)
        
        return bootstrap_results
    
    def bootstrap_to_dataframe(self, *args, label):
        n = len(args)
        dict_var = {}
        for _ in range(n):
            key = f"{_}"
            value = args[_]
            dict_var[key] = value
        result = pd.DataFrame(dict_var)
        
        if label != None and type(label) == list:
            t = len(label)
            for n in range(t):
                result.rename(columns = {f'{n}' : label[n]}, inplace=True)
                
        return result

    def percentile_method(self, data, a_var, b_var, confidence_level = 0.95, hist=True):
        
        confidence_dict = {
            0.90 : [5, 95],
            0.95 : [2.5, 97.5],
            0.99 : [0.5, 99.5],
        }
    
        interval = confidence_dict[confidence_level]
        
        n = len(data)
        
        a_confidence_interval = np.percentile(data[a_var], interval)
        b_confidence_interval = np.percentile(data[b_var], interval)
        a_lower_bound = a_confidence_interval[0]
        a_upper_bound = a_confidence_interval[1]
        b_lower_bound = b_confidence_interval[0]
        b_upper_bound = b_confidence_interval[1]
        
        
        
        print(f"{a_var} 의 {confidence_level * 100:.0f}% 신뢰구간: [{a_lower_bound:.3f}, {a_upper_bound:.3f}]")
        print(f"{b_var} 의 {confidence_level * 100:.0f}% 신뢰구간: [{b_lower_bound:.3f}, {b_upper_bound:.3f}]\n")
        
        
        if a_upper_bound < b_lower_bound or a_lower_bound > b_upper_bound:
            print("두 분포의 신뢰구간이 중복되지 않습니다. \n두 분포 간 차이가 유의합니다.")
        else:
            print("두 분포의 신뢰구간이 중복됩니다. \n두 분포 간 차이가 유의하지 않습니다.")
        
        print("\nReference:\nEfron, B., & Tibshirani, R. (1986). Bootstrap methods for standard errors, confidence intervals, and other measures of statistical accuracy. Statistical Science, 1(1), 54-75.\n")
        print("히스토그램: \n")
        
        
        if hist == True:
            plt.figure(figsize=(10, 8))
            sns.set(font = "Gulim", font_scale = 1.5)
            plt.style.use('grayscale')
            plt.title(f'Histogram of {a_var} & {b_var}')
            sns.histplot(data = data[a_var], label = a_var, alpha=0.5, kde=True)
            sns.histplot(data = data[b_var], label = b_var, alpha=0.5, kde=True)
            
            plt.axvline(a_lower_bound, color='black', linestyle='--', label=f'{confidence_level * 100:.0f}% CI ({a_var})')
            plt.axvline(a_upper_bound, color='black', linestyle='--')
            plt.axvline(b_lower_bound, color='gray', linestyle='--', label=f'{confidence_level * 100:.0f}% CI ({b_var})')
            plt.axvline(b_upper_bound, color='gray', linestyle='--')
                    
            plt.xlabel(f"Value of {a_var} & {b_var}")
            plt.ylabel("No. of Samples")
            plt.legend(bbox_to_anchor=(1, 1))
            plt.grid(False)
            plt.show()
    
    def custom_join(self, vars):
        result = []
    
        for i in range(len(vars)):
            for j in range(i + 1, len(vars)):
                pair = f"{vars[i]}:{vars[j]}"
                result.append(pair)
        
        return ' + '.join(vars + result)
    
    def create_interaction_columns(self, df, elements):
        interactions = []
        new_df = df.copy()  # 원본 DataFrame 복사
        
        for i in range(len(elements)):
            for j in range(i + 1, len(elements)):
                element1 = elements[i]
                element2 = elements[j]
                
                interaction_name = f"interaction_{element1}_{element2}"
                interaction_values = df[element1] + "_" + df[element2]
                
                new_df[interaction_name] = interaction_values
                interactions.append(interaction_name)
        
        return new_df, interactions

    def calculate_cohen(self, series):
        groupa_n = series[0].count()
        groupb_n = series[1].count()
        
        groupa_mean = series[0].mean()
        groupb_mean = series[1].mean()
        
        groupa_std = series[0].std()
        groupb_std = series[1].std()                    
        
        son = groupa_mean - groupb_mean
        
        stage_1 = ((groupa_n - 1) * (groupa_std ** 2)) + ((groupb_n - 1) * (groupb_std ** 2))
        stage_2 = groupa_n + groupb_n - 2
        
        pooled_std = np.sqrt(stage_1/stage_2)
        
        cohen_d = (son / pooled_std)
        
        if cohen_d < 0.2:
            grade = '해석 불가'
        elif cohen_d < 0.5:
            grade = '작은 효과크기'
        elif cohen_d < 0.8:
            grade = '중간 효과크기'
        elif cohen_d >= 0.8:
            grade = '큰 효과크기'
        
        return cohen_d, grade

    def calculate_etasquared(self, series):
        # 그룹 수
        k = len(series)

        # 그룹별 평균 계산
        group_means = [ser.mean() for ser in series]

        # 전체 데이터의 평균 계산
        overall_mean = np.mean(group_means)

        # 그룹 간 변동(SS_Between) 계산
        ss_between = sum([(group_mean - overall_mean) ** 2 * len(ser) for group_mean, ser in zip(group_means, series)])

        # 전체 변동(SS_Total) 계산
        all_data = pd.concat(series)
        ss_total = sum((all_data - overall_mean) ** 2)

        # Eta-squared (\(\eta^2\)) 계산
        eta_squared = ss_between / ss_total

        if eta_squared < 0.06:
            grade = '작은 효과크기'
        elif eta_squared < 0.14:
            grade = '중간 효과크기'
        elif eta_squared >= 0.14:
            grade = '큰 효과크기'

        return eta_squared, grade
    
    def showing(self, result):
        try:
            display(result)
        except:
            print(result)
    
    def howtouse(self, keyword: str = None):
        """statmanager-kr 사용법을 출력합니다. 

        Args:
            keyword (str, optional): 분석 방법에 대해 검색할 키워드를 입력하십시오. 특정한 단어를 입력하지 않는 경우 모든 설명이 출력됩니다. 'selector'를 입력하는 경우 .progress()의 데이터 필터링 파라미터인 selector에 대한 설명이 출력됩니다.  
        """
        print(self.link)
        
        if keyword != None:
            
            if keyword == 'selector':
                self.showing(self.selector_for_howtouse)
            
            else:    
            
                if keyword == '모수' or keyword == '모수검정':
                    cond1 = self.menu_for_howtouse['목적'].str.contains(keyword)
                    cond2 = self.menu_for_howtouse['목적'].str.contains('비모수')
                    
                    self.showing(self.menu_for_howtouse.loc[~cond2 & cond1].set_index('분석명'))
                    
                else:
                    cond1 = self.menu_for_howtouse['목적'].str.contains(keyword)
                    cond2 = self.menu_for_howtouse['method'].str.contains(keyword)
                    cond3 = self.menu_for_howtouse['분석명'].str.contains(keyword)
                    
                    self.showing(self.menu_for_howtouse.loc[cond1 | cond2 | cond3].set_index('분석명'))
            
        else:
            print(self.notation)
            self.showing(self.menu_for_howtouse.set_index('분석명'))
            print('\n아래 표는 .progress()에서 데이터 필터링에 활용되는 selector 파라미터의 활용 방법을 설명합니다. \n')
            self.showing(self.selector_for_howtouse)
        
        