# Monitoramento CPD

## Portal de monitoramento para parque misto de máquinas. Criado para auxiliar o trabalho de analistas de suporte.  
Possui os seguintes módulos:
### Workstation
Estações de trabalho, exibe o status de online ou offline através de PING

### Impressoras
Verifica status de online através de PING, além de raspagem da página web de monitoramento de impressoras modelos Lexmark MS811 (por enquanto, por enquanto, apenas esta) para exibir níveis de suprimentos e mensagem de status.  

## Módulos planejados

### Thinclients
Exibe status de online e permite enviar comandos via SSH (presume-se que são computadores GNU/Linux)

### PDVs
O mesmo para Thinclients, com a inclusão de comandos específicos relacionados a ponto de venda, como status e reinício de equipamentos conectados a máquina.

# Contribuições
Criado e desenvolvido por Richelmy Monteiro (gitlab @richmont1) e João Pedro Silva (gitlab @inpedro), utilizando de tecnologias backend (Django, Python) e frontend (Bootstrap, CSS, JS) para desenvolver este projeto em conjunto, com objetivo de otimizar rotinas e aprendizado prático.