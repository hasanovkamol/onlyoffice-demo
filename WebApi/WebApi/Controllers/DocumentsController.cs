using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using WebApi.Models;
using WebApi.Services;
using WebApi.Data;

namespace WebApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class DocumentsController(
    IOptions<OnlyOfficeSettings> settings,
    IOnlyOfficeService onlyOfficeService,
    IActiveSessionService sessionService,
    ApplicationDbContext db,
    IWebHostEnvironment environment,
    ILogger<DocumentsController> logger) : ControllerBase
{
    private readonly OnlyOfficeSettings _settings = settings.Value;
    private readonly IOnlyOfficeService _onlyOfficeService = onlyOfficeService;
    private readonly IActiveSessionService _sessionService = sessionService;
    private readonly ApplicationDbContext _db = db; // Database Context
    private readonly IWebHostEnvironment _environment = environment;
    private readonly ILogger<DocumentsController> _logger = logger;

    [HttpGet("config/{fileName}")]
    public IActionResult GetConfig(string fileName)
    {
        var fileExtension = Path.GetExtension(fileName).ToLower().TrimStart('.');
        var documentType = fileExtension switch
        {
            "docx" or "doc" or "txt" or "rtf" or "odt" => "word",
            "xlsx" or "xls" or "csv" or "ods" => "cell",
            "pptx" or "ppt" or "odp" => "slide",
            _ => "word"
        };

        string userId=Guid.NewGuid().ToString();

        // Hujjat kaliti fayl uchun bir xil bo'lishi shart (birga ishlash uchun)
        // Fayl nomidan yoki faylning o'zgarish vaqtidan kalit yasaladi. 
        var documentKey = fileName.GetHashCode().ToString("x");

        var config = new
        {
            document = new
            {
                fileType = fileExtension,
                key = documentKey,
                title = fileName,
                url = $"{_settings.DownloadUrl}/{fileName}"
            },

            documentType = documentType,
            editorConfig = new
            {
                // callbackUrl ga userId parametrini qo'shamiz
                callbackUrl = $"{_settings.CallbackUrl}?fileName={fileName}&userId={userId}",
                lang = "ru",
                user = new
                {
                    id = userId,
                    name = userId == "1" ? "Admin User" : $"User {userId}"
                },
                customization = new {
                    forcesave = true
                }
            }
        };

        var token = _onlyOfficeService.CreateToken(config);

        return Ok(new
        {
            config = config,
            token = token
        });
    }

    [HttpGet("download/{fileName}")]
    public IActionResult Download(string fileName)
    {
        _logger.LogInformation("Attempting to download file: {FileName}", fileName);
        
        var filePath = Path.Combine(_environment.WebRootPath, "documents", fileName);
        if (!System.IO.File.Exists(filePath))
        {
            _logger.LogWarning("File not found for download: {FileName}. Path: {FilePath}", fileName, filePath);
            return NotFound();
        }

        var fileBytes = System.IO.File.ReadAllBytes(filePath);
        _logger.LogInformation("File {FileName} ({Size} bytes) successfully served for download", fileName, fileBytes.Length);
        
        return File(fileBytes, "application/octet-stream", fileName);
    }

    [HttpPost("callback")]
    public async Task<IActionResult> Callback([FromBody] OnlyOfficeCallback body)
    {
        var fileName = Request.Query["fileName"].ToString();
        var triggerUserId = Request.Query["userId"].ToString();

        // Sessiyani yangilash
        if (body.Users != null)
        {
            _sessionService.UpdateSession(fileName, body.Users);
        }

        // Bazaga tarixni saqlash
        var activity = new DocumentActivity
        {
            FileName = fileName,
            UserId = triggerUserId,
            Status = body.Status,
            DownloadUrl = body.Url,
            CreatedAt = DateTime.UtcNow
        };
        _db.DocumentActivities.Add(activity);
        await _db.SaveChangesAsync();

        _logger.LogInformation("OnlyOffice Callback for {FileName}. Saved to DB. User: {UserId}. Status: {Status}", 
            fileName, triggerUserId, body.Status);



        // Hujjat ustida ishlayotgan barcha userlar ro'yxati
        if (body.Users != null && body.Users.Any())
        {
            _logger.LogInformation("Active users on document {FileName}: {Users}", 
                fileName, string.Join(", ", body.Users));
        }


        // JWT Validation
        string? token = body.Token;
        if (HttpContext.Request.Headers.TryGetValue("Authorization", out var authHeader))
        {
            var headerValue = authHeader.ToString();
            if (headerValue.StartsWith("Bearer ", StringComparison.OrdinalIgnoreCase))
            {
                token = headerValue.Substring(7);
            }
        }

        if (string.IsNullOrEmpty(token) || !_onlyOfficeService.ValidateToken(token, out _))
        {
            _logger.LogWarning("Invalid or missing OnlyOffice JWT token in callback for {FileName}", fileName);
        }

        switch (body.Status)
        {
            case 1: // Document is being edited
                _logger.LogInformation("Document {FileName} is being edited by: {Users}", fileName, string.Join(", ", body.Users ?? new List<string>()));
                break;
            case 2: // Document is ready for saving
            case 6: // Document is being edited, but is saved
                _logger.LogInformation("Document {FileName} is ready to be saved. Download URL: {Url}", fileName, body.Url);
                
                if (string.IsNullOrEmpty(body.Url))
                {
                    _logger.LogError("Callback status {Status} received but URL is null for {FileName}", body.Status, fileName);
                    return BadRequest();
                }

                try
                {
                    // Docker ichki tarmog'i uchun URLni qayta quramiz:
                    // Hostni 'onlyoffice_ds' ga va portni standart 80 ga majburlaymiz
                    var uriBuilder = new UriBuilder(body.Url)
                    {
                        Host = "onlyoffice_ds",
                        Port = -1 // Standart port (HTTP bo'lsa 80, HTTPS bo'lsa 443)
                    };
                    var downloadUrl = uriBuilder.ToString();

                    _logger.LogInformation("Downloading updated file from: {DownloadUrl} (Original: {OriginalUrl})", downloadUrl, body.Url);

                    using var httpClient = new HttpClient();
                    var response = await httpClient.GetAsync(downloadUrl);
                    if (response.IsSuccessStatusCode)
                    {
                        var fileBytes = await response.Content.ReadAsByteArrayAsync();
                        var filePath = Path.Combine(_environment.WebRootPath, "documents", fileName);
                        
                        await System.IO.File.WriteAllBytesAsync(filePath, fileBytes);
                        _logger.LogInformation("File {FileName} successfully updated and saved. Size: {Size} bytes", fileName, fileBytes.Length);
                    }
                    else
                    {
                        _logger.LogError("Failed to download updated file from OnlyOffice. Status: {StatusCode}", response.StatusCode);
                    }
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Exception occurred while saving file {FileName} from OnlyOffice callback", fileName);
                    return BadRequest();
                }
                break;
            case 4: // Document is closed with no changes
                _logger.LogInformation("Document {FileName} was closed without changes", fileName);
                break;
            default:
                _logger.LogDebug("Received unhandled OnlyOffice callback status {Status} for {FileName}", body.Status, fileName);
                break;
        }

        return Ok(new { error = 0 });
    }
}

