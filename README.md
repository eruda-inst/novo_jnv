# novo_jnv
Nova versão do JNV, agora WEB.

````mermaid
flowchart TD
    A((Início)) --> B[Autenticação]
    B --> C[Homepage]
    C --> D[Equipamentos]
    C --> E[Usuários]
    D --> F[Cadastro de equipamentos]
    D --> G[Lista de equipamentos]
    G --> GA[Ver configurações de equipamento]
    G --> GB[Ver especificidades do equipamento]
    subgraph espeficidades_de_equipamentos[" "]
        direction LR
        GB -.- OBS[Cada tipo de equipamento tem observações diferentes, como iniciaremos com OLT todas as observaçòes serão idênticas]
    end

