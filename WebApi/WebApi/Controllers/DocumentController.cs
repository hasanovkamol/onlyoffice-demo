using Microsoft.AspNetCore.Mvc;
using System.Text.Json;

namespace WebApi.Controllers;

[ApiController]
[Route("api/[controller]/[action]")]
public class DocumentController : Controller
{
    private readonly string _storagePath = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "documents");

    [HttpGet("download/{fileName}")]
    public IActionResult DownloadFile(string fileName)
    {
        var filePath = Path.Combine(_storagePath, fileName);
        if (!System.IO.File.Exists(filePath)) return NotFound();

        var fileBytes = System.IO.File.ReadAllBytes(filePath);
        // OnlyOffice uchun MIME turi muhim
        return File(fileBytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", fileName);
    }

    [HttpPost("callback")]
    public async Task<IActionResult> Callback([FromBody] JsonElement body)
    {
        // 1. Statusni olish (status: 1)
        int status = body.GetProperty("status").GetInt32();

        // 2. Kalitni olish (key: "Kh-612456")
        string key = body.GetProperty("key").GetString();

        // 3. Foydalanuvchilar ro'yxatini olish (users: ["789"])
        var users = body.GetProperty("users").EnumerateArray();
        foreach (var user in users)
        {
            string userId = user.GetString();
            Console.WriteLine($"Foydalanuvchi: {userId}");
        }

        // 4. Action turi (actions: [{ "type": 1, ... }])
        var actions = body.GetProperty("actions").EnumerateArray();
        if (actions.Any())
        {
            int actionType = actions.First().GetProperty("type").GetInt32();
            // type 1: Foydalanuvchi ulandi
            // type 2: Foydalanuvchi uzildi
        }

        // Statusga qarab qaror qabul qilamiz
        switch (status)
        {
            case 1:
                Console.WriteLine($"Hujjat ochildi. Key: {key}");
                break;
            case 2:
                Console.WriteLine("Hujjat saqlashga tayyor!");
                // Bu yerda yuqoridagi 'url' orqali saqlash kodini yozasiz
                break;
        }

        return Ok(new { error = 0 });
    }

}
