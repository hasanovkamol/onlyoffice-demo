using System.Collections.Concurrent;

namespace WebApi.Services;

public interface IActiveSessionService
{
    void UpdateSession(string fileName, List<string> users);
    int GetTotalActiveConnections();
    Dictionary<string, int> GetActiveSessions();
}

public class ActiveSessionService : IActiveSessionService
{
    // Key: FileName, Value: List of User IDs
    private readonly ConcurrentDictionary<string, HashSet<string>> _activeUsers = new();

    public void UpdateSession(string fileName, List<string> users)
    {
        if (users == null || !users.Any())
        {
            _activeUsers.TryRemove(fileName, out _);
        }
        else
        {
            _activeUsers[fileName] = [.. users];
        }
    }

    public int GetTotalActiveConnections()
    {
        return _activeUsers.Values.Sum(u => u.Count);
    }

    public Dictionary<string, int> GetActiveSessions()
    {
        return _activeUsers.ToDictionary(k => k.Key, v => v.Value.Count);
    }
}
