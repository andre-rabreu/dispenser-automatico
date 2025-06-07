# Dispenser Automatizado para Alimentação de Pets com Agendamento via Bluetooth

## Conceito/Descrição do Projeto

O projeto propõe o desenvolvimento de um dispositivo automatizado de alimentação para pets, como cães e gatos, com foco em praticidade e autonomia. Utilizando um motor de passo (28BYJ-48) controlado por um microcontrolador Raspberry Pi Pico, o sistema é capaz de liberar porções de ração de forma precisa. A ativação pode ser feita manualmente via conexão Bluetooth (HC-05), através de um aplicativo ou terminal no celular, ou ainda por agendamento baseado no tempo real fornecido por um módulo RTC (DS1307). O dispositivo é alimentado por um conversor AC/DC 5V e conta com feedback visual por LED para indicar funcionamento. Voltado para uso doméstico, o projeto visa auxiliar tutores na alimentação regular dos animais, mesmo quando estão ausentes ou com rotina corrida, promovendo bem-estar e previsibilidade na rotina alimentar dos pets.

## Requisitos de sistema
| Código | Requisito                                                                                   | Tipo        |
|--------|---------------------------------------------------------------------------------------------|-------------|
| UR-01  | Utilizar módulos de fácil acesso e baixo custo, como Raspberry Pi Pico, HC-05 e RTC DS1307 | Obrigatório |
| UR-02  | Permitir controle remoto do dispenser via Bluetooth por meio de comandos simples de texto   | Obrigatório |
| UR-03  | Realizar acionamento imediato do motor para liberar ração quando solicitado pelo usuário     | Obrigatório |
| UR-04  | Permitir agendamento de horários específicos para ativação do motor com base no RTC         | Obrigatório |
| UR-05  | Executar a rotina de alimentação automaticamente no horário programado                      | Obrigatório |
| UR-06  | Exibir feedback visual por LED durante o acionamento do motor                               | Obrigatório |
| UR-07  | Restaurar o estado do sistema em caso de desconexão Bluetooth, mantendo agendamentos válidos| Obrigatório |
| UR-08  | Permitir múltiplos agendamentos ordenados por horário                                       | Desejável   |
| UR-09  | Oferecer um menu interativo via Bluetooth para facilitar o uso por pessoas sem conhecimento técnico | Desejável   |
| UR-10  | Garantir segurança no acionamento do motor, evitando sobreposição de comandos simultâneos   | Desejável   |
| UR-11  | Funcionar com alimentação elétrica contínua via fonte 5V                                    | Obrigatório |
| UR-12  | Permitir atualização ou reprogramação do firmware com facilidade                            | Desejável   |

## Diagrama de blocos
<img src="https://i.imgur.com/HB8CYCo.png" width="512">

## Demonstração
Clique na imagem para acessar o vídeo.

<a href="https://www.youtube.com/shorts/5-v-bV1ZpnA" title="Link do YouTube">
<img src="https://i.imgur.com/a80q2SJ.png" width="512">
</a>

## Autores
André Renato Almeida Abreu

<img src="https://i.imgur.com/s7CEaK1.jpeg" width="256">