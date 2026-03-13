$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Net.Http

[Console]::InputEncoding  = [Text.Encoding]::UTF8
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

$sessionId = "s_utf8"
$apiUrl = "http://127.0.0.1:8000/chat"
$msgPath = ".\msg.txt"
$logPath = ".\chat_log.txt"

# 读取所有行（UTF-8），保留顺序；过滤空行/纯空白
$lines = Get-Content -Path $msgPath -Encoding UTF8 | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }

if (-not $lines -or $lines.Count -eq 0) {
    Write-Host "No non-empty lines found in msg.txt"
    exit 0
}

$client = New-Object System.Net.Http.HttpClient
$client.Timeout = [TimeSpan]::FromSeconds(120)

# 可选：清理旧日志
# Remove-Item $logPath -ErrorAction SilentlyContinue

$index = 0
foreach ($line in $lines) {
    $index++

    $bodyObj = @{
        session_id = $sessionId
        user_text  = $line
    }
    $bodyJson = $bodyObj | ConvertTo-Json -Compress
    $content  = New-Object System.Net.Http.StringContent($bodyJson, [Text.Encoding]::UTF8, "application/json")

    Write-Host ""
    Write-Host ("[{0}/{1}] >>> USER: {2}" -f $index, $lines.Count, $line)

    $resp = $client.PostAsync($apiUrl, $content).Result
    $status = [int]$resp.StatusCode

    # 按 UTF-8 读字节
    $bytes = $resp.Content.ReadAsByteArrayAsync().Result
    $raw   = [Text.Encoding]::UTF8.GetString($bytes)

    Write-Host ("Status: {0}" -f $status)
    Write-Host ("Raw: {0}" -f $raw)

    # 解析 JSON（若失败就只输出 raw）
    $replyText = $null
    try {
        $json = $raw | ConvertFrom-Json
        if ($json.reply) {
            $replyText = [string]$json.reply
            Write-Host ("<<< AI: {0}" -f $replyText)
        } elseif ($json.detail) {
            Write-Host ("<<< ERROR detail: {0}" -f $json.detail)
        }
    } catch {
        Write-Host "<<< (Non-JSON response or decode failed)"
    }

    # 追加写入日志（可选）
    $ts = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    Add-Content -Path $logPath -Encoding UTF8 -Value "[$ts] USER: $line"
    if ($replyText) {
        Add-Content -Path $logPath -Encoding UTF8 -Value "[$ts] AI:   $replyText"
    } else {
        Add-Content -Path $logPath -Encoding UTF8 -Value "[$ts] RAW:  $raw"
    }

    # 如果遇到非 2xx，可以选择中断或继续
    if ($status -lt 200 -or $status -ge 300) {
        Write-Host "Stopping due to non-2xx status."
        break
    }
}

$client.Dispose()
Write-Host ""
Write-Host "Done. Log written to $logPath"
