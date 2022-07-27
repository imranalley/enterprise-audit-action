########################################################
# List all repos and permissions for org name provided #
########################################################
 
auditOrgQuery = """
{
    organization(login: "#ORG#") {
        repositories(first: 3) {
            pageInfo{
                startCursor
                hasNextPage
                endCursor
            }
            nodes {
                nameWithOwner
                collaborators(first: 3) {
                totalCount
                edges {
                    permission
                    node {
                        login
                        name
                        }
                    }
                }
            }
        }
    }
}
"""
 
auditOrgQueryPagination = """
{
    organization(login: "#ORG#") {
        repositories(first: 3, after:"#PAGE#") {
            pageInfo{
                startCursor
                hasNextPage
                endCursor
            }
            nodes {
                nameWithOwner
                collaborators(first: 3) {
                totalCount
                edges {
                    permission
                    node {
                        login
                        name
                        }
                    }
                }
            }
        }
    }
}
 
"""
#########################################################
# List all repos and permissions for team name provided #
#########################################################
 
auditTeamQuery = """
{
    organization(login: "#ORG#") {
        team(slug: "#TEAM#") {
            name
            members(first: 3) {
                pageInfo {
                    startCursor
                    hasNextPage
                    endCursor
                } totalCount  
                nodes {
                    name
                    login
                    email
                } edges {
                    role
                }
            }
            repositories(first: 3) {
                pageInfo {
                    endCursor
                }
            totalCount
            nodes {
                name
                }
            }
        }
    }
}
"""
 
auditTeamQueryPagination = """
{
    organization(login: "#ORG#") {
        team(slug: "#TEAM#") {
            name
            members(first: 3, after:"#PAGE#") {
                pageInfo {
                    startCursor
                    hasNextPage
                    endCursor
                } totalCount  
                nodes {
                    name
                    login
                    email
                } edges {
                    role
                }
            }
            repositories(first: 3) {
                pageInfo {
                    endCursor
                }
            totalCount
            nodes {
                name
                }
            }
        }
    }
}
"""
 
#######################################################
# List all repos and permissions of username provided #
#######################################################
 
auditUserQuery = """
{
    user(login: "#USER#") {
        login
        name
        email
        repositories(affiliations: [OWNER, ORGANIZATION_MEMBER, COLLABORATOR], first: 3, isFork: false, ownerAffiliations: [OWNER, ORGANIZATION_MEMBER, COLLABORATOR]) {
            pageInfo {
                startCursor
                hasNextPage
                endCursor
            } totalCount
            nodes {
                nameWithOwner
                viewerPermission
            }
        }
    }
}
"""
 
auditUserQueryPagination = """
{
    user(login: "#USER#") {
        login
        name
        email
        repositories(affiliations: [OWNER, ORGANIZATION_MEMBER, COLLABORATOR], first: 3, after:"#PAGE#", isFork: false, ownerAffiliations: [OWNER, ORGANIZATION_MEMBER, COLLABORATOR]) {
            pageInfo {
                startCursor
                hasNextPage
                endCursor
            } totalCount
            nodes {
                nameWithOwner
                viewerPermission
            }
        }
    }
}
"""
 
#########################################################
# List user and permission level for repo name provided #
#########################################################
 
auditRepoQuery = """
{
    repository(owner:"#OWNER#", name:"#REPOSITORY#") {
        nameWithOwner
        collaborators(first: 10) {
            pageInfo {
                startCursor
                hasNextPage
                endCursor
            }
        totalCount
        edges {
            permission
            node {
                login
                name
                email
                }
            }
        }
    }
}
"""
 
auditRepoQueryPagination = """
{
    repository(owner:"#OWNER#", name:"#REPOSITORY#") {
        nameWithOwner
        collaborators(first: 10, after:"#PAGE#") {
            pageInfo {
                startCursor
                hasNextPage
                endCursor
            }
        totalCount
        edges {
            permission
            node {
                login
                name
                email
                }
            }
        }
    }
}
"""