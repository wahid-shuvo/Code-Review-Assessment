import os
import re
import base64
import pandas as pd
from requests.adapters import Retry
import configparser
import requests
from typing import Dict, List, Optional, Tuple, Union

requests.session().get_adapter('https://').max_retries = Retry(
  total=10,
  backoff_factor=0.1,
)
ROOT = 'https://api.github.com'


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
      return 0
    limit_remaining = int(response_obj.headers['x-ratelimit-remaining'])
    if limit_remaining >= 1:
      break
    else:
      continue
  response = response_obj.json()
  print('token limit: ' + str(limit_remaining))
  return response


def _get_pull_request(owner, repo, token: Optional[str] = None):
  prDf = pd.DataFrame(
    columns=['pr_id', 'pr_title', 'requester', 'pr_requested_reviewers',
             'pr_comment', 'pr_commits', 'pr_link'])
  from itertools import count
  path_template = f'/repos/{owner}/{repo}/pulls?state=all&per_page=100'
  for page_n in count(1):
    path = path_template + f'&page={page_n}'
    response = get_rate_limited_response(f'{ROOT}{path}', token)

    # response output format here:
    # https://docs.github.com/en/rest/pulls/pulls#list-pull-requests getting
    # all the pull request in a repo

    print(len(prDf))
    '''
    check total repository commits has 
    been written or not
    '''
    if len(prDf) >= 16551:
      prDf.to_csv( os.path.join(DATASET_Dir, repo +'.csv'),
        index=False)
      print("Pr file written succesfully")
      return prDf

    for item in response:
      pr_title = item['title']
      pr_requested_reviewers = item['requested_reviewers']
      pr_id = item['number']
      requester = item['user']['login']
      pr_comment = item['review_comments_url']
      pr_commits = item['commits_url']
      pr_link = item['url']
      prDf = prDf.append(
        {'pr_id': pr_id, 'pr_title': pr_title, 'requester': requester,
         'pr_requested_reviewers': pr_requested_reviewers,
         'pr_comment': pr_comment, 'pr_commits': pr_commits,
         'pr_link': pr_link}, ignore_index=True)
  return prDf;


def _filter_pr_list(all_pr_list, repo_name):
  existing_prs = []
  if not os.path.exists(os.path.join(DATASET_Dir,'single-pr')):
    os.mkdir(os.path.join(DATASET_Dir,'single-pr'))
  if not os.path.exists(os.path.join(DATASET_Dir,'single-pr',repo_name)):
    os.mkdir(os.path.join(DATASET_Dir,'single-pr',repo_name))
  existing_file = os.listdir(os.path.join(DATASET_Dir,'single-pr',repo_name))
  for i in existing_file:
    pr_id = i.split('.')
    existing_prs.append(int(pr_id[0]))
  updated_pr_list = set(all_pr_list) - set(existing_prs)
  return list(updated_pr_list)


def _get_reviewers_list(path):
  revs_list = []
  query_response = get_rate_limited_response(path)
  for item in query_response:
    try:
      revs_list.append(item['user']['login'])
    except:
      print('Non type value in reviewers list')
  return revs_list


def _single_pr_content_collector(repo_name):
  pr_df = pd.read_csv(f'{DATASET_Dir}/{repo_name}.csv')
  all_pr_list = pr_df['pr_id'].to_list()
  updated_pr_list = _filter_pr_list(all_pr_list, repo_name)
  # converting the integer type list into string for condition checking convenience
  final_pr_list = [str(x) for x in updated_pr_list]

  for index, row in pr_df.iterrows():
    single_pr_df = pd.DataFrame(
      columns=['commit_id', 'commit_message', 'commit_url', 'commit_author',
               'commit_author_email',
               'commit_author_login', 'pr_reviewers'])
    pr_number = str(row['pr_id'])
    if pr_number in final_pr_list:
      pr_link = str(row['pr_link'])
      commit_link = str(row['pr_commits'])
      path_template = f'{commit_link}?per_page=100'
      response = get_rate_limited_response(f'{path_template}')
      if response==0:
        continue
      elif (response):
        pr_rev = _get_reviewers_list(f'{pr_link}/reviews?per_page=100')
        c = 0
        for item in response:
          c = c + 1
          try:
            single_pr_df = single_pr_df.append({'commit_id': item['sha'],
                                                'commit_message':
                                                  item['commit']['message'],
                                                'commit_author': item['commit'][
                                                  'author'],
                                                'commit_url': item['url'],
                                                'commit_author_email':
                                                  item['commit']['author'][
                                                    'email'],
                                                'commit_author_login':
                                                  item['author']['login'],
                                                'pr_reviewers': pr_rev},
                                               ignore_index=True)
          except:
            print('Python value error')
            continue
        print('total commit: ' + str(c))
        if not os.path.isdir(DATASET_Dir + '\\single-pr\\' + repo_name):
          os.mkdir(repo_name)
        single_pr_df.to_csv(
          DATASET_Dir + '\\single-pr\\' + repo_name + '\\' + pr_number + '.csv',
          index=False)
      else:
        print('response empty')
    temp = _filter_pr_list(all_pr_list, repo_name)
    file_written = len(all_pr_list) - len(temp)
    print(str(len(
      all_pr_list) - file_written) + ' file remaining to write out of ' + str(
      len(all_pr_list)))


def _filter_commit_list(all_pr_list, repo_name):
  existing_prs = []
  if not os.path.isdir('single-pr'):
    os.mkdir('single-pr')
  existing_file = os.listdir(DATASET_Dir + '\\single-pr\\' + repo_name)
  for i in existing_file:
    pr_id = i.split('.')
    existing_prs.append(int(pr_id[0]))
  updated_pr_list = set(all_pr_list) - set(existing_prs)
  return list(updated_pr_list)


def _get_commits_id(pr_list, repo_name):
  commit_sha_s = []
  for pr in pr_list:
    df = pd.read_csv(PR_DIR + repo_name + '\\' + pr)
    for index, row in df.iterrows():
      commit_sha_s.append(str(row['commit_id']) + '-' + pr)
  return commit_sha_s


def _filter_pr_commit_list(all_prs, repo_name):
  updated_prs = []
  all_commits_file_list = os.listdir(COMMIT_DIR + repo_name + '\\')
  for item in all_commits_file_list:
    pr = item.split('-')
    updated_prs.append(pr[1])
  remaining_prs = set(all_prs) - set(updated_prs)
  return list(remaining_prs)


def _single_commit_content_collector(repo_name):
  existing_commits_list = []
  if not os.path.isdir(COMMIT_DIR + repo_name):
    os.mkdir(COMMIT_DIR + repo_name)
  pr_list = os.listdir(PR_DIR + repo_name + '\\')
  reamianing_pr_list = _filter_pr_commit_list(pr_list, repo_name)
  all_commit_list = _get_commits_id(pr_list, repo_name)
  commit_ur_list = []
  for pr in reamianing_pr_list:
    df = pd.read_csv(PR_DIR + repo_name + '\\' + pr)
    commits = df['commit_id'].to_list();
    commit_ur_list.clear()
    commit_ur_list = df['commit_url'].to_list()
    if len(commit_ur_list) > 0:
      for index in range(len(commit_ur_list)):
        existing_commits_list = os.listdir(COMMIT_DIR + repo_name + '\\')
        if str(commits[index]) + '-' + pr in existing_commits_list:
          continue
        single_commit_df = pd.DataFrame(
          columns=['sha', 'parent_info', 'file_info', 'file_name',
                   'file_content', 'patch'])
        response = get_rate_limited_response(
          f'{commit_ur_list[index]}?per_page=100')
        if not response:
          continue
        parent_commit = response['parents']
        files = response['files']
        file_names = []
        file_contents = []
        file_patches = []
        for file in files:
          file_names.append(file['filename'])
          file_contents.append(file['contents_url'])
          try:
            file_patches.append(file['patch'])
          except:
            file_patches.append(None)
        try:
          single_commit_df = single_commit_df.append(
            {'sha': response['sha'], 'parent_info': parent_commit,
             'file_info': files,
             'file_name': file_names, 'file_content': file_contents,
             'patch': file_patches}, ignore_index=True)
        except:
          print('Python value error')
          continue
        single_commit_df.to_csv(
          COMMIT_DIR + repo_name + '\\' + response['sha'] + '-' + pr,
          index=False)
      existing_commits_list.clear()
      existing_commits_list = os.listdir(COMMIT_DIR + repo_name + '\\')
    print('Remaining file to write:  ' + str(
      len(all_commit_list) - len(existing_commits_list)) + ' out of ' + str(
      len(all_commit_list)))


def _handle_file_conflict(repo_name, commit_file_list):
  if not os.path.isdir('file-content'):
    os.mkdir('file-content')
  if not os.path.isdir(CHANGE_FILE_Dir + repo_name):
    os.mkdir(CHANGE_FILE_Dir + repo_name)

  existing_file = os.listdir(DATASET_Dir + '\\file-content\\' + repo_name)
  return list(set(commit_file_list) - set(existing_file))


def _get_change_file_content(repo_name):
  pattern = "'*|\[*|\]*"
  commit_file_list = os.listdir(COMMIT_DIR + repo_name + '\\')
  remaining_commit_file_list = _handle_file_conflict(repo_name,commit_file_list)

  for commit_file in remaining_commit_file_list:
    df = pd.read_csv(COMMIT_DIR + repo_name + '\\' + commit_file)
    if len(df):
      for index, row in df.iterrows():
        file_name_list_string = re.sub(pattern, '', row['file_name'])
        change_file_list = file_name_list_string.split(',')
        file_content_links_string = re.sub(pattern, '', row['file_content'])
        file_content_links = file_content_links_string.split(',')
        # print(file_content_links)
        # print(change_file_list)
        if len(change_file_list) > 0:
          change_file_df = pd.DataFrame(
            columns=['file_name', 'file_path', 'file_url', 'file_content'])
          for i in range(len(change_file_list)):
            if change_file_list[i].endswith('.py'):
              try:
                content_link = file_content_links[i]
                response = get_rate_limited_response(content_link)
                decoded_file_content = base64.b64decode(
                  response['content']).decode(encoding='utf-8')
                change_file_df = change_file_df.append(
                  {'file_name': response['name'], 'file_path': response['path'],
                   'file_url': response['url'],
                   'file_content': decoded_file_content},ignore_index=True)
              except:
                print(f"Empty Response for {row['file_name']}")
                continue
          if len(change_file_df)>0:
            change_file_df.to_csv(CHANGE_FILE_Dir + repo_name +'\\'+ commit_file[:-4] + '.csv',index=False)
    remaining_commit_file_list = _handle_file_conflict(repo_name,commit_file_list)
    print(f'File written: {len(commit_file_list)-len(remaining_commit_file_list)} out of {len(commit_file_list)}')


def _get_token_list():
  config = configparser.RawConfigParser()
  path = os.getcwd()
  config.read(path + '\\github-token.cfg')
  details_dict = dict(config.items('DEFAULT'))
  tokens = list(details_dict.values())
  return tokens


if __name__ == '__main__':
  DATASET_Dir = 'Data-dir'
  PR_DIR = DATASET_Dir + '\\single-pr\\'
  COMMIT_DIR = DATASET_Dir + '\\single-commit\\'
  CHANGE_FILE_Dir = DATASET_Dir + '\\file-content\\'

  os.chdir(DATASET_Dir)
  assert os.getcwd().endswith('github-scrapping')
  # repo_dict = {
  #
  # }
  owner = 'django'
  repo_list = ['django']
  for repo in repo_list:
    # _get_pull_request(owner, repo,'')
    # _single_pr_content_collector(repo)
    _single_commit_content_collector(repo)

# for repo in repo_list:
#   _get_change_file_content(repo)
