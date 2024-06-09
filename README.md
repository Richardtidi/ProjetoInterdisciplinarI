
Sistema de Gerenciamento de Estoque para Campanhas Beneficentes
Este é um trabalho acadêmico com a intenção de criar um sistema de gerenciamento de estoque para campanhas beneficentes. O sistema foi desenvolvido para ser simples e fácil de usar, utilizando Python para criar um servidor local e SQLite como SGBD (Sistema de Gerenciamento de Banco de Dados) interno.

Funcionalidades
Criação de Usuário: Permite que novos usuários se cadastrem no sistema.
Login de Usuário: Permite que os usuários registrados façam login.
Cadastro de Itens: Permite que os usuários cadastrem novos itens no estoque informando o tipo da roupa, gênero, tamanho e quantidade.
Gerenciamento de Estoque: Permite a edição e remoção de itens cadastrados.
Edição de Perfil: Permite que os usuários editem suas informações de perfil, como nome completo, e-mail e senha.
Estoque Individualizado: Cada usuário tem acesso apenas ao seu próprio estoque. Para criar múltiplos estoques, é possível registrar novos usuários.
Como Testar o Sistema Localmente
Abrir o Terminal: Com o código do projeto aberto, abra o terminal.
Iniciar o Servidor: Digite o seguinte comando no terminal para iniciar o servidor local:
bash
Copiar código
python Projeto/Server.py
Acesso ao Sistema Online
O sistema está hospedado e funcional na plataforma Heroku. Para acessá-lo, utilize o seguinte link:
https://estoque-beneficente-60c39bd79215.herokuapp.com/

Instruções de Uso
1. Criar um Usuário
Na tela inicial do site, siga os seguintes passos para criar um novo usuário:

Clique em "Cadastre-se".
Preencha os campos requisitados e finalize o cadastro.
2. Fazer Login
Após criar o usuário, faça login no sistema:

Clique em "Fazer Login".
Insira suas credenciais (e-mail e senha) e faça login.
3. Cadastrar Novos Itens ao Estoque
Para adicionar novos itens ao estoque, siga os passos abaixo:

Clique em "Novo item".
Informe o tipo da roupa, o gênero, o tamanho e a quantidade.
Adicione quantos itens forem necessários.
4. Gerenciar Itens do Estoque
Para editar ou remover itens do estoque:

Clique em "Gerenciar estoque".
Na página de gerenciamento, você pode editar as informações dos itens clicando em "Editar".
Para remover um item, clique em "Remover".
5. Editar Perfil
Para editar as informações do seu perfil:

Clique em "Editar Perfil".
Altere o nome completo, o e-mail e/ou a senha conforme necessário.
Notas Adicionais
Cada estoque é individual e só pode ser acessado pelo usuário que o criou.
Se for necessária a criação de mais de um estoque, registre novos usuários conforme necessário.
Tecnologias Utilizadas
Python: Linguagem de programação utilizada para o desenvolvimento do servidor.
SQLite: Sistema de Gerenciamento de Banco de Dados utilizado.
Heroku: Plataforma de hospedagem onde o sistema está online.
Contribuição
Para contribuir com o projeto, por favor, siga estas etapas:

Faça um fork do repositório.
Crie um branch com a sua feature: git checkout -b minha-feature.
Commit suas mudanças: git commit -m 'Adiciona minha feature'.
Push para o branch: git push origin minha-feature.
Envie um pull request.

Esperamos que este sistema seja útil para gerenciar estoques em campanhas beneficentes, facilitando a organização e a distribuição de recursos. Se você tiver alguma dúvida ou sugestão, entre em contato conosco.

Desenvolvido por: Cássio Luiz, Ester Gonçalves, Lucas de Freitas, Petry Estevam e Richard Gabriel
