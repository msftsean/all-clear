// University Front Door Support Agent - Azure Infrastructure
// Deploy with: azd provision

@description('Name prefix for all resources')
param resourcePrefix string = 'frontdoor'

@description('Location for all resources')
param location string = resourceGroup().location

@description('Dedicated location for Cosmos DB when regional capacity is constrained')
param cosmosLocation string = 'canadacentral'

@description('Dedicated location for AI Search when regional capacity is constrained')
param searchLocation string = 'eastus'

@description('Azure OpenAI chat deployment model (All Clear runs on gpt-5.1 only)')
param openAiModel string = 'gpt-5.1'

@description('OpenAI chat model version')
param openAiModelVersion string = '2025-11-13'

@description('Azure OpenAI embedding deployment model (required for RouterExecutor dedup)')
param embeddingModel string = 'text-embedding-3-small'

@description('OpenAI embedding model version')
param embeddingModelVersion string = '1'

@description('Realtime model name')
param realtimeModel string = 'gpt-realtime'

@description('Realtime model version')
param realtimeModelVersion string = '2025-08-28'

@description('Region for the realtime OpenAI account (realtime models are not available in eastus)')
param realtimeLocation string = 'swedencentral'

@description('Enable mock mode (no external service connections)')
param mockMode bool = false

@description('Deployment timestamp for tagging')
param deploymentDate string = utcNow('yyyy-MM-dd')

// Naming convention
var resourceToken = toLower(uniqueString(subscription().id, resourceGroup().id, location))
var prefix = '${resourcePrefix}-${resourceToken}'
var keyVaultName = take(replace('${resourcePrefix}${resourceToken}kv', '-', ''), 24)
var cosmosToken = toLower(uniqueString(subscription().id, resourceGroup().id, cosmosLocation))
var cosmosAccountName = '${resourcePrefix}-${cosmosToken}-cosmos'

// Tags for all resources
var tags = {
  'azd-env-name': resourcePrefix
  'solution-accelerator': 'university-front-door-agent'
  'deployment-date': deploymentDate
}

// ============================================================================
// Azure OpenAI
// ============================================================================
resource openAi 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: '${prefix}-openai'
  location: location
  tags: tags
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: '${prefix}-openai'
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: true  // Managed identity only - no API key auth
  }
}

resource openAiDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = {
  parent: openAi
  name: openAiModel
  properties: {
    model: {
      format: 'OpenAI'
      name: openAiModel
      version: openAiModelVersion
    }
  }
  sku: {
    name: 'GlobalStandard'
    capacity: 5
  }
}

resource openAiEmbeddingDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = {
  parent: openAi
  name: embeddingModel
  dependsOn: [openAiDeployment]
  properties: {
    model: {
      format: 'OpenAI'
      name: embeddingModel
      version: embeddingModelVersion
    }
  }
  sku: {
    name: 'Standard'
    capacity: 50
  }
}

// Separate OpenAI account for the Realtime model. Realtime models (gpt-realtime)
// are NOT available in eastus, so this account lives in realtimeLocation
// (default swedencentral). The backend uses AZURE_OPENAI_REALTIME_ENDPOINT to
// reach it for voice (A1) and phone (A2) while chat/embeddings stay on the
// primary eastus account.
resource openAiRealtime 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: '${prefix}-openai-rt'
  location: realtimeLocation
  tags: tags
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: '${prefix}-openai-rt'
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: true
  }
}

resource openAiRealtimeDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = {
  parent: openAiRealtime
  name: realtimeModel
  properties: {
    model: {
      format: 'OpenAI'
      name: realtimeModel
      version: realtimeModelVersion
    }
  }
  sku: {
    name: 'GlobalStandard'
    capacity: 10
  }
}

// ============================================================================
// Azure Cosmos DB
// ============================================================================
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2023-11-15' = if (!mockMode) {
  name: cosmosAccountName
  location: cosmosLocation
  tags: tags
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    enableFreeTier: false
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
    locations: [
      {
        locationName: cosmosLocation
        failoverPriority: 0
      }
    ]
  }
}

resource cosmosDatabase 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2023-11-15' = if (!mockMode) {
  parent: cosmosAccount
  name: 'frontdoor'
  properties: {
    resource: {
      id: 'frontdoor'
    }
  }
}

resource sessionsContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2023-11-15' = if (!mockMode) {
  parent: cosmosDatabase
  name: 'sessions'
  properties: {
    resource: {
      id: 'sessions'
      partitionKey: {
        paths: [
          '/student_id_hash'
        ]
        kind: 'Hash'
      }
      defaultTtl: 7776000 // 90 days
    }
  }
}

resource auditContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2023-11-15' = if (!mockMode) {
  parent: cosmosDatabase
  name: 'audit_logs'
  properties: {
    resource: {
      id: 'audit_logs'
      partitionKey: {
        paths: [
          '/timestamp'
        ]
        kind: 'Hash'
      }
    }
  }
}

// All Clear incidents store (spec 001 Clarification #2 / 016 FR-1).
// Partitioned by /intent_category — the dedup query scope (001 Clarification #1).
resource incidentsContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2023-11-15' = if (!mockMode) {
  parent: cosmosDatabase
  name: 'incidents'
  properties: {
    resource: {
      id: 'incidents'
      partitionKey: {
        paths: [
          '/intent_category'
        ]
        kind: 'Hash'
      }
    }
  }
}

// ============================================================================
// Azure AI Search
// ============================================================================
resource searchService 'Microsoft.Search/searchServices@2023-11-01' = {
  name: '${prefix}-search'
  location: searchLocation
  tags: tags
  sku: {
    // 'basic' (not 'free'): Azure allows only ONE free-tier search service per
    // subscription, which fails azd up with ServiceQuotaExceeded when the slot
    // is already taken (e.g. multiple hackathon teams in one subscription).
    name: 'basic'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
  }
}

// ============================================================================
// Azure Communication Services
// ============================================================================
resource acs 'Microsoft.Communication/communicationServices@2023-04-01' = {
  name: '${prefix}-acs'
  location: 'global'  // ACS is a global resource
  tags: tags
  properties: {
    dataLocation: 'unitedstates'  // Data residency
  }
}

// ============================================================================
// Azure Container Apps Environment
// ============================================================================
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: '${prefix}-logs'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource containerAppEnv 'Microsoft.App/managedEnvironments@2023-08-01-preview' = {
  name: '${prefix}-env'
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

// ============================================================================
// Azure Key Vault
// ============================================================================
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  tags: tags
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    accessPolicies: []
    enableRbacAuthorization: true
  }
}

// Store secrets
resource cosmosKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = if (!mockMode) {
  parent: keyVault
  name: 'cosmos-db-key'
  properties: {
    value: cosmosAccount.listKeys().primaryMasterKey
  }
}

resource searchKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'search-api-key'
  properties: {
    value: searchService.listAdminKeys().primaryKey
  }
}

resource acsConnectionStringSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'acs-connection-string'
  properties: {
    value: acs.listKeys().primaryConnectionString
  }
}

// ============================================================================
// Azure Container Registry
// ============================================================================
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: replace('${prefix}acr', '-', '')
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}

// ============================================================================
// Service Targets for azd deploy
// ============================================================================
resource backendContainerApp 'Microsoft.App/containerApps@2023-08-01-preview' = {
  name: '${prefix}-backend'
  location: location
  tags: union(tags, {
    'azd-service-name': 'backend'
  })
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
        transport: 'auto'
      }
      secrets: [
        {
          name: 'acr-password'
          value: containerRegistry.listCredentials().passwords[0].value
        }
        {
          name: 'cosmos-db-key'
          value: mockMode ? 'mock' : cosmosAccount.listKeys().primaryMasterKey
        }
        {
          name: 'search-api-key'
          value: searchService.listAdminKeys().primaryKey
        }
        {
          name: 'acs-connection-string'
          value: mockMode ? '' : acs.listKeys().primaryConnectionString
        }
      ]
      registries: [
        {
          server: containerRegistry.properties.loginServer
          username: containerRegistry.listCredentials().username
          passwordSecretRef: 'acr-password'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'backend'
          image: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
          env: [
            {
              name: 'MOCK_MODE'
              value: string(mockMode)
            }
            {
              name: 'AZURE_OPENAI_ENDPOINT'
              value: openAi.properties.endpoint
            }
            {
              name: 'AZURE_OPENAI_DEPLOYMENT'
              value: openAiDeployment.name
            }
            {
              name: 'AZURE_OPENAI_EMBEDDING_DEPLOYMENT'
              value: openAiEmbeddingDeployment.name
            }
            {
              name: 'AZURE_OPENAI_API_VERSION'
              // gpt-5.1 Responses API (/openai/v1/) accepts only "preview"; dated
              // versions return 400 (validated in 001-maf-rehost T13). The embedding
              // client pins its own dated GA version in code (dependencies.py).
              value: 'preview'
            }
            {
              name: 'AZURE_OPENAI_REALTIME_ENDPOINT'
              value: openAiRealtime.properties.endpoint
            }
            {
              name: 'AZURE_OPENAI_REALTIME_DEPLOYMENT'
              value: openAiRealtimeDeployment.name
            }
            {
              name: 'AZURE_COSMOS_ENDPOINT'
              value: mockMode ? '' : cosmosAccount.properties.documentEndpoint
            }
            {
              name: 'AZURE_COSMOS_KEY'
              secretRef: 'cosmos-db-key'
            }
            {
              name: 'AZURE_COSMOS_DATABASE'
              value: mockMode ? 'frontdoor' : cosmosDatabase.name
            }
            {
              name: 'AZURE_SEARCH_ENDPOINT'
              value: 'https://${searchService.name}.search.windows.net'
            }
            {
              name: 'AZURE_SEARCH_KEY'
              secretRef: 'search-api-key'
            }
            {
              name: 'AZURE_ACS_ENDPOINT'
              value: mockMode ? '' : 'https://${acs.properties.hostName}'
            }
            {
              name: 'AZURE_ACS_CONNECTION_STRING'
              secretRef: 'acs-connection-string'
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
        maxReplicas: 2
      }
    }
  }
}

// ============================================================================
// Role Assignments for Managed Identity
// ============================================================================

// Cognitive Services OpenAI User role definition ID (Azure built-in role)
var cognitiveServicesOpenAIUserRoleId = '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'

// Grant backend container app access to Azure OpenAI via managed identity
resource backendOpenAIRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(openAi.id, backendContainerApp.id, cognitiveServicesOpenAIUserRoleId)
  scope: openAi
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', cognitiveServicesOpenAIUserRoleId)
    principalId: backendContainerApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// Grant backend container app access to the realtime OpenAI account via managed identity
resource backendRealtimeOpenAIRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(openAiRealtime.id, backendContainerApp.id, cognitiveServicesOpenAIUserRoleId)
  scope: openAiRealtime
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', cognitiveServicesOpenAIUserRoleId)
    principalId: backendContainerApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// Grant backend container app Contributor access to ACS via managed identity
var acsContributorRoleId = 'b24988ac-6180-42a0-ab88-20f7382dd24c'
resource backendACSRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(acs.id, backendContainerApp.id, acsContributorRoleId)
  scope: acs
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', acsContributorRoleId)
    principalId: backendContainerApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// ============================================================================
// Frontend Container App
// ============================================================================
resource frontendContainerApp 'Microsoft.App/containerApps@2023-08-01-preview' = {
  name: '${prefix}-frontend'
  location: location
  tags: union(tags, {
    'azd-service-name': 'frontend'
  })
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 80
        transport: 'auto'
      }
      secrets: [
        {
          name: 'acr-password'
          value: containerRegistry.listCredentials().passwords[0].value
        }
      ]
      registries: [
        {
          server: containerRegistry.properties.loginServer
          username: containerRegistry.listCredentials().username
          passwordSecretRef: 'acr-password'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'frontend'
          image: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
          env: [
            {
              name: 'BACKEND_URL'
              value: 'https://${backendContainerApp.properties.configuration.ingress.fqdn}'
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
        maxReplicas: 2
      }
    }
  }
}

// ============================================================================
// Outputs for azd
// ============================================================================
output AZURE_OPENAI_ENDPOINT string = openAi.properties.endpoint
output AZURE_OPENAI_DEPLOYMENT string = openAiDeployment.name
output AZURE_OPENAI_EMBEDDING_DEPLOYMENT string = openAiEmbeddingDeployment.name
output AZURE_COSMOS_ENDPOINT string = mockMode ? '' : cosmosAccount.properties.documentEndpoint
output AZURE_COSMOS_DATABASE string = mockMode ? 'frontdoor' : cosmosDatabase.name
output AZURE_SEARCH_ENDPOINT string = 'https://${searchService.name}.search.windows.net'
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerRegistry.properties.loginServer
output AZURE_CONTAINER_ENV_ID string = containerAppEnv.id
output AZURE_CONTAINERAPP_URL string = 'https://${backendContainerApp.properties.configuration.ingress.fqdn}'
output AZURE_FRONTEND_URL string = 'https://${frontendContainerApp.properties.configuration.ingress.fqdn}'
output AZURE_RESOURCE_GROUP string = resourceGroup().name
output AZURE_KEY_VAULT_NAME string = keyVault.name
output AZURE_ACS_ENDPOINT string = mockMode ? '' : 'https://${acs.properties.hostName}'
output MOCK_MODE bool = mockMode
