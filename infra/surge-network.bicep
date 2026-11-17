@allowed(['eastus2'])
param location string = 'eastus2'

var tags = {
  'azd-env-name': 'allclear-surge-20261117'
  'solution-accelerator': 'all-clear'
  purpose: 'audience-surge-private-connectivity'
}

resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2023-11-15' existing = {
  name: 'allclear-sbuqtpuppifra-cosmos'
}

resource logs 'Microsoft.OperationalInsights/workspaces@2022-10-01' existing = {
  name: 'allclear-sbuqtpuppifra-logs'
}

resource vnet 'Microsoft.Network/virtualNetworks@2023-11-01' = {
  name: 'allclear-surge-private-vnet'
  location: location
  tags: tags
  properties: {
    addressSpace: {
      addressPrefixes: ['10.77.0.0/16']
    }
    subnets: [
      {
        name: 'container-apps'
        properties: {
          addressPrefix: '10.77.0.0/23'
          delegations: [
            {
              name: 'container-apps'
              properties: {
                serviceName: 'Microsoft.App/environments'
              }
            }
          ]
        }
      }
      {
        name: 'private-endpoints'
        properties: {
          addressPrefix: '10.77.2.0/27'
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
    ]
  }
}

resource cosmosDns 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.documents.azure.com'
  location: 'global'
  tags: tags
}

resource cosmosDnsLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: cosmosDns
  name: 'allclear-surge-private-link'
  location: 'global'
  properties: {
    registrationEnabled: false
    virtualNetwork: {
      id: vnet.id
    }
  }
}

resource cosmosEndpoint 'Microsoft.Network/privateEndpoints@2023-11-01' = {
  name: 'allclear-surge-cosmos-pe'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: '${vnet.id}/subnets/private-endpoints'
    }
    privateLinkServiceConnections: [
      {
        name: 'cosmos-sql'
        properties: {
          privateLinkServiceId: cosmos.id
          groupIds: ['Sql']
        }
      }
    ]
  }
}

resource cosmosDnsGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-11-01' = {
  parent: cosmosEndpoint
  name: 'cosmos-sql'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'cosmos-sql'
        properties: {
          privateDnsZoneId: cosmosDns.id
        }
      }
    ]
  }
}

resource environment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: 'allclear-surge-private-env'
  location: location
  tags: tags
  properties: {
    vnetConfiguration: {
      infrastructureSubnetId: '${vnet.id}/subnets/container-apps'
      internal: false
    }
    workloadProfiles: [
      {
        name: 'Consumption'
        workloadProfileType: 'Consumption'
      }
    ]
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logs.properties.customerId
        sharedKey: logs.listKeys().primarySharedKey
      }
    }
  }
}

output environmentName string = environment.name
output environmentId string = environment.id
output cosmosPrivateEndpointId string = cosmosEndpoint.id
output vnetId string = vnet.id
