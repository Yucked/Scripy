$WebhookUrl = $args[0]
$JobStatus = $args[1]
$Context = $env:GITHUB | ConvertFrom-Json

if (!$WebhookUrl) {
  Write-Output "Webhook URL is missing. Please make sure a valid Webhook URL is provided."
  Exit
}

Switch ($JobStatus) {
  "success" {
    $EmbedColor = 10288950
    $Thumbnail = "https://imgur.com/lwqJqWO.png"
    Break
  }
  "failure" {
    $EmbedColor = 15739727
    $Thumbnail = "https://imgur.com/6OnouMH.png"
    Break
  }
  "cancelled" {
    $EmbedColor = 10896639
    $Thumbnail = "https://imgur.com/lzM2lem.png"
    Break
  }
  default {
    $EmbedColor = 10896639
    $Thumbnail = "https://imgur.com/T70lZ64.png"
    Break
  }
}

$List = New-Object System.Collections.Generic.List[System.Object]
if ($Context.event_name -eq 'push'){
    $FieldName = "Commit(s) Information"
    foreach($Commit in $Context.event.commits){
        $CommitData = '{0}    -    {1}' -f $Commit.id.SubString(0, 7), $Commit.message
        $List.Add($CommitData)
    }
    $FieldValue = '```{0}```' -f [system.String]::Join("`r`n", $List)
}
ElseIf ($Context.event_name -eq 'pull_request'){
    $FieldName = "Pull Request Information"
    $FieldValue = '```
Head       -    {0}
Base       -    {1}
Title      -    {2}
Files      -    {3}
Commits    -    {4}

{5}
```' -f $Context.head_ref, $Context.base_ref, $Context.event.pull_request.title, ` 
        $Context.event.pull_request.changed_files, $Context.event.pull_request.commits, `
        $Context.event.pull_request.body
}

$Webhook = @{
    username = "Cooking Boi"
    avatar_url = "https://imgur.com/dtkN2W6.png"
    embeds = @(
        @{
        title = "GitHub Actions finished building $($Context.repository)!"
        url = "https://github.com/$($Context.repository)"
        color = $EmbedColor
        description = "$Data"
        fields = @(
            @{
                name = "Build Information"
                value = 
                '```
Number     -   {0}
Workflow   -   {1}
Sha        -   {2}```' -f $Context.run_number, $Context.workflow, $Context.sha
            }
            @{
                name = "$FieldName"
                value = "$FieldValue"                
            }
        )
        author = @{
            name = "$($Context.actor)"
            icon_url = "https://avatars.githubusercontent.com/$($Context.actor)"
        }
        timestamp = "$(Get-Date -UFormat '+%Y-%m-%dT%H:%M:%S.000Z')"
        thumbnail = @{
            url = $Thumbnail
        }
      }
   )
}

$Json = ConvertTo-Json $Webhook -Depth 100
Invoke-RestMethod -Uri "$WebhookUrl" -Method "POST" -UserAgent "GitHub Actions" `
  -ContentType "application/json" -Header @{"X-Author"="Yucked"} -Body $Json
