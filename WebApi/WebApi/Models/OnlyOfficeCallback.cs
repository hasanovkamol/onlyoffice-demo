using System.Text.Json.Serialization;

namespace WebApi.Models;

public class OnlyOfficeCallback
{
    [JsonPropertyName("key")]
    public string Key { get; set; } = string.Empty;

    [JsonPropertyName("status")]
    public int Status { get; set; }

    [JsonPropertyName("url")]
    public string? Url { get; set; }

    [JsonPropertyName("users")]
    public List<string>? Users { get; set; }

    [JsonPropertyName("history")]
    public object? History { get; set; }

    [JsonPropertyName("token")]
    public string? Token { get; set; }
}
