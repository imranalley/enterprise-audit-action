from time import strftime
import requests
import queries
import csv
from datetime import date
import os

###################################################################
# enterprise-audit-action - Input Parameters from action.yml file #
###################################################################
gh_repo_owner = os.environ["INPUT_OWNER"]
gh_repo_name = os.environ["INPUT_REPOSITORY"]
gh_token = os.environ["INPUT_TOKEN"]
gh_organization = os.environ["INPUT_ORGANIZATION"]
gh_team = os.environ["INPUT_TEAM"]
useCase = os.environ["INPUT_AUDIT"]
gh_user = os.environ["INPUT_USER"]
 
# GH Authentication
headers = {"Authorization": "Bearer {0}".format(gh_token) }
 
#################################################################
# Use Case 1 (Audit Org) - List all repos and permissions per Organization #
#################################################################
 
def situation_audit_org(local_gh_organization, local_gh_repo_owner, local_gh_repo_name):
    local_csv_data = []
    try:
        # Request
        tmp_gh_query = queries.auditOrgQuery.replace("#ORG#", local_gh_organization)
        request = requests.post("https://github.com/api/graphql", json={'query': tmp_gh_query}, headers=headers)
        response = request.json()["data"]
        print ("response:", response)
        collaborators = response["organization"]["repositories"]["nodes"]
        print ("collaborators:", collaborators)
        nextPage = response["organization"]["repositories"]["pageInfo"]["hasNextPage"]
        pageEnd = response["organization"]["repositories"]["pageInfo"]["endCursor"]
        print(pageEnd)
 
        for c in collaborators:
            print("{0},{1},{2}".format(local_gh_organization, c["nameWithOwner"], c["collaborators"]))
            local_csv_data.append([local_gh_organization, c["nameWithOwner"], c["collaborators"]])
 
        while(nextPage == True):
            print("loop start")
            tmp_gh_query = queries.auditOrgQueryPagination.replace("#ORG#", local_gh_organization).replace("#PAGE#", pageEnd)
            print(tmp_gh_query)
            request = requests.post("https://github.com/api/graphql", json={'query': tmp_gh_query}, headers=headers)
            response = request.json()["data"]
            print ("response:", response)
            collaborators = response["organization"]["repositories"]["nodes"]
            print ("collaborators:", collaborators)
            nextPage = response["organization"]["repositories"]["pageInfo"]["hasNextPage"]
            pageEnd = response["organization"]["repositories"]["pageInfo"]["endCursor"]
            print(pageEnd)
 
            for c in collaborators:
                print("{0},{1},{2}".format(local_gh_organization, c["nameWithOwner"], c["collaborators"]))
                local_csv_data.append([local_gh_organization, c["nameWithOwner"], c["collaborators"]])
 
    except Exception as e:
        print("Error retrieving ACL for {0}".format(local_gh_organization))
        print(e)
   
    return local_csv_data
 
#################################################################
# Use Case 2 (Audit Team) - List all repos and permissions per Team          #
#################################################################
 
def situation_audit_team(local_gh_organization, local_gh_team):
    local_csv_data = []
    try:
        # Request
        tmp_gh_query = queries.auditTeamQuery.replace("#ORG#", local_gh_organization).replace("#TEAM#", local_gh_team)
        request = requests.post("https://github.com/api/graphql", json={'query': tmp_gh_query}, headers=headers)
        response = request.json()["data"]
        members = response["organization"]["team"]["members"]["nodes"]
        permissions = response["organization"]["team"]["members"]["edges"]
        nextPage = response["organization"]["team"]["members"]["pageInfo"]["hasNextPage"]
        pageEnd = response["organization"]["team"]["members"]["pageInfo"]["endCursor"]
 
        for i in range(len(members)):
            print("{0},{1},{2},{3}".format(local_gh_organization, local_gh_team, members[i]["name"], members[i]["login"], permissions[i]["role"]))
            local_csv_data.append([local_gh_organization, local_gh_team, members[i]["name"], members[i]["login"], permissions[i]["role"]])
       
        while (nextPage == True):
            tmp_gh_query = queries.auditTeamQueryPagination.replace("#ORG#", local_gh_organization).replace("#TEAM#", local_gh_team).replace("#PAGE#", pageEnd)
            request = requests.post("https://github.com/api/graphql", json={'query': tmp_gh_query}, headers=headers)
            response = request.json()["data"]
            members = response["organization"]["team"]["members"]["nodes"]
            permissions = response["organization"]["team"]["members"]["edges"]
            nextPage = response["organization"]["team"]["members"]["pageInfo"]["hasNextPage"]
            pageEnd = response["organization"]["team"]["members"]["pageInfo"]["endCursor"]
 
            for i in range(len(members)):
                print("{0},{1},{2},{3}".format(local_gh_organization, local_gh_team, members[i]["name"], members[i]["login"], permissions[i]["role"]))
                local_csv_data.append([local_gh_organization, local_gh_team, members[i]["name"], members[i]["login"], permissions[i]["role"]])
    except Exception as e:
        print("Error retrieving ACL for {0}".format(local_gh_team))
        print(e)
   
    return local_csv_data
 
#################################################################
# Use Case 3 (Audit User) - List all repos and permissions of user
#################################################################
 
def situation_audit_user(local_gh_user):
    local_csv_data = []
    try:
        # Request
        tmp_gh_query = queries.auditUserQuery.replace("#USER#", local_gh_user)
        request = requests.post("https://github.com/api/graphql", json={'query': tmp_gh_query}, headers=headers)
        response = request.json()["data"]
        nextPage = response["user"]["repositories"]["pageInfo"]["hasNextPage"]
        pageEnd = response["user"]["repositories"]["pageInfo"]["endCursor"]
        repos = response["user"]["repositories"]["nodes"]
        print (nextPage)
 
        for c in repos:
            print("{0},{1},{2}".format(local_gh_user, c["nameWithOwner"], c["viewerPermission"]))
            local_csv_data.append([local_gh_user, c["nameWithOwner"], c["viewerPermission"]])
       
        while(nextPage == True):
            tmp_gh_query = queries.auditUserQueryPagination.replace("#USER#", local_gh_user).replace("#PAGE#", pageEnd)
            request = requests.post("https://github.com/api/graphql", json={'query': tmp_gh_query}, headers=headers)
            response = request.json()["data"]
            nextPage = response["user"]["repositories"]["pageInfo"]["hasNextPage"]
            pageEnd = response["user"]["repositories"]["pageInfo"]["endCursor"]
            repos = response["user"]["repositories"]["nodes"]
            print (nextPage)
 
            for c in repos:
                print("{0},{1},{2}".format(local_gh_user, c["nameWithOwner"], c["viewerPermission"]))
                local_csv_data.append([local_gh_user, c["nameWithOwner"], c["viewerPermission"]])
    except:
        print("Error retrieving ACL for {0}".format(local_gh_user))
   
    return local_csv_data
 
####################################################################
# Situation 4 (Audit Repo)- List user and permissions per list of repositories #
####################################################################
 
def situation_audit_repo(local_gh_repo_owner, local_gh_repo_name):
    local_csv_data = []
    try:
        # Request
        tmp_gh_query = queries.auditRepoQuery.replace("#OWNER#", local_gh_repo_owner).replace("#REPOSITORY#", str(local_gh_repo_name))
        request = requests.post("https://github.com/api/graphql", json={'query': tmp_gh_query}, headers=headers)
        response = request.json()["data"]
        collaborators = response["repository"]["collaborators"]["edges"]
        nextPage = response["repository"]["collaborators"]["pageInfo"]["hasNextPage"]
        pageEnd = response["repository"]["collaborators"]["pageInfo"]["endCursor"]
 
        for c in collaborators:
            print("{0},{1},{2},{3},{4},{5}".format(local_gh_repo_owner, local_gh_repo_name, c["node"]["name"], c["node"]["login"], c["node"]["email"], c["permission"]))
            local_csv_data.append([local_gh_repo_owner, local_gh_repo_name, c["node"]["name"], c["node"]["login"], c["node"]["email"], c["permission"]])
       
        while (nextPage == True):
            # Request
            tmp_gh_query = queries.auditRepoQueryPagination.replace("#OWNER#", local_gh_repo_owner).replace("#REPOSITORY#", str(local_gh_repo_name)).replace("#PAGE#", pageEnd)
            request = requests.post("https://github.com/api/graphql", json={'query': tmp_gh_query}, headers=headers)
            response = request.json()["data"]
            collaborators = response["repository"]["collaborators"]["edges"]
            nextPage = response["repository"]["collaborators"]["pageInfo"]["hasNextPage"]
            pageEnd = response["repository"]["collaborators"]["pageInfo"]["endCursor"]
 
            for c in collaborators:
                print("{0},{1},{2},{3},{4},{5}".format(local_gh_repo_owner, local_gh_repo_name, c["node"]["name"], c["node"]["login"], c["node"]["email"], c["permission"]))
                local_csv_data.append([local_gh_repo_owner, local_gh_repo_name, c["node"]["name"], c["node"]["login"], c["node"]["email"], c["permission"]])
           
    except:
        print("Error retrieving ACL for {0}/{1}".format(local_gh_repo_owner, str(local_gh_repo_name)))
   
    return local_csv_data
 
####################################################################
# Audit Report - Create GH ACL Report in CSV file                 #
####################################################################
 
csv_data = []
 
####################################################################
# Decision Maker - Decide and execute a specific use case          #
####################################################################
# For use case
if (useCase == "team"):
    csv_data = situation_audit_team(gh_organization, gh_team)
    csv_header = ['org', 'team', 'name', 'login', 'role']
elif (useCase == "org"):
    csv_data = situation_audit_org(gh_organization, gh_repo_owner, gh_repo_name)
    csv_header = ['org_name', 'repository', 'collaborators']
elif (useCase == "repo"):
    csv_data = situation_audit_repo(gh_repo_owner, gh_repo_name)
    csv_header = ['owner_name', 'repository', 'user_name', 'user_login', 'user_email', 'permission']
elif(useCase == "user"):
    csv_data = situation_audit_user(gh_user)
    csv_header = ['user', 'repository', 'permission']
 
####################################################################
# CSV Parsing/Writing File                                         #
####################################################################
   
current_datetime = date.today().strftime("%b-%d-%Y")
csv_filename = "gh-acl-{0}-{1}.csv".format(useCase, current_datetime)
 
with open(csv_filename, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
 
    # write the header
    writer.writerow(csv_header)
 
    # write multiple rows
    writer.writerows(csv_data)