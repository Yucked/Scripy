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
Set-Variable docfx 'docfx/'
Copy-Item 'Victoria' 'Pages'

cd Victoria/docs
docfx build
cd Pages
git checkout gh-pages
rm -rf .