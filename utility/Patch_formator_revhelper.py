"""
This python script is for analyzing all the changed source lines (diff) of the same file(i.e.,
change file for each comment) from earlier commits of the same pull request.
Source Paper: "Predicting Usefulness of Code Review Comments
using Textual Features and Developer Experience"
"""
import os
import pandas as pd
import re

def get_change_file(repo_name):
  change_file_map = {}
  with open(
      CHANGE_FILE_Dir + repo_name + "\\" + repo_name + "-comment-file.txt") as f:
    lines = f.readlines()
  for line in lines:
    splitted_line = line.split('\t')
    c_id = splitted_line[0]
    change_file = splitted_line[1]
    change_file_map[c_id] = change_file
  return change_file_map

def _patch_builder(repo_name):
  if not os.path.isdir(DATASET_Dir + '\\patch'):
    os.mkdir(DATASET_Dir + '\\patch')
  if not os.path.isdir(DATASET_Dir + '\\patch\\'+repo_name):
    os.mkdir(DATASET_Dir + '\\patch\\'+repo_name)

  with open(CORPUS_Dir + repo_name + "-corpus.txt",encoding="utf8") as f:
    lines = f.readlines()
  change_file_map = get_change_file(repo_name)
  pr_dir_list = os.listdir(PR_DIR + repo_name + "\\")
  commit_dir_list = os.listdir(COMMIT_DIR + repo_name + "\\")
  for line in lines:
    # Creating directory according to the corpus entry
    comment_dir_name = line.split("\t")
    if os.path.exists(DATASET_Dir + '\\patch\\' +repo_name+"\\"+comment_dir_name[0]):
      continue
    os.mkdir(DATASET_Dir + '\\patch\\' +repo_name+"\\"+comment_dir_name[0])
    splitted_line = line.split('-')
    comment_id = splitted_line[0]
    pr_id = splitted_line[1]
    change_file = ''
    if comment_id in change_file_map.keys():
      change_file = change_file_map.get(comment_id).strip()
    if pr_id + ".csv" in pr_dir_list:
      pr_df = pd.read_csv(PR_DIR + repo_name + "\\" + pr_id + ".csv")
      pr_commit_list = []
      for index, row in pr_df.iterrows():
        pr_commit_list.append(row['commit_id'])
      for commit in pr_commit_list:
        commit_file_name = commit + "-" + pr_id + ".csv"
        if commit_file_name in commit_dir_list:
          commit_df = pd.read_csv(COMMIT_DIR + repo_name + "\\" + commit_file_name)
          for index,row in commit_df.iterrows():
            c_file_list=re.sub(pattern,"",row['file_name'])
            c_file=c_file_list.split(",")
            if change_file in c_file:
              diff=re.sub(pattern,'',row['patch'])
              with open(DATASET_Dir + '\\patch\\' +repo_name+"\\"+comment_dir_name[0]+"\\"+commit+".txt",'w',encoding="utf-8") as f:
                diff_lines=diff.split("\\n")
                patch_line=[]
                for x in diff_lines:
                    f.write(x)
                    f.write("\n")
              f.close()
    existingfile=os.listdir(DATASET_Dir + '\\patch\\' +repo_name+"\\")
    print(f'file written {len(existingfile)} out of {len(lines)}')


if __name__ == "__main__":
  pattern = "'*|\[*|\]*"
  CORPUS_Dir = "C:\\Users\wahid\PycharmProjects\Replication-Study\Data\Corpus\initial data\\"
  CHANGE_FILE_Dir = "C:\\Users\wahid\PycharmProjects\Replication-Study\Data\github-scrapping\\version-history\\"
  DATASET_Dir = 'C:\\Users\\wahid\\PycharmProjects\\Replication-Study\\Data\\github-scrapping'
  PR_DIR = DATASET_Dir + '\\single-pr\\'
  COMMIT_DIR = DATASET_Dir + '\\single-commit\\'
  repo_name = "leakcanary"
  _patch_builder(repo_name)
