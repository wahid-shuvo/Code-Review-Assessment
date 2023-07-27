import os
import re
import base64
import pandas as pd
from requests.adapters import Retry
import configparser
import requests


requests.session().get_adapter('https://').max_retries = Retry(
  total=10,
  backoff_factor=0.1,
)
ROOT = 'https://api.github.com'

# def _handle_file_conflict(repo_name, file_list):
#   if not os.path.isdir('file-content'):
#     os.mkdir('file-content')
#   if not os.path.isdir(CHANGE_FILE_Dir + repo_name):
#     os.mkdir(CHANGE_FILE_Dir + repo_name)
#
#   existing_file = os.listdir(DATASET_Dir + '\\file-content\\' + repo_name)
#   existing_file=[x.replace('')for x in existing_file]
#   return list(set(file_list) - set(existing_file))

def get_rate_limited_response(path: str, token=None):
  token_list = _get_token_list()
  for i in range(len(token_list)):
    token = token_list[i]
    _headers = {
      'Authorization': f'Bearer {token}'
    }
    try:
      response_obj = requests.get(path, headers=_headers)
    except:
      print("No commits on pr:" + path)
      return False
    limit_remaining = int(response_obj.headers['x-ratelimit-remaining'])
    if limit_remaining >= 1:
      break
    else:
      continue
  response = response_obj.json()
  print('token limit: ' + str(limit_remaining))
  return response


def _get_change_file_link(repo_name):
  pattern = "'*|\[*|\]*"
  commit_file_list = os.listdir(COMMIT_DIR + repo_name + '\\')
  change_file_map = {}
  for commit_file in commit_file_list:
    df = pd.read_csv(COMMIT_DIR + repo_name + '\\' + commit_file)
    if len(df):
      for index, row in df.iterrows():
        file_name_list_string = re.sub(pattern, '', row['file_name'])
        change_file_list = file_name_list_string.split(',')
        file_content_links_string = re.sub(pattern, '', row['file_content'])
        file_content_links = file_content_links_string.split(',')
        if len(change_file_list) > 0 and len(file_content_links) > 0:
          for i in range(len(change_file_list)):
            if change_file_list[i].endswith('.java'):
              if change_file_list[i] in change_file_map.keys():
                continue
              try:
                change_file_map[change_file_list[i]] = file_content_links[i]
              except:
                print(row['file_name'])
    print(len(change_file_map))
  # print(change_file_map)
  return change_file_map

def _ensure_change_file_written(repo_name):
  change_file_map=_get_change_file_link(repo_name)
  if not os.path.isdir('file-content'):
    os.mkdir('file-content')
  if not os.path.isdir(CHANGE_FILE_Dir + repo_name):
    os.mkdir(CHANGE_FILE_Dir + repo_name)
  for file_name,file_link in change_file_map.items():
    existing_file = os.listdir(DATASET_Dir + '\\file-content\\' + repo_name)
    if file_name[:-3].replace('/','-')+'.csv' not in existing_file:
      change_file_df = pd.DataFrame(
        columns=['file_name', 'file_path', 'file_url', 'file_content'])
      try:
        link=file_link.replace('\'','')
        response = get_rate_limited_response(link)
        decoded_file_content = base64.b64decode(response['content']).decode(encoding='utf-8')
        change_file_df = change_file_df.append({'file_name': response['name'], 'file_path': response['path'],'file_url': response['url'],'file_content': decoded_file_content}, ignore_index=True)
      except:
        print(f"Empty Response for {file_name}")
        continue
      modified_file_name=file_name[:-3].replace('/','-')
      change_file_df.to_csv(DATASET_Dir + '\\file-content\\' + repo_name+'\\'+modified_file_name+'.csv',index=False)
      existing_file=os.listdir(DATASET_Dir + '\\file-content\\' + repo_name)
      print(f'file written {len(existing_file) } out of {len(change_file_map.keys())} ')


def _get_token_list():
  config = configparser.RawConfigParser()
  path = os.getcwd()
  config.read(path + '\\github-token.cfg')
  details_dict = dict(config.items('DEFAULT'))
  tokens = list(details_dict.values())
  return tokens

if __name__ == '__main__':
  DATASET_Dir = 'C:\\Users\\wahid\\PycharmProjects\\Replication-Study\\Data\\github-scrapping'
  PR_DIR = DATASET_Dir + '\\single-pr\\'
  COMMIT_DIR = DATASET_Dir + '\\single-commit\\'
  CHANGE_FILE_Dir = DATASET_Dir + '\\file-content\\'
  repo_name = 'elasticsearch'
  # changefile_dict= _get_change_file_link(repo_name)
  # print(changefile_dict)
  _ensure_change_file_written(repo_name)
