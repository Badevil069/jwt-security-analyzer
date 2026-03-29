# Add this to your PowerShell profile ($PROFILE)
# To find your profile location, run: echo $PROFILE
# To edit it, run: notepad $PROFILE

function jwt {
    & "c:\Users\abhia\jwt-analyzer\jwt.bat" @args
}

# Also add these helpful aliases
Set-Alias -Name jwtanalyzer -Value jwt
