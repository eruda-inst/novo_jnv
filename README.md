# JNV Web(Nome a ser alterado)

O JNV tem o propósito de ser um agregador e gerenciador universal de infraestrutura de redes, unificando e facilitando o acesso a equipamentos como OLTs, Switches e Roteadores.

Atualmente o JNV é um sistema de terminal que integra com OLTs Fiberhome e Datacom. Não possui muitos recursos e roda de forma localmente.

O JNV Web poderá ser instalado na nuvem, porém uma vpn terá que ser configurada para que seja possível a comunicação com os equipamentos na rede.


A baixo temos um fluxograma do funcionamento do sistema
> Estágio atual: MVP

````mermaid
flowchart TD
    A((Início)) --> B[Autenticação]
    B --> C[Homepage]
    C --> D[Equipamentos]
    C --> E[Usuários]
    D --> F[Cadastro de equipamentos]
    D --> G[Lista de equipamentos]
    G --> GA[Ver configurações de equipamento]
    subgraph GrupoEquip[" "]
        direction LR
        GB[Ver especificidades do equipamento] -.- OBS[Cada tipo de equipamento tem observações diferentes, como iniciaremos com OLT todas as observaçòes serão idênticas]
    end
    G --> GrupoEquip

