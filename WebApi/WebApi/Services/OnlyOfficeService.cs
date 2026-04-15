using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using System.Linq;
using Microsoft.Extensions.Options;

using Microsoft.IdentityModel.Tokens;
using WebApi.Models;

namespace WebApi.Services;

public interface IOnlyOfficeService
{
    string CreateToken(object payload);
    bool ValidateToken(string token, out JwtSecurityToken? jwtToken);
}

public class OnlyOfficeService : IOnlyOfficeService
{
    private readonly OnlyOfficeSettings _settings;

    public OnlyOfficeService(IOptions<OnlyOfficeSettings> settings)
    {
        _settings = settings.Value;
    }

    public string CreateToken(object payload)
    {
        var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_settings.JwtSecret));
        var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

        var header = new JwtHeader(credentials);
        
        var payloadJson = System.Text.Json.JsonSerializer.Serialize(payload);
        var payloadDictionary = System.Text.Json.JsonSerializer.Deserialize<Dictionary<string, object>>(payloadJson);
        
        var payloadData = new JwtPayload();
        if (payloadDictionary != null)
        {
            foreach (var item in payloadDictionary)
            {
                payloadData[item.Key] = ConvertJsonElement(item.Value);
            }
        }

        var token = new JwtSecurityToken(header, payloadData);
        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    private object? ConvertJsonElement(object? element)
    {
        if (element is System.Text.Json.JsonElement jsonElement)
        {
            return jsonElement.ValueKind switch
            {
                System.Text.Json.JsonValueKind.String => jsonElement.GetString(),
                System.Text.Json.JsonValueKind.Number => jsonElement.TryGetInt64(out long l) ? l : jsonElement.GetDouble(),
                System.Text.Json.JsonValueKind.True => true,
                System.Text.Json.JsonValueKind.False => false,
                System.Text.Json.JsonValueKind.Object => System.Text.Json.JsonSerializer.Deserialize<Dictionary<string, object>>(jsonElement.GetRawText())
                                                            ?.ToDictionary(k => k.Key, v => ConvertJsonElement(v.Value)),
                System.Text.Json.JsonValueKind.Array => jsonElement.EnumerateArray().Select(e => ConvertJsonElement(e)).ToList(),
                _ => null
            };
        }
        return element;
    }



    public bool ValidateToken(string token, out JwtSecurityToken? jwtToken)
    {
        jwtToken = null;
        try
        {
            var tokenHandler = new JwtSecurityTokenHandler();
            var key = Encoding.UTF8.GetBytes(_settings.JwtSecret);
            tokenHandler.ValidateToken(token, new TokenValidationParameters
            {
                ValidateIssuerSigningKey = true,
                IssuerSigningKey = new SymmetricSecurityKey(key),
                ValidateIssuer = false,
                ValidateAudience = false,
                ClockSkew = TimeSpan.Zero
            }, out SecurityToken validatedToken);

            jwtToken = (JwtSecurityToken)validatedToken;
            return true;
        }
        catch
        {
            return false;
        }
    }
}
