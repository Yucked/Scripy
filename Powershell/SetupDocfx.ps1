$Repo = ${env:GITHUB_REPOSITORY} -split '/'
$RepoName = $Repo[1]

Write-Output dir
Write-Output 'Downloading latest release of docfx ...'
$response = Invoke-RestMethod -Uri 'https://api.github.com/repos/dotnet/docfx/releases'
$latest = $response[0].assets

if (!$latest) {
    Write-Output 'GitHub response changed. Please update script.'
    return
}


Invoke-WebRequest $latest.browser_download_url -OutFile ./docfx.zip
Write-Output 'Extracting docfx.zip to docfx ...'
Expand-Archive ./docfx.zip -DestinationPath ./docfx

Write-Output 'Setting docfx variable ..'
$env:Path += ";/home/runner/work/docfx/"

Write-Output "Copying $($Repo)"
Copy-Item $RepoName 'Pages'

Write-Output 'Building docs ...'
cd 'docs'
docfx build
