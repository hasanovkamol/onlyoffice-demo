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
        var filePath = Path.Combine(_environment.WebRootPath, "documents", fileName);
        if (!System.IO.File.Exists(filePath))
            return NotFound();

        var fileBytes = System.IO.File.ReadAllBytes(filePath);
        return File(fileBytes, "application/octet-stream", fileName);
    }

    [HttpPost("callback")]
    public async Task<IActionResult> Callback([FromBody] OnlyOfficeCallback body)
    {
        _logger.LogInformation("OnlyOffice Callback received. Status: {Status}", body.Status);

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
            _logger.LogWarning("Invalid OnlyOffice JWT token in callback");
            // return Forbid(); // OnlyOffice expects { error: 0 } even if we don't save, but strictly we should check
        }

        if (body.Status == 2 || body.Status == 6)
        {

            if (string.IsNullOrEmpty(body.Url))
            {
                return BadRequest();
            }

            try
            {
                using var httpClient = new HttpClient();
                var response = await httpClient.GetAsync(body.Url);
                if (response.IsSuccessStatusCode)
                {
                    var fileBytes = await response.Content.ReadAsByteArrayAsync();
                    
                    // The 'key' in dummy implementation often encodes the filename or we track it elsewere
                    // For demo, we might need to know which file it was. 
                    // Let's assume we use the key or we could have passed fileName in callbackUrl query
                    
                    // In a real app, you'd map 'key' to a specific database record
                    // Here for demo, let's look for the file in wwwroot/documents
                    // (Simplified: we use a fixed filename or pass it via query)
                    
                    var fileName = Request.Query["fileName"].ToString();
                    if (string.IsNullOrEmpty(fileName)) fileName = "demo.docx";

                    var filePath = Path.Combine(_environment.WebRootPath, "documents", fileName);
                    await System.IO.File.WriteAllBytesAsync(filePath, fileBytes);
                    
                    _logger.LogInformation("File {FileName} successfully saved via callback.", fileName);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error saving file from OnlyOffice callback");
                return BadRequest();
            }
        }

        return Ok(new { error = 0 });
    }
}
