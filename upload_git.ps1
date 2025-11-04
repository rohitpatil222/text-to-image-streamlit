# ===============================
# 🚀 Auto GitHub Uploader Script
# Author: Rohit Patil (rohitpatil222)
# ===============================

# Ask for inputs
$zipPath = Read-Host "Enter full path of your ZIP file (e.g. E:\Downloads\Downloads\text-to-image-streamlit.zip)"
$repoName = Read-Host "Enter new GitHub repo name (e.g. text-to-image-streamlit)"
$repoVisibility = Read-Host "Enter repo visibility (public/private) [default: public]"
if ([string]::IsNullOrWhiteSpace($repoVisibility)) { $repoVisibility = "public" }

$githubUsername = "rohitpatil222"

Write-Host "`n🚀 Starting upload for '$repoName' as $githubUsername..." -ForegroundColor Cyan

# === 1. Extract ZIP ===
$extractPath = "$env:TEMP\$repoName"
if (Test-Path $extractPath) { Remove-Item $extractPath -Recurse -Force }
Expand-Archive -Path $zipPath -DestinationPath $extractPath
Write-Host "✅ Extracted project to: $extractPath"

# === 2. Move into project ===
Set-Location $extractPath

# === 3. Initialize Git ===
if (!(Test-Path ".git")) {
    git init | Out-Null
    Write-Host "✅ Initialized new Git repository"
}

# === 4. Add and commit files ===
git add .
git commit -m "Initial commit" | Out-Null
Write-Host "📝 Created initial commit"

# === 5. Check GitHub CLI ===
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️ GitHub CLI not found! Install it from https://cli.github.com/ and run 'gh auth login'" -ForegroundColor Yellow
    exit
}

# === 6. Create or link repo ===
$repoExists = gh repo view "$githubUsername/$repoName" 2>$null
if ($repoExists) {
    Write-Host "📂 Repo already exists. Linking to local repo..."
    git remote add origin "https://github.com/$githubUsername/$repoName.git" 2>$null
} else {
    Write-Host "🌐 Creating new GitHub repo..."
    gh repo create $repoName --$repoVisibility --source=. --remote=origin --push
    Write-Host "🚀 Repository created and uploaded successfully!"
    exit
}

# === 7. Push to GitHub ===
git branch -M main
git push -u origin main | Out-Null
Write-Host "`n✅ Successfully uploaded project!" -ForegroundColor Green
Write-Host "🌍 URL: https://github.com/$githubUsername/$repoName" -ForegroundColor Cyan
