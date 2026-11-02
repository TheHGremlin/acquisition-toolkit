# Open a workbook in Excel, recalculate, save (so formula results are cached for later readers),
# and optionally export the whole workbook to PDF for a visual check.
# Windows only (needs Excel installed). Usage: powershell -NoProfile -ExecutionPolicy Bypass -File excel_refresh.ps1 -Path <xlsx> [-Pdf <pdf>]
param([Parameter(Mandatory = $true)][string]$Path, [string]$Pdf)
$full = (Resolve-Path $Path).Path
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$xl.DisplayAlerts = $false
try {
    $wb = $xl.Workbooks.Open($full)
    $xl.CalculateFull()
    foreach ($ws in $wb.Worksheets) {
        $ws.PageSetup.Orientation = 2          # landscape
        $ws.PageSetup.Zoom = $false
        $ws.PageSetup.FitToPagesWide = 1
        $ws.PageSetup.FitToPagesTall = $false
    }
    $wb.Save()
    if ($Pdf) { $wb.ExportAsFixedFormat(0, [System.IO.Path]::GetFullPath($Pdf)) }
    $wb.Close($false)
    "refreshed $full"
} finally {
    $xl.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
}
