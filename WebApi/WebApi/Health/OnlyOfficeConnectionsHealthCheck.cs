using Microsoft.Extensions.Diagnostics.HealthChecks;
using WebApi.Services;

namespace WebApi.Health;

public class OnlyOfficeConnectionsHealthCheck : IHealthCheck
{
    private readonly IActiveSessionService _sessionService;

    public OnlyOfficeConnectionsHealthCheck(IActiveSessionService sessionService)
    {
        _sessionService = sessionService;
    }

    public Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken cancellationToken = default)
    {
        var count = _sessionService.GetTotalActiveConnections();
        var sessions = _sessionService.GetActiveSessions();

        var data = new Dictionary<string, object>
        {
            { "TotalConnections", count },
            { "ActiveDocuments", sessions }
        };

        return Task.FromResult(HealthCheckResult.Healthy($"Active Connections: {count}", data));
    }
}
