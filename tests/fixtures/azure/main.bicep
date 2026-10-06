targetScope = 'subscription'
resource diag 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'audit'
  properties: {
    logs: [ { category: 'Administrative', enabled: true } ]
  }
}
resource alert 'Microsoft.Insights/metricAlerts@2018-03-01' = {
  name: 'cpu'
}
resource vault 'Microsoft.RecoveryServices/vaults@2023-01-01' = {
  name: 'v'
}
