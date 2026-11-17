@allowed(['eastus2'])
param location string = 'eastus2'

@description('Disable to bootstrap identities and roles before image-pull permission propagation')
param deployApps bool = true

@secure()
@minLength(1)
param surgeCoachKey string

@description('Immutable backend image from the audience-owned registry')
param backendImage string = 'allclearsbuqtpuppifraacr.azurecr.io/backend@sha256:10299ea6bb99b2108ce270203a614ea09ff373aadccd61d366680cd681f59be4'

@description('Immutable frontend image from the audience-owned registry')
param frontendImage string = 'allclearsbuqtpuppifraacr.azurecr.io/frontend@sha256:9162e709edc41b9f7ef9865444d394dde4bd3e494b787019400c3c7ff69ac32d'

var tags = {
  'azd-env-name': 'allclear-surge-20261117'
  'solution-accelerator': 'all-clear'
  purpose: 'audience-surge-private-connectivity'
}
var openAiUserRole = '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'
var acrPullRole = '7f951dda-4ed3-4680-a7ca-43fe172d538d'
var cosmosContributorRole = '00000000-0000-0000-0000-000000000002'

resource environment 'Microsoft.App/managedEnvironments@2024-03-01' existing = {
  name: 'allclear-surge-private-env'
}
resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2023-11-15' existing = {
  name: 'allclear-sbuqtpuppifra-cosmos'
}
resource openAi 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' existing = {
  name: 'allclear-sbuqtpuppifra-openai'
}
resource search 'Microsoft.Search/searchServices@2023-11-01' existing = {
  name: 'allclear-sbuqtpuppifra-search'
}
resource registry 'Microsoft.ContainerRegistry/registries@2023-07-01' existing = {
  name: 'allclearsbuqtpuppifraacr'
}

resource backendIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'allclear-surge-backend-identity'
  location: location
  tags: tags
}
resource frontendIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'allclear-surge-frontend-identity'
  location: location
  tags: tags
}

resource backendOpenAiRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(openAi.id, backendIdentity.id, openAiUserRole)
  scope: openAi
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', openAiUserRole)
    principalId: backendIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}
resource backendCosmosRole 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2023-11-15' = {
  parent: cosmos
  name: guid(cosmos.id, backendIdentity.id, cosmosContributorRole)
  properties: {
    roleDefinitionId: '${cosmos.id}/sqlRoleDefinitions/${cosmosContributorRole}'
    principalId: backendIdentity.properties.principalId
    scope: '${cosmos.id}/dbs/allclear'
  }
}
resource backendAcrRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(registry.id, backendIdentity.id, acrPullRole)
  scope: registry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', acrPullRole)
    principalId: backendIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}
resource frontendAcrRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(registry.id, frontendIdentity.id, acrPullRole)
  scope: registry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', acrPullRole)
    principalId: frontendIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource backend 'Microsoft.App/containerApps@2024-03-01' = if (deployApps) {
  name: 'allclear-surge-live-backend'
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${backendIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: environment.id
    workloadProfileName: 'Consumption'
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        allowInsecure: false
        targetPort: 8000
        transport: 'auto'
      }
      registries: [
        {
          server: registry.properties.loginServer
          identity: backendIdentity.id
        }
      ]
      secrets: [
        {
          name: 'surge-coach-key'
          value: surgeCoachKey
        }
        {
          name: 'search-api-key'
          value: search.listAdminKeys().primaryKey
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'backend'
          image: backendImage
          env: [
            {
              name: 'MOCK_MODE'
              value: 'false'
            }
            {
              name: 'AZURE_CLIENT_ID'
              value: backendIdentity.properties.clientId
            }
            {
              name: 'AZURE_OPENAI_ENDPOINT'
              value: openAi.properties.endpoint
            }
            {
              name: 'AZURE_OPENAI_DEPLOYMENT'
              value: 'gpt-5.1'
            }
            {
              name: 'AZURE_OPENAI_EMBEDDING_DEPLOYMENT'
              value: 'text-embedding-3-small'
            }
            {
              name: 'AZURE_OPENAI_API_VERSION'
              value: 'preview'
            }
            {
              name: 'AZURE_COSMOS_ENDPOINT'
              value: cosmos.properties.documentEndpoint
            }
            {
              name: 'AZURE_COSMOS_DATABASE'
              value: 'allclear'
            }
            {
              name: 'AZURE_SEARCH_ENDPOINT'
              value: 'https://${search.name}.search.windows.net'
            }
            {
              name: 'AZURE_SEARCH_KEY'
              secretRef: 'search-api-key'
            }
            {
              name: 'AZURE_SEARCH_INDEX'
              value: 'knowledge-base'
            }
            {
              name: 'SURGE_COACH_KEY'
              secretRef: 'surge-coach-key'
            }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
    }
  }
  dependsOn: [
    backendOpenAiRole
    backendCosmosRole
    backendAcrRole
  ]
}

resource frontend 'Microsoft.App/containerApps@2024-03-01' = if (deployApps) {
  name: 'allclear-surge-live-frontend'
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${frontendIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: environment.id
    workloadProfileName: 'Consumption'
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        allowInsecure: false
        targetPort: 80
        transport: 'auto'
      }
      registries: [
        {
          server: registry.properties.loginServer
          identity: frontendIdentity.id
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'frontend'
          image: frontendImage
          env: [
            {
              name: 'BACKEND_URL'
              value: deployApps ? 'https://${backend!.properties.configuration.ingress.fqdn}' : ''
            }
          ]
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
    }
  }
  dependsOn: [frontendAcrRole]
}

output backendUrl string = deployApps ? 'https://${backend!.properties.configuration.ingress.fqdn}' : ''
output frontendUrl string = deployApps ? 'https://${frontend!.properties.configuration.ingress.fqdn}' : ''
output backendIdentityPrincipalId string = backendIdentity.properties.principalId
