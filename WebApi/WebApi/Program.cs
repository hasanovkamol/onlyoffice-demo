using WebApi.Models;
using WebApi.Services;
using WebApi.Middleware;
using WebApi.Health;
using WebApi.Data;
using Microsoft.EntityFrameworkCore;
using Serilog;

using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using HealthChecks.UI.Client;

var builder = WebApplication.CreateBuilder(args);

// Serilog configuration
Log.Logger = new LoggerConfiguration()
    .ReadFrom.Configuration(builder.Configuration)
    .Enrich.FromLogContext()
    .CreateLogger();

builder.Host.UseSerilog();

// Database Context
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("PostgreSQL")));

// Sessiyalarni kuzatish servisi
builder.Services.AddSingleton<IActiveSessionService, ActiveSessionService>();

// Health Checks
builder.Services.AddHealthChecks()
    .AddNpgSql(builder.Configuration.GetConnectionString("PostgreSQL")!)
    .AddRabbitMQ(name: builder.Configuration.GetConnectionString("RabbitMQ")!)
    .AddUrlGroup(new Uri("http://onlyoffice_ds/healthcheck"), name: "OnlyOffice Docs")


    .AddCheck<OnlyOfficeConnectionsHealthCheck>("OnlyOffice Active Connections");

// Configuration
builder.Services.Configure<OnlyOfficeSettings>(builder.Configuration.GetSection("OnlyOffice"));

// Services
builder.Services.AddScoped<IOnlyOfficeService, OnlyOfficeService>();

builder.Services.AddControllers();
builder.Services.AddOpenApi();

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

// Avtomatik migratsiya (Database yaratish)
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    db.Database.Migrate(); // Migratsiyalarni qo'llash
}


if (app.Environment.IsDevelopment())
{

    app.MapOpenApi();
}

app.UseStaticFiles();
app.UseMiddleware<CorrelationIdMiddleware>();
app.UseCors("AllowAll");

app.UseAuthorization();

app.MapControllers();
app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});

try
{
    Log.Information("Starting web application");
    app.Run();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Application terminated unexpectedly");
}
finally
{
    Log.CloseAndFlush();
}



