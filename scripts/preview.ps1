param(
    [switch]$Build,
    [int]$Port = 4000
)

$ErrorActionPreference = 'Stop'
$repositoryPath = Split-Path -Parent $PSScriptRoot
$portableRuby = Join-Path $repositoryPath 'local\runtime\rubyinstaller-3.3.10-1-x64\bin\ruby.exe'
$previousPath = $env:PATH

Push-Location $repositoryPath
try {
    if (Test-Path -LiteralPath $portableRuby) {
        $rubyExecutable = $portableRuby
        $rubyBin = Split-Path -Parent $portableRuby
        $env:PATH = $rubyBin + ';' + $env:PATH
    } else {
        $rubyExecutable = (Get-Command ruby -ErrorAction Stop).Source
        $rubyBin = Split-Path -Parent $rubyExecutable
    }

    $bundleScript = Join-Path $rubyBin 'bundle'
    if (-not (Test-Path -LiteralPath $bundleScript)) {
        throw 'Bundler was not found. Install Bundler for your Ruby runtime first.'
    }

    & $rubyExecutable $bundleScript check
    if ($LASTEXITCODE -ne 0) {
        throw 'Dependencies are missing. Run bundle config set --local path local/gems and bundle install first.'
    }

    if ($Build) {
        & $rubyExecutable -rbundler/setup -e "load Gem.bin_path('jekyll', 'jekyll')" -- build --safe --strict_front_matter
    } else {
        & $rubyExecutable -rbundler/setup -e "load Gem.bin_path('jekyll', 'jekyll')" -- serve --host 127.0.0.1 --port $Port --livereload
    }
    if ($LASTEXITCODE -ne 0) { throw ('Jekyll failed with exit code ' + $LASTEXITCODE) }
} finally {
    $env:PATH = $previousPath
    Pop-Location
}
