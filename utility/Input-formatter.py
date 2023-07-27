'''
 This script is for formatting the input data for various operation of
'''
import os

from xlrd import open_workbook
import pandas as pd
import numpy as np

# function to convert excel file into csv file
def _excel_to_csv(file_name):
  workbook = open_workbook(GOLD_DIR +file_name+".xlsx")
  sheet = workbook.sheet_by_index(0)
  texts = []
  labels = []
  df = pd.DataFrame(columns=['text', 'label'])
  for cell_num in range(0, sheet.nrows):
    text = sheet.cell(cell_num, 0).value
    label = sheet.cell(cell_num, 1).value
    if not label == 2.0:
      texts.append(text)
      labels.append(label)
  del texts[0]
  del labels[0]
  df['text'] = texts
  df['label'] = labels
  df.to_csv(DATA_DIR+file_name+'.csv',index=False)
  print(file_name+'.csv written successfully')

# function to merge two dataset into one
def _merge_dataframe(file1,file2):
  df1=pd.read_csv(DATA_DIR+file1+".csv")
  df2 = pd.read_csv(DATA_DIR + file2 + ".csv")
  merged_df=df1.append(df2)
  merged_df.to_csv(DATA_DIR+'merged-corpus.csv',index=False)
  return merged_df

# function to convert txt file into csv file
def txt_to_csv(file_name):
  df=pd.read_csv("C:\\Users\wahid\PycharmProjects\Replication-Study\Data\Corpus\initial data\\"+file_name+'.txt',sep='\t',encoding='utf-8',names=['id','text'])
  #df.to_csv("C:\\Users\wahid\CodeReviewHelper\\New-Dataset\All metrics\\"+file_name+'.csv',encoding='utf-8',index=False)

  #print(df)
  return df


def _read_csv(path,file):
  return pd.read_csv(path+file+'.csv')

# function to build programming language dataset
def _programming_language_dataset_builder(file1,file2,gold_file1,gold_file2,language):
  prog_file1=txt_to_csv(file1)
  prog_file2=txt_to_csv((file2))
  programming_df=prog_file1.append(prog_file2)
  programming_df=programming_df.drop_duplicates()
  gold1=_read_csv(GOLD_DIR,gold_file1+'-uid')
  gold2=_read_csv(GOLD_DIR,gold_file2+'-uid')
  gold_corpus=gold1.append(gold2)
  gold_corpus=gold_corpus[gold_corpus.gold!=2]
  gold_corpus=gold_corpus.drop_duplicates()
  for index,row in programming_df.iterrows():
    tmp=row['id'].split('-')
    c_id=tmp[0]+'-'+tmp[1]
    if c_id in list(gold_corpus.id) :
      t = gold_corpus[gold_corpus['id'] == c_id]
      try:
        gold_polarity=float(t['gold'].values[0])
        programming_df['id'][index] = row['id']
        programming_df['polarity'][index]=gold_polarity
      except Exception as e:
        print(e)
  programming_df=programming_df.dropna()
  # drop_indices=np.random.choice(programming_df.index,3,replace=False)
  # programming_df_subset=programming_df.drop(drop_indices)
  sample_df=programming_df.sample(n=350,random_state=42,ignore_index=True)
  sample_df.to_csv(GOLD_DIR+'programming-language\\'+language+'.csv',index=False)
  print(language+'.csv written successfully')

# Function to merge multiple dataframe
def _merge_multiple_dataframe(repo):
  file_list=os.listdir(os.path.join(DATA_DIR,repo))
  df=pd.DataFrame()
  for file in file_list:
    temp_df=pd.read_csv(os.path.join(DATA_DIR,repo,file))
    df=df.append(temp_df)
  df.to_csv(os.path.join(DATA_DIR,repo,repo+"-comments.csv"),index=False)
  print("file written successfully")


def _programming_language_dataset_builder_updated(file1,file2,file3,file4,file5,file6,gold_file):
  prog_file1=txt_to_csv(file1)
  prog_file2=txt_to_csv((file2))
  programming_df_python=prog_file1.append(prog_file2)

  prog_file11=txt_to_csv(file3)
  prog_file12=txt_to_csv((file4))
  programming_df_java=prog_file11.append(prog_file12)

  prog_file111=txt_to_csv(file5)
  prog_file122=txt_to_csv((file6))
  programming_df_javascript=prog_file111.append(prog_file122)

  gold1=_read_csv(GOLD_DIR,gold_file)
  gold1['project_name']=None
  for index,row in gold1.iterrows():
    if row['c_id'] in list(programming_df_python.id) :
      gold1['project_name'][index] = 'python'
    elif row['c_id'] in list(programming_df_java.id) :
      gold1['project_name'][index] = 'java'
    elif row['c_id'] in list(programming_df_javascript.id):
      gold1['project_name'][index]='javascript'
  gold1.to_csv("C:\\Users\wahid\PycharmProjects\Replication-Study\Goldset\programming-language\\modeldata-training-and-testing-openSource-programming-language.csv",index=False)

def formatDatasetForReviewExperienceCalculation(repo_name):
  df=pd.read_csv(os.path.join("C:\\Users\wahid\PycharmProjects\Replication-Study\Data",repo_name,repo_name+"-review-comment-final-sample-for-EMSE.csv"))
  text=df['comment_text'].to_list()
  text=[' '.join(x.split("\n")) for x in text ]
  df['comment_text']=text
  df.to_csv(os.path.join("C:\\Users\wahid\PycharmProjects\Replication-Study\Data",repo_name,repo_name+"-review-comment-final-sample-for-EMSE-formatted.csv"))


if __name__=='__main__':
  DATA_DIR="C:\\Users\wahid\PycharmProjects\Replication-Study\Data\\"
  GOLD_DIR="C:\\Users\wahid\PycharmProjects\Replication-Study\Goldset\\"
  # file1='keras-corpus'
  # file2='numpy-corpus'
  # file3="elasticsearch-corpus"
  # file4="leakcanary-corpus"
  # file5="meteor-corpus"
  # file6="polymer-corpus"
  # gold_file='modeldata-training-and-testing-openSource-senti'
  # repo_names=["elasticsearch"]
  #txt_to_csv(file)
  # _excel_to_csv(file3)
  # _merge_dataframe(file1,file_2)
  # _programming_language_dataset_builder_updated(file1,file2,file3,file4,file5,file6,gold_file)
  # # for repo in repo_names:
  #   _merge_multiple_dataframe(repo)
  formatDatasetForReviewExperienceCalculation("youtube-dl")

