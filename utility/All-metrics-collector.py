'''
This python file is to merge all the metrics into one
to pass as a input for the machine learning model.
'''

import pandas as pd

def _get_reading_ease():
  comment_list=[]
  reading_ease=[]
  reading_ease_NL=[]
  with open(DATA_DIR+"uease-openSource.txt",'r',encoding="utf-8") as f1:
    lines=f1.readlines()
  f1.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    comment_list.append(temp[0])
    reading_ease.append(temp[1])
    reading_ease_NL.append(temp[2])
  with open(DATA_DIR+"nuease-openSource.txt",'r',encoding="utf-8") as f2:
    lines=f2.readlines()
  f2.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    comment_list.append(temp[0])
    reading_ease.append(temp[1])
    reading_ease_NL.append(temp[2])
  return comment_list,reading_ease,reading_ease_NL

def _get_code_element():
  comment_code_map={}
  with open(DATA_DIR+"uelem-openSource.txt",'r',encoding="utf-8") as f1:
    lines=f1.readlines()
  f1.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    comment_code_map[temp[0]]=temp[1]
  with open(DATA_DIR+"nuelem-openSource.txt",'r',encoding="utf-8") as f2:
    lines=f2.readlines()
  f2.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    comment_code_map[temp[0]] = temp[1]
  return comment_code_map

def _get_question_ratio():
  comment_question_map={}
  with open(DATA_DIR+"uquest-openSource.txt",'r',encoding="utf-8") as f1:
    lines=f1.readlines()
  f1.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    comment_question_map[temp[0]]=temp[1]
  with open(DATA_DIR+"nuquest-openSource.txt",'r',encoding="utf-8") as f2:
    lines=f2.readlines()
  f2.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    comment_question_map[temp[0]] = temp[1]
  return comment_question_map

def _get_stopword_ratio():
  comment_stopword_map={}
  with open(DATA_DIR+"ustop-openSource.txt",'r',encoding="utf-8") as f1:
    lines=f1.readlines()
  f1.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    comment_stopword_map[temp[0]]=temp[1]
  with open(DATA_DIR+"nustop-openSource.txt",'r',encoding="utf-8") as f2:
    lines=f2.readlines()
  f2.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    comment_stopword_map[temp[0]] = temp[1]
  return comment_stopword_map

def _get_stopkey_ratio():
  comment_stopkey_map={}
  with open(DATA_DIR+"ustopkey-openSource.txt",'r',encoding="utf-8") as f1:
    lines=f1.readlines()
  f1.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    comment_stopkey_map[temp[0]]=temp[1]
  with open(DATA_DIR+"nustopkey-openSource.txt",'r',encoding="utf-8") as f2:
    lines=f2.readlines()
  f2.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    comment_stopkey_map[temp[0]] = temp[1]
  return comment_stopkey_map

def _get_stopkey_ratio():
  comment_stopkey_map={}
  with open(DATA_DIR+"ustopkey-openSource.txt",'r',encoding="utf-8") as f1:
    lines=f1.readlines()
  f1.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    comment_stopkey_map[temp[0]]=temp[1]
  with open(DATA_DIR+"nustopkey-openSource.txt",'r',encoding="utf-8") as f2:
    lines=f2.readlines()
  f2.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    comment_stopkey_map[temp[0]] = temp[1]
  return comment_stopkey_map

def _get_conceptual_ratio():
  comment_concept_map={}
  with open(DATA_DIR+"concept-openSource.txt",'r',encoding="utf-8") as f1:
    lines=f1.readlines()
  f1.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    try:
      comment_concept_map[temp[0]]=temp[1]
    except:
      print(line)
  return comment_concept_map

def _get_authorship_ratio():
  comment_authorCommitFile_map={}
  comment_committedTwice_map={}
  comment_totalAuthoredCommits={}
  with open(DATA_DIR+"authorship-openSource.txt",'r',encoding="utf-8") as f1:
    lines=f1.readlines()
  f1.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    try:
      comment_authorCommitFile_map[temp[0]]=temp[1]
      comment_committedTwice_map[temp[0]]=temp[2]
      comment_totalAuthoredCommits[temp[0]]=temp[3]
    except:
      print(line)
  return comment_authorCommitFile_map,comment_committedTwice_map,comment_totalAuthoredCommits

def _get_reviewership_ratio():
  comment_reviewingTwice_map = {}
  comment_reviewCommitFile_map={}
  comment_totalreviewedCommits={}
  comment_reviewed_pr={}
  with open(DATA_DIR+"reviewership-openSource.txt",'r',encoding="utf-8") as f1:
    lines=f1.readlines()
  f1.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    try:
      comment_reviewingTwice_map[temp[0]]=temp[1]
      comment_reviewCommitFile_map[temp[0]]=temp[2]
      comment_totalreviewedCommits[temp[0]]=temp[3]
      comment_reviewed_pr[temp[0]] = temp[4]
    except:
      print(line)
  return comment_reviewCommitFile_map,comment_reviewingTwice_map,comment_totalreviewedCommits,comment_reviewed_pr

def _get_extLib_ratio():
  comment_extLib_map={}
  with open(DATA_DIR+"extLib-openSource.txt",'r',encoding="utf-8") as f1:
    lines=f1.readlines()
  f1.close()
  for line in lines:
    line=line.strip()
    temp=line.split('\t')
    try:
      comment_extLib_map[temp[0]]=temp[1]
    except:
      print(line)
  return comment_extLib_map

def _collect_all_metrics():
  df=pd.DataFrame(columns=["c_id","className","ReadingEase","ReadingEase(NL)","CodeElementRatio","QuestionRatio","StopwordRatio","StopKeyRatio","ConceptualSimilarity",
                           "AuthorCommitsFile","CommittedTwice","TotalAuthoredCommits","ReviewingTwice","ReviewedCommitsFile","TotalReviewedCommits","ReviewedPRs","ExtLibSimilarity"])
  comment_list,reading_ease,reading_ease_NL=_get_reading_ease()
  df["c_id"]=comment_list
  df['ReadingEase']=reading_ease
  df['ReadingEase(NL)']=reading_ease_NL
  comment_code_map=_get_code_element()
  comment_question_map=_get_question_ratio()
  comment_stopword_map=_get_stopword_ratio()
  comment_stopkey_map=_get_stopkey_ratio()
  comment_concept_map=_get_conceptual_ratio()
  comment_authorCommitFile_map,comment_committedTwice_map,comment_totalAuthoredCommits=_get_authorship_ratio()
  comment_reviewCommitFile_map, comment_reviewingTwice_map, comment_totalreviewedCommits, comment_reviewed_pr=_get_reviewership_ratio()
  comment_extLib_map=_get_extLib_ratio()
  for index,row in df.iterrows():
    comment_id=str(row['c_id']);
    temp=comment_id.split('-')
    row['className']=temp[2]
    if comment_id in comment_code_map.keys():
      row['CodeElementRatio']=comment_code_map.get(comment_id)
    if comment_id in comment_question_map.keys():
      row['QuestionRatio'] = comment_question_map.get(comment_id)
    if comment_id in comment_stopword_map.keys():
      row['StopwordRatio'] = comment_stopword_map.get(comment_id)
    if comment_id in comment_stopkey_map.keys():
      row['StopKeyRatio'] = comment_stopkey_map.get(comment_id)
    if comment_id in comment_concept_map.keys():
        row['ConceptualSimilarity'] = comment_concept_map.get(comment_id)
    if comment_id in comment_authorCommitFile_map.keys():
        row['AuthorCommitsFile'] = comment_authorCommitFile_map.get(comment_id)
    if comment_id in comment_committedTwice_map.keys():
        row['CommittedTwice'] = comment_committedTwice_map.get(comment_id)
    if comment_id in comment_totalAuthoredCommits.keys():
      row['TotalAuthoredCommits'] = comment_totalAuthoredCommits.get(comment_id)
    if comment_id in comment_reviewingTwice_map.keys():
      row['ReviewingTwice'] = comment_reviewingTwice_map.get(comment_id)
    if comment_id in comment_reviewCommitFile_map.keys():
      row['ReviewedCommitsFile'] = comment_reviewCommitFile_map.get(comment_id)
    if comment_id in comment_totalreviewedCommits.keys():
      row['TotalReviewedCommits'] = comment_totalreviewedCommits.get(comment_id)
    if comment_id in comment_reviewed_pr.keys():
      row['ReviewedPRs'] = comment_reviewed_pr.get(comment_id)
    if comment_id in comment_extLib_map.keys():
      row['ExtLibSimilarity'] = comment_extLib_map.get(comment_id)
  df.to_csv(DATA_DIR+"modeldata-training-and-testing-openSource.csv",index=False)
  txt_df=df.drop(['c_id'],axis=1)
  txt_df.to_csv(DATA_DIR + "modeldata-training-and-testing-openSource.txt",index=None,sep=' ',mode='a')
  print("File written successfully")


if __name__=='__main__':
  DATA_DIR="C:\\Users\wahid\CodeReviewHelper\\New-Dataset\All metrics\\"
  _collect_all_metrics()