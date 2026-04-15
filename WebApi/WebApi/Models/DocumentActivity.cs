using System.ComponentModel.DataAnnotations;

namespace WebApi.Models;

public class DocumentActivity
{
    [Key]
    public int Id { get; set; }
    
    [Required]
    public string FileName { get; set; } = string.Empty;
    
    [Required]
    public string UserId { get; set; } = string.Empty;
    
    public int Status { get; set; }
    
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    
    public string? DownloadUrl { get; set; }
}
