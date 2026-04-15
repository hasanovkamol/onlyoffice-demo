namespace WebApi.Models;

public class OnlyOfficeSettings
{
    public string DocumentServerUrl { get; set; } = string.Empty;
    public string JwtSecret { get; set; } = string.Empty;
    public string CallbackUrl { get; set; } = string.Empty;
    public string DownloadUrl { get; set; } = string.Empty;
}
