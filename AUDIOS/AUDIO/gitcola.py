from github import Github
import os

g = Github('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')
repo = g.get_repo("sergiolucero/corfo-parkinsons-streamlit")
#source=repo.get_branch('master')
contents=repo.get_contents('app.py')
print(contents.decoded_content)

repo.create_file('test.txt', content='wena!', message='uno de prueba')
#https://towardsdatascience.com/all-the-things-you-can-do-with-github-api-and-python-f01790fca131
push(file_path, "Add pytest to dependencies.", data, "update-dependencies", update=True)

