import pandas as pd
import numpy as np
from mlxtend.evaluate import mcnemar

def _build_contingency_table(dfA,dfB,dfGold):
  n11 = 0
  n12 = 0
  n21 = 0
  n22 = 0
  dfA['label']=[float(x) for x in dfA['label']]
  for i in range(len(dfA)):
    if dfA['label'][i]==dfGold['Polarity'][i] and dfB['nlp'][i]==dfGold['Polarity'][i]:
      n11 = n11 + 1;
    if dfA['label'][i]==dfGold['Polarity'][i] and dfB['nlp'][i]!=dfGold['Polarity'][i]:
      n12 = n12 + 1;
    if dfA['label'][i] != dfGold['Polarity'][i] and dfB['nlp'][i] ==dfGold['Polarity'][i]:
      n21=n21+1
    if dfA['label'][i] != dfGold['Polarity'][i] and dfB['nlp'][i] !=dfGold['Polarity'][i]:
      n22=n22+1

  table = np.array([[n11, n12],
                    [n21, n22]])
  print(table)
  chi2, p = mcnemar(ary=table, corrected=True)
  # summarize the finding
  print('chi-squared:', chi2)
  print('p-value: {:.15f}'.format(p))



def _McNemar_test(file1,file2,gold_file):
  dfA=pd.read_csv(SentiMoji_DIR+file1+'.txt',sep='\t',encoding='utf-8',names=('text','label'))
  dfA['label'] = dfA['label'] - 1
  dfGold=pd.read_csv(SentiMoji_DIR+gold_file+'.csv')
  dfB=pd.read_csv(Second_SE_DIR+file2+'.csv')
  table=_build_contingency_table(dfA,dfB,dfGold)


if __name__=='__main__':
  DATA_DIR = "C:\\Users\wahid\PycharmProjects\Replication-Study\Data\\"
  Second_SE_DIR="C:\\Users\wahid\PycharmProjects\Replication-Study\Stanford-Core-NlP\\"
  SentiMoji_DIR = "C:\\Users\wahid\PycharmProjects\Replication-Study\SentiMoji\\"
  file1='merged-corpus-test-SentiMoji-pred'
  file2='merged-NLP-prediction'
  gold_file='merged-corpus-test-SentiMoji'
  _McNemar_test(file1,file2,gold_file)