# Digitador

Simulador de digitação que lê um texto da interface e simula teclas no computador.
Serve para testes, demonstrações e automação simples de entrada de texto.

## Como funciona

* Cole um texto no campo principal
* Clique em Iniciar
* Você tem dez segundos para focar a janela alvo
* O programa começa a digitar caractere por caractere
* Para interromper use o botão Parar ou a tecla ESC
* Os arquivos `shiftmap.json` e `writemap.json` permitem ajustar como certos caracteres são digitados
* O programa registra eventos no arquivo `digitador.log`

## Requisitos

* Python 3.10 ou superior
* Windows recomendado
  Em macOS e Linux pode ser preciso conceder permissões de acessibilidade para simular teclas
* Bibliotecas Python

  * `pyautogui`
  * `keyboard`

## Instalação

1. Clone ou baixe este repositório

2. Crie um ambiente virtual

   Windows PowerShell

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Windows CMD

   ```cmd
   python -m venv .venv
   .\.venv\Scripts\activate.bat
   ```

   Linux ou macOS

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências

   ```bash
   pip install pyautogui keyboard
   ```

4. Rode o app

   ```bash
   python digitador.py
   ```

## Uso

1. Abra o programa
2. Cole o texto na caixa
3. Clique em Iniciar
4. Em até dez segundos leve o foco para a janela onde o texto deve ser digitado
5. Para interromper use o botão Parar ou a tecla ESC

Atalhos

* ESC interrompe a digitação

## Arquivos de configuração

O app lê dois arquivos opcionais na mesma pasta do executável ou do script.

### writemap.json

Lista de caracteres que serão digitados pelo método `keyboard.write`, útil para símbolos que não funcionam bem com `pyautogui.press`.

Exemplo

```json
[
  "á",
  "é",
  "í",
  "ó",
  "ú",
  "ç"
]
```

### shiftmap.json

Mapa de caracteres que precisam de SHIFT com uma tecla base.
Chave é o caractere desejado. Valor é a tecla que será pressionada junto com SHIFT.

Exemplo

```json
{
  "{": "[",
  "}": "]",
  ":": ";",
  "\"": "'",
  "|": "\\",
  "<": ",",
  ">": ".",
  "?": "/",
  "!": "1",
  "@": "2",
  "#": "3",
  "$": "4",
  "%": "5",
  "^": "6",
  "&": "7",
  "*": "8",
  "(": "9",
  ")": "0"
}
```

Observação

* Se o caractere estiver em `writemap.json`, este método tem prioridade
* Se o caractere for maiúsculo, o app usa SHIFT com a letra minúscula
* Enter Tab e espaço têm tratamento dedicado

## Comportamento de pausas

* Após espaço ou enter o atraso fica entre 0.1 e 0.2 segundos
* Entre demais caracteres o atraso fica entre 0.03 e 0.15 segundos
* Esses valores simulam digitação humana

## Log

O arquivo `digitador.log` registra

* Início e fim de digitação
* Interrupções
* Erros ao digitar caracteres
* Carregamento dos arquivos JSON

## Geração de executável no Windows

A forma mais simples é usar PyInstaller.

1. Instale o PyInstaller no ambiente virtual

   ```bash
   pip install pyinstaller
   ```

2. Gere o executável em arquivo único

   ```bash
   pyinstaller --onefile --noconsole --name Digitador ^
     --add-data "shiftmap.json;." ^
     --add-data "writemap.json;." ^
     digitador.py
   ```

   Explicação

   * `--onefile` cria um arquivo único
   * `--noconsole` oculta o console
   * `--add-data` inclui os JSON na mesma pasta interna do app
     No Windows use ponto e vírgula no separador
     Em Linux ou macOS troque por dois pontos
     Exemplo Linux ou macOS

     ```bash
     pyinstaller --onefile --noconsole --name Digitador \
       --add-data "shiftmap.json:." \
       --add-data "writemap.json:." \
       digitador.py
     ```

3. Pegue o executável em `dist/Digitador.exe`

4. Caso queira ícone personalizado
   Coloque um `.ico` no projeto e rode

   ```bash
   pyinstaller --onefile --noconsole --name Digitador --icon app.ico digitador.py
   ```

5. Distribuição
   Copie apenas `Digitador.exe`
   Se preferir manter os JSON do lado de fora para fácil edição, não use `--add-data` e deixe `shiftmap.json` e `writemap.json` na mesma pasta do `.exe`

## Dicas e solução de problemas

* Se a tecla ESC não interromper pode ser falta de permissão de teclado global
  Em Windows rode como administrador
* Em macOS permita controle do computador nas preferências de segurança
* Layout do teclado pode afetar o `shiftmap.json`
  Ajuste as teclas base conforme seu layout
* Se certos caracteres falharem adicione ao `writemap.json`
* Colar textos muito longos aumenta o tempo total
  Use Parar ou ESC para cancelar
* Em alguns antivírus pode ser preciso criar uma exceção para o executável gerado

## Segurança

O app simula teclas no sistema
Evite usar enquanto digita senhas
Use apenas em ambientes controlados

## Estrutura do código

* `carregar_writemap` lê `writemap.json`
* `carregar_combinacoes` lê `shiftmap.json`
* `carregar_jsons` chama as duas funções
* `digitar_texto` faz o loop de digitação com pausas naturais e tratamento por tipo de caractere
* `iniciar_digitação` cria a thread de digitação e mostra o aviso dos dez segundos
* `parar_digitação` sinaliza interrupção
* `monitorar_tecla_esc` escuta a tecla ESC em loop
* Interface feita com Tkinter usando uma caixa de texto e três botões
