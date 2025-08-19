import tkinter as tk
from tkinter import messagebox
import pyautogui
import threading
import time
import random
import keyboard
import json
import os
import logging

# Configuração do logging
logging.basicConfig(
    filename='digitador.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)

interromper = False
combinacoes_shift = {}
writemap = set()

def carregar_combinacoes():
    global combinacoes_shift
    if os.path.exists("shiftmap.json"):
        try:
            with open("shiftmap.json", "r", encoding="utf-8") as f:
                combinacoes_shift = json.load(f)
            messagebox.showinfo("ShiftMap Atualizado", "shiftmap.json recarregado com sucesso.")
            logging.info("shiftmap.json carregado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro ao ler shiftmap.json", str(e))
            logging.error(f"Erro ao carregar shiftmap.json: {e}")
            combinacoes_shift = {}
    else:
        messagebox.showerror("Arquivo faltando", "O arquivo 'shiftmap.json' não foi encontrado.")
        logging.warning("shiftmap.json não encontrado.")
        combinacoes_shift = {}

def carregar_writemap():
    global writemap
    if os.path.exists("writemap.json"):
        try:
            with open("writemap.json", "r", encoding="utf-8") as f:
                writemap = set(json.load(f))
            logging.info("writemap.json carregado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro ao ler writemap.json", str(e))
            logging.error(f"Erro ao carregar writemap.json: {e}")
            writemap = set()
    else:
        writemap = set()
        logging.warning("writemap.json não encontrado.")

def carregar_jsons():
    carregar_writemap()
    carregar_combinacoes()

def digitar_texto(texto):
    global interromper
    logging.info("Iniciando digitação...")
    time.sleep(10)

    for char in texto:
        if interromper:
            logging.info("Digitação interrompida pelo usuário.")
            break

        try:
            if char in writemap:
                keyboard.write(char)
            elif char in combinacoes_shift:
                tecla = combinacoes_shift[char]
                pyautogui.keyDown('shift')
                pyautogui.press(tecla)
                pyautogui.keyUp('shift')
            elif char.isupper():
                pyautogui.keyDown('shift')
                pyautogui.press(char.lower())
                pyautogui.keyUp('shift')
            elif char == '\n':
                pyautogui.press('enter')
            elif char == '\t':
                pyautogui.press('tab')
            elif char == ' ':
                pyautogui.press('space')
            else:
                pyautogui.press(char)
        except Exception as e:
            logging.warning(f"Falha ao digitar caractere '{char}': {e}")

        # pausa natural
        if char in [' ', '\n']:
            time.sleep(random.uniform(0.1, 0.2))  # pausa após espaço ou enter
        else:
            time.sleep(random.uniform(0.03, 0.15))  # pausa normal entre caracteres

    if not interromper:
        logging.info("Digitação concluída.")
    interromper = False

def iniciar_digitação():
    global interromper
    interromper = False
    texto = caixa_texto.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Aviso", "Cole algum texto antes de iniciar.")
        return
    carregar_jsons()
    messagebox.showinfo("Atenção", "Você tem 10 segundos para focar a janela. Pressione ESC ou clique em Parar para cancelar.")
    threading.Thread(target=digitar_texto, args=(texto,), daemon=True).start()

def parar_digitação():
    global interromper
    interromper = True
    logging.info("Botão Parar pressionado.")

def monitorar_tecla_esc():
    global interromper
    while True:
        keyboard.wait('esc')
        interromper = True
        logging.info("Tecla ESC pressionada. Interrompendo digitação.")

# Interface
janela = tk.Tk()
janela.title("Simulador de Digitação")

caixa_texto = tk.Text(janela, height=15, width=60)
caixa_texto.pack(padx=10, pady=10)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

botao_iniciar = tk.Button(frame_botoes, text="Iniciar Digitação", command=iniciar_digitação)
botao_iniciar.pack(side=tk.LEFT, padx=5)

botao_parar = tk.Button(frame_botoes, text="Parar Digitação", command=parar_digitação)
botao_parar.pack(side=tk.LEFT, padx=5)

botao_recarregar = tk.Button(frame_botoes, text="Recarregar arquivos JSON", command=carregar_jsons)
botao_recarregar.pack(side=tk.LEFT, padx=5)

# Thread do ESC
threading.Thread(target=monitorar_tecla_esc, daemon=True).start()

# Inicialização
carregar_jsons()
logging.info("Aplicação iniciada.")

janela.mainloop()
