using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using WebApi.Models;
using WebApi.Services;
using System.Net.Http;

namespace WebApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class DocumentsController : ControllerBase
{
    private readonly OnlyOfficeSettings _settings;
    private readonly IOnlyOfficeService _onlyOfficeService;
    private readonly IWebHostEnvironment _environment;
    private readonly ILogger<DocumentsController> _logger;

    public DocumentsController(
        IOptions<OnlyOfficeSettings> settings,
        IOnlyOfficeService onlyOfficeService,
        IWebHostEnvironment environment,
        ILogger<DocumentsController> logger)
    {
        _settings = settings.Value;
        _onlyOfficeService = onlyOfficeService;
        _environment = environment;
        _logger = logger;
    }

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

        var config = new
        {
            document = new
            {
                fileType = fileExtension,
                key = Guid.NewGuid().ToString().Substring(0, 8),
                title = fileName,
                url = $"{_settings.DownloadUrl}/{fileName}"
            },
            documentType = documentType,
            editorConfig = new
            {
                callbackUrl = $"{_settings.CallbackUrl}?fileName={fileName}",
                lang = "ru",
                user = new
                {
                    id = "1",
                    name = "Demo User"
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
        if (string.IsNullOrEmpty(fileName)) fileName = "demo.docx";

        _logger.LogInformation("OnlyOffice Callback received for {FileName}. Status: {Status}", fileName, body.Status);

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
                    using var httpClient = new HttpClient();
                    var response = await httpClient.GetAsync(body.Url);
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

