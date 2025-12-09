# Script para configurar o repositório Git

# Inicializar repositório Git (se não existir)
if (-not (Test-Path .git)) {
    Write-Host "Inicializando repositório Git..." -ForegroundColor Yellow
    git init
}

# Remover remote origin se já existir
git remote remove origin 2>$null

# Adicionar o novo remote
Write-Host "Adicionando repositório remoto..." -ForegroundColor Yellow
git remote add origin https://github.com/JoaoAmpeze/Trabalho_final_lfa.git

# Verificar configuração
Write-Host "`nRepositório remoto configurado:" -ForegroundColor Green
git remote -v

Write-Host "`nPróximos passos:" -ForegroundColor Cyan
Write-Host "1. git add ." -ForegroundColor White
Write-Host "2. git commit -m 'Initial commit'" -ForegroundColor White
Write-Host "3. git branch -M main" -ForegroundColor White
Write-Host "4. git push -u origin main" -ForegroundColor White

