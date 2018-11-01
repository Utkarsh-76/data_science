param($a,$b
);
$filePath = $a
    $wd = New-Object -ComObject Word.Application
$wd.Visible = $false
$txt = $wd.Documents.Open($filePath, $false, $true)

$txt.SaveAs([REF]$b)
$txt.Close()
$wd.Application.Quit()