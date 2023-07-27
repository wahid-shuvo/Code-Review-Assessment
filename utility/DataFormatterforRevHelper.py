'''
This python file is for formatting the data according to the source code input of REVHelper Replication
'''

import os
import re
import json
import ast
from collections import namedtuple
import pandas as pd
import javalang

Import = namedtuple("Import", ["module", "name", "alias"])
'''
This function is for creating the PUll Request map for each dataset repository-
i.e., keras.json, elasticsearch.json
'''


def _pull_request_datamap_builder(repo_name):
  pattern = "'*|\[*|\]*"
  pr_df = pd.read_csv(DATASET_Dir + '\\' + repo_name + '.csv')
  pr_datamap = []
  num_empty_pr = 0
  for index, row in pr_df.iterrows():
    pr_dict = {}
    pr_dict["prNumber"] = row['pr_id']
    pr_dict['requester'] = row['requester']
    try:
      single_pr_df = pd.read_csv(
        PR_DIR + repo_name + '\\' + str(row['pr_id']) + '.csv')
    except:
      num_empty_pr = num_empty_pr + 1;
      print("Empty Pull request: " + str(row['pr_id']))
      continue
    commitShas = list(single_pr_df['commit_id'])
    pr_dict['commitSHAs'] = commitShas
    '''
    row['pr_requested_reviewers'] stored as a string
    therefore need to extract the recommended reviewer name
    using regex
    '''
    recommendedRevs = []
    if len(row['pr_requested_reviewers']) > 1:
      temp = row['pr_requested_reviewers'].replace('\'', '')
      rev_login_info = re.findall("login:\s*\w*", temp)
      for items in rev_login_info:
        item = items.split(':')
        recommendedRevs.append(item[1])

    pr_dict['recommendedRevs'] = recommendedRevs

    pr_revs = single_pr_df['pr_reviewers']
    if len(pr_revs):
      for index, value in pr_revs.items():
        temp = re.sub(pattern, '', value)
        actualRevs = temp.split(',')
        break
    pr_dict['actualRevs'] = actualRevs
    pr_datamap.append(pr_dict)
  jsonString = json.dumps(pr_datamap)
  jsonFile = open(DATASET_Dir + '\\PR\\' + repo_name + ".json", "w")
  jsonFile.write(jsonString)
  jsonFile.close()
  print(f"Number of empty pull request: {num_empty_pr} in {repo_name}")


'''
This function is for creating the Commit map for each dataset repository-
i.e., keras.json, elasticsearch.json
'''


def _commit_change_file_map(repo_name):
  pattern = "'*|\[*|\]*"
  commit_file_list = os.listdir(COMMIT_DIR + repo_name + '\\')
  commit_map_dict = {}
  for commit_file in commit_file_list:
    df = pd.read_csv(COMMIT_DIR + repo_name + '\\' + commit_file)
    if len(df):
      for index, row in df.iterrows():
        file_name_list_string = re.sub(pattern, '', row['file_name'])
        change_file_list = file_name_list_string.split(',')
        commit_map_dict[row['sha']] = change_file_list
    # print(commit_map_dict)
  with open(DATASET_Dir + '\\COMMIT\\' + repo_name + '.json', 'w') as fp:
    json.dump(commit_map_dict, fp)
  print(f'The file have been written successfully for {repo_name}')


# function for parsing python file
def get_imports(file):
  root = ast.parse(file)
  for node in ast.iter_child_nodes(root):
    if isinstance(node, ast.Import):
      module = []
    elif isinstance(node, ast.ImportFrom):
      if node.module is None:
        module = ['.' * node.level]
      else:
        module = node.module.split('.')
    else:
      continue
    for n in node.names:
      yield Import(module, n.name.split('.'), n.asname)


def _change_file_token_map_builder_python(repo_name):
  file_list = os.listdir(CHANGE_FILE_Dir + '\\' + repo_name)
  change_file_map = []
  for file in file_list:
    df = pd.read_csv(CHANGE_FILE_Dir + '\\' + repo_name + '\\' + file)
    for index, row in df.iterrows():
      file_content = row['file_content']
      # file_path = row['file_path'].replace('/', '\\/')
      file_path=row['file_path']
      # Checking empty file content
      try:
        if len(file_content) > 0:
          change_file_dict = {}
          content = file_content
          lines = content.split("\n")
          code = ""
          for line in lines:
            line = line.strip()
            if line.startswith("import"):
              code += line + "\n"
            elif line.startswith("from") and "import" in line:
              code += line + "\n"
          import_token = get_imports(code)
          import_stmts = list(
            map(lambda node: [node.name, node.alias], import_token))
          tokens = ""
          for stmt in import_stmts:
            cleaned_token = re.sub(pattern, '', str(stmt[0]))
            tokens += cleaned_token + " " + str(stmt[1]) + " "
            tokens = tokens.replace('None', '')
          change_file_dict["file"] = file_path
          change_file_dict["token"] = tokens
          change_file_map.append(change_file_dict)
      except:
        print(f"file name: {file} and file path {row['file_path']}")
  # if not os.path.isdir(DATASET_Dir + 'JSON'):
  #   os.mkdir(DATASET_Dir + '\\JSON')
  jsonString = json.dumps(change_file_map)
  jsonFile = open(DATASET_Dir + '\\JSON\\' + repo_name + ".json", "w")
  jsonFile.write(jsonString)
  jsonFile.close()
  print(f'{repo_name} written successfully')



def _change_file_token_map_builder_java(repo_name):
  file_list = os.listdir(CHANGE_FILE_Dir + '\\' + repo_name)
  change_file_map = []
  for file in file_list:
    df = pd.read_csv(CHANGE_FILE_Dir + '\\' + repo_name + '\\' + file)
    for index, row in df.iterrows():
      file_content = row['file_content']
      # file_path = row['file_path'].replace('/', '\\/')
      file_path=row['file_path']
      # Checking empty file content
      try:
        if len(file_content) > 0:
          change_file_dict = {}
          contents = file_content.split('{')
          code = contents[0] + '{}'
          #  Java File parsing
          # Link: https://github.com/c2nes/javalang
          tree = javalang.parse.parse(code)
          tokens = ""
          package_statement = tree.children[0]
          try:
            tokens += package_statement.name
          except:
            print("No package included")
          import_statements = tree.children[1]
          for item in import_statements:
            tokens += " " + item.path
          change_file_dict["file"] = file_path
          change_file_dict["token"] = tokens
          change_file_map.append(change_file_dict)
      except:
        print(f"file name: {file} and file path {row['file_path']}")
  # if not os.path.isdir(DATASET_Dir + 'JSON'):
  #   os.mkdir(DATASET_Dir + '\\JSON')
  jsonString = json.dumps(change_file_map)
  jsonFile = open(DATASET_Dir + '\\JSON\\' + repo_name + "-witout-Replaceing-slash.json", "w")
  jsonFile.write(jsonString)
  jsonFile.close()
  print(f'{repo_name} written successfully')

def _change_file_token_map_builder_kotlin(repo_name):
  file_list = os.listdir(CHANGE_FILE_Dir + '\\' + repo_name)
  change_file_map = []
  for file in file_list:
    df = pd.read_csv(CHANGE_FILE_Dir + '\\' + repo_name + '\\' + file)
    for index, row in df.iterrows():
      file_content = row['file_content']
      # file_path = row['file_path'].replace('/', '\\/')
      file_path=row['file_path']
      # Checking empty file content
      try:
        if len(file_content) > 0:
          change_file_dict = {}
          content = file_content
          lines = content.split("\n")
          code = ""
          for line in lines:
            line = line.strip()
            if line.startswith("import"):
              code += line + ";\n"
            elif line.startswith("package"):
              code += line + ";\n"
        #  Kotlin File parsing
        # Link: https://github.com/c2nes/javalang
        tree = javalang.parse.parse(code)
        tokens = ""
        package_statement = tree.children[0]
        try:
          tokens += package_statement.name
        except:
          print("No package included")
        import_statements = tree.children[1]
        for item in import_statements:
          tokens += " " + item.path
        change_file_dict["file"] = file_path
        change_file_dict["token"] = tokens
        change_file_map.append(change_file_dict)
      except:
        print(f"file name: {file} and file path {row['file_path']}")
  jsonString = json.dumps(change_file_map)
  jsonFile = open(
    DATASET_Dir + '\\JSON\\' + repo_name + "-witout-Replaceing-slash.json", "w")
  jsonFile.write(jsonString)
  jsonFile.close()
  print(f'{repo_name} written successfully')

def _comment_author_map_builder(repo_name):
  accstat_map={}
  with open(COMMENT_AUTHOR_Dir+repo_name+"\\"+repo_name+"-unique-author-login.txt",'r',encoding="utf-8") as cf1:
    accstat_line=cf1.readlines()
    for acc_line in accstat_line:
      acc_line=acc_line.strip()
      acc_line_token=acc_line.split("\t")
      print(acc_line_token)
      accstat_map[acc_line_token[0]]=acc_line_token[2]
  cf1.close()

  with open(COMMENT_AUTHOR_Dir+repo_name+"\\"+repo_name+"-comment-author.txt",'r',encoding="utf-8") as cf2:
    comment_author_lines=cf2.readlines()
    for c_line in comment_author_lines:
      c_line=c_line.strip()
      c_tokens=c_line.split("\t")
      author_login=c_tokens[1]
      comment_id=c_tokens[0]
      author_comment_info=''
      if author_login in accstat_map.keys():
        email=accstat_map.get(author_login)
        temp=email.strip()
        author_email=re.sub('<|>','',temp)
        author_comment_info=comment_id+"\t"+author_email
        with open(COMMENT_AUTHOR_Dir+repo_name+"\\"+repo_name+"-comment-author-email-version.txt",'a',encoding="utf-8") as cf3:
          cf3.write(author_comment_info)
          cf3.write("\n")
        cf3.close()

def _change_file_token_map_builder_javascript(repo_name):
  regex_require = 'require\(\S*?\)'
  regex_preprocess = "require\(|\)|\'"
  regex_import = '\*|import|\sas|from|\"|\{|\}|\(|\)|var\s\S*\s=\s|;|\[*|\]*|,|.*/m'
  file_list = os.listdir(CHANGE_FILE_Dir + '\\' + repo_name)
  change_file_map = []
  for file in file_list:
    df = pd.read_csv(CHANGE_FILE_Dir + '\\' + repo_name + '\\' + file)
    for index, row in df.iterrows():
      file_content = row['file_content']
      # file_path = row['file_path'].replace('/', '\\/')
      file_path=row['file_path']
      # Checking empty file content
      try:
        if len(file_content) > 0:
          change_file_dict = {}
          content = file_content
          lines = content.split("\n")
          code = []
          for line in lines:
            line = line.strip()
            if line.startswith('\\'):
              continue
            elif 'require(' in line:
              code.append(line)
            elif 'import ' in line:
              code.append(line)
        #  Javascript import token extracting using regex
        tokens = ''
        for line in code:
          if 'require' in line:
            require_item = re.findall(regex_require, line)
            for i in require_item:
              tokens = tokens + re.sub(regex_preprocess, '', i)+' '
          else:
            tokens=re.sub(regex_import, '', line).strip()
        change_file_dict["file"] = file_path
        change_file_dict["token"] = tokens
        change_file_map.append(change_file_dict)
      except:
        print(f"file name: {file} and file path {row['file_path']}")
  jsonString = json.dumps(change_file_map)
  jsonFile = open(
    DATASET_Dir + '\\JSON\\' + repo_name + "-witout-Replaceing-slash.json", "w")
  jsonFile.write(jsonString)
  jsonFile.close()
  print(f'{repo_name} written successfully')

if __name__ == '__main__':
  repo_list = ['django']
  DATASET_Dir = 'C:\\Users\\wahid\\PycharmProjects\\Replication-Study\\Data\\github-scrapping'
  PR_DIR = DATASET_Dir + '\\single-pr\\'
  COMMIT_DIR = DATASET_Dir + '\\single-commit\\'
  CHANGE_FILE_Dir = DATASET_Dir + '\\file-content\\'
  COMMENT_AUTHOR_Dir="C:\\Users\wahid\CodeReviewHelper\\New-Dataset\\"
  pattern = "'*|\[*|\]*"

for repo in repo_list:
  _pull_request_datamap_builder(repo)
for repo in repo_list:
  _commit_change_file_map(repo)
for repo in repo_list:
  _comment_author_map_builder(repo)

# for repo in repo_list:
#   # _change_file_token_map_builder_javascript(repo)
#   _change_file_token_map_builder_python(repo)
#   # _change_file_token_map_builder_java('elasticsearch')
#   # _change_file_token_map_builder_kotlin('leakcanary')