
# Ferramentas

Versões utilizadas 

- python 3.8.10

# Setup

- Criar ambiente virtual: `python -m venv env`.
- Toda vez que for rodar o projeto é importante garantir que o ambiente virtual está ativo. Para isso, rodar: `.\env\Scripts\Activate.ps1` (se estiver utilizando powershell)
- Instalar dependências: `pip install -r requirements.txt`

# Populando o banco de dados

- Como o sistema depende de muitos dados, existe um script para iniciar entradas no banco de dados. Para executá-lo, rode: `python manage.py populate_db`

# Rodar o projeto

- Garantir que o ambiente virtual está ativo. Se não estiver: `.\env\Scripts\Activate.ps1` (se estiver utilizando powershell)
- `cd backend`
- Se as migrations não tiverem sido aplicadas: `python manage.py migrate`
- Rodar a aplicação `python manage.py runserver`

# Usuário administrador

- Para criar um usuário admin, execute `python manage.py createsuperuser` e complete o fluxo 
# Instalando novas dependências

Não se esqueça de atualizar o `requirements.txt` após instalar dependências com o pip. Para fazer isso, rode ` pip freeze > "requirements.txt"`