# Projeto Integrador - Modelo
# MetFlix


Um modelo para o desenvolvimento do Projeto Integrador do Curso de Técnico em Desenvolvimento de Sistemas para a Internet Integrado ao Ensino Médio do IFC - Campus Araquari.

O projeto MetFlix tem como objetivo o desenvolvimento de uma plataforma web para automatizar o processo de locação de filmes e séries de uma locadora.A proposta é criar um sistema completo que permita o gerenciamento do acervo de mídias, cadastro de clientes, controle de empréstimos e devoluções, aplicação de multas por atraso e geração de relatórios estratégicos. 

Professor: [Marco André Mendes](github.com/marcoandre)

Equipe:
- [Deivid Leonardo Mendes da Silva](https://github.com/deivid1801)
- [Brayan Pedroso de Mattos](https://github.com/brayanpedroso)

Links do projeto:
-   [Documentação (esse documento)](github.com/marcoandre/pi-modelo)
-   Backend: [Repositório](github.com/marcoandre/pi-backend) e [Publicação](https://pi-backend.herokuapp.com/)
-   Frontend: [Repositório](github.com/marcoandre/pi-frontend) e [Publicação](https://pi-frontend.herokuapp.com/)



# **1.1.2 Empréstimo**

O projeto MetFlix foi baseado no modelo de sistema de Empréstimo, pois a proposta consiste em desenvolver uma plataforma de locação de mídias (filmes e séries), cujo funcionamento é semelhante ao de uma biblioteca: o cliente realiza um empréstimo (locação), com data prevista para devolução, podendo sofrer penalidades em caso de atraso.

# 2. Situação‑Problema

A MetFlix é uma locadora de filmes e séries que enfrenta dificuldades operacionais devido à falta de um sistema informatizado. Atualmente, todo o controle de estoque, locações, pagamentos e multas é feito manualmente, por meio de planilhas e anotações em papel. Isso gera erros frequentes, atrasos no atendimento, perda de dados importantes e retrabalho para os funcionários.

Além disso, não há histórico integrado de clientes, as promoções não são aplicadas automaticamente e os relatórios gerenciais são imprecisos e demorados. Esses problemas afetam diretamente a eficiência da equipe e a experiência do cliente.

Um sistema de gerenciamento digital é essencial para automatizar os processos, melhorar o controle do acervo e das locações, garantir a aplicação correta de regras e promoções, e oferecer relatórios confiáveis em tempo real.


# 3. Descrição da Proposta

Será desenvolvido um sistema web responsivo para a MetFlix, com foco na automação de todo o processo de locação de mídias: desde o cadastro de clientes e títulos até devoluções, cobranças e geração de relatórios.

O sistema contará com três tipos de usuários:

- Administrador: gerencia o catálogo, planos de assinatura e acessa relatórios.

- Atendente: realiza locações, devoluções e registra pagamentos.

- Cliente: acessa o catálogo online, faz reservas e consulta seu histórico.

As funcionalidades principais incluem:

- Cadastro e login de clientes e funcionários

- Controle de estoque e locações

- Cálculo de multas e geração automática de boletos

- Reservas online para membros

- Painéis de indicadores com dados em tempo real

- A plataforma vai padronizar os processos da empresa, reduzir o tempo de atendimento e oferecer dados estratégicos para apoiar o crescimento da MetFlix.

# 4. Modelagem de Dados
![Modelagem de Dados](https://raw.githubusercontent.com/deivid1801/MetFlix/3674ce7ebcad097cddc09f1dab4e3d807089baba/docs/Modelagem%20MetFlix.png)







## 4. 📌 Regras de Negócio

**RN01. Cadastro único de CPF e e-mail**  
Cada cliente deve ter um CPF e e-mail únicos no sistema.  
Cada funcionário deve ter um e-mail único.

**RN02. Tipos de usuário**  
Existem três tipos de usuários:
- **Administrador:** acesso total ao sistema.
- **Atendente:** apenas operações de atendimento (locações, devoluções, pagamentos).
- **Cliente:** apenas consultas, reservas e histórico próprio.

**RN03. Planos de assinatura**  
Um cliente deve estar vinculado a um plano (ex.: `BASICO`, `PADRAO`, `PREMIUM`) que pode restringir:
- Quantidade de mídias simultâneas
- Tipo de mídia (ex.: `DIGITAL` só para planos avançados)  
*(Essas restrições devem ser definidas nas regras internas do sistema, com base nas políticas da empresa.)*

**RN04. Controle de estoque**  
A quantidade de uma mídia disponível deve ser reduzida ao realizar uma locação e aumentada ao registrar a devolução.  
Não é permitido locar uma mídia com quantidade igual a zero.

**RN05. Devolução e cálculo de multa**  
Caso a data de devolução seja posterior à data prevista, deve ser calculada uma multa por dia de atraso.  
O valor da multa deve ser armazenado na tabela `Locacao_Midia`.

**RN06. Pagamento obrigatório para finalização**  
Uma locação só será considerada fechada após o registro do pagamento (aluguel e, se houver, multa).

**RN07. Reservas**  
Apenas clientes ativos e logados podem fazer reservas.  
O sistema deve permitir uma reserva por título por cliente enquanto o status estiver como `pendente`.  
Reservas vencidas ou não convertidas em locações dentro de um prazo definido (ex.: 24h) devem ser automaticamente canceladas.

**RN08. Inativação lógica**  
Clientes, mídias e funcionários não devem ser excluídos fisicamente do banco, mas marcados como `ativo = 0`.

**RN09. Histórico de locações e reservas**  
O cliente pode acessar apenas seu próprio histórico.  
O atendente pode acessar o histórico de qualquer cliente.

**RN10. Acesso por perfil**  
Cada funcionalidade do sistema deve ser acessível apenas pelos perfis autorizados:
- **Administrador:** tudo
- **Atendente:** locação, devolução, pagamento, consulta
- **Cliente:** consulta, reserva, histórico pessoal

**RN11. Geração de relatórios**  
Os relatórios devem ser gerados apenas por administradores e conter dados como:
- Quantidade de locações por período
- Mídias mais locadas
- Faturamento mensal
- Inadimplência

---

## 5. ✅ Requisitos Funcionais

**RF01. Cadastro de Usuários**  
O sistema deve permitir o cadastro de clientes e funcionários, bem como suas respectivas contas de acesso.

**RF02. Autenticação e Acesso**  
Login com autenticação por senha, com acesso controlado por tipo de usuário.

**RF03. Gerenciamento de Mídias**  
Cadastro, edição e ativação/desativação de mídias. Controle de estoque baseado em locações e devoluções.

**RF04. Gerenciamento de Gêneros**  
Cadastro e edição de gêneros de mídia.

**RF05. Locação de Mídias**  
Registro de locações e devoluções com atualização de estoque e datas.

**RF06. Cálculo e Registro de Multas**  
Cálculo de multas por atraso e armazenamento na tabela `Locacao_Midia`.

**RF07. Pagamento**  
Registro de pagamentos (aluguel e multa), com data e método.

**RF08. Reservas Online**  
Clientes podem consultar o catálogo e fazer reservas; atendentes podem converter ou cancelar reservas.

**RF09. Consulta de Histórico**  
Clientes acessam seu próprio histórico; atendentes podem consultar históricos de qualquer cliente.

**RF10. Gerenciamento de Planos**  
Administradores podem gerenciar os planos de assinatura disponíveis.

**RF11. Painéis e Relatórios**  
Administradores acessam dashboards com dados em tempo real e relatórios exportáveis (PDF/Excel).

**RF12. Controle de Acesso**  
O sistema deve restringir funcionalidades com base no perfil do usuário.

---

## 6. ⚙️ Requisitos Não Funcionais

**RNF01. Interface Web Responsiva**  
Compatível com desktop e dispositivos móveis.

**RNF02. Desempenho**  
Deve suportar pelo menos 50 usuários simultâneos sem degradação significativa.

**RNF03. Segurança**  
- Senhas criptografadas
- Controle de roles/permissões
- Prevenção contra SQL Injection e XSS

**RNF04. Disponibilidade**  
Disponibilidade de 99,9% do tempo, exceto manutenções planejadas.

**RNF05. Escalabilidade**  
Arquitetura modular ou orientada a microserviços, permitindo expansão futura.

**RNF06. Conformidade**  
Adequação à LGPD (Lei Geral de Proteção de Dados).

**RNF07. Portabilidade**  
Deve rodar em servidores Linux e ambientes Docker.

**RNF08. Manutenibilidade**  
Código com documentação clara e cobertura de testes automatizados.

