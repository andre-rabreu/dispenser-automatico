# ======== Imports e hardware =========
import uasyncio as asyncio
from machine import Pin, I2C, UART
import time, uheapq

# --- DS1307 ----------
from urtc import DS1307
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
rtc = DS1307(i2c)

# --- LED -----
led = Pin(6, Pin.OUT)

# --- Motor ----------
motor_pins = [
    machine.Pin(15, machine.Pin.OUT), # IN 1
    machine.Pin(14, machine.Pin.OUT), # IN 2
    machine.Pin(16, machine.Pin.OUT), # IN 3
    machine.Pin(17, machine.Pin.OUT) # IN 4
    ]
full_step_sequence = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
    ]

# --- Bluetooth UART (HC-05) ----
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
bt_state_pin = Pin(2, Pin.IN)

# ======== Tarefas auxiliares =========
async def blink_led(period_ms=400):
    try:
        while True:
            led.toggle()
            await asyncio.sleep_ms(period_ms)
    except asyncio.CancelledError:
        led.off()
        raise

async def run_motor_cw(fullsteps):
    global led_task
    
    led_task = asyncio.create_task(blink_led())
    
    for s in range(fullsteps * 512):
        for step in full_step_sequence:
            for i in range(len(motor_pins)):
                motor_pins[i].value(step[i])
            await asyncio.sleep(0.002)
            
    if led_task:
        led_task.cancel()
        try:
            await led_task
        except asyncio.CancelledError:
            pass
        led.high()
        led_task = None
            
# ======== Scheduler baseado em RTC =========
schedules = set()           # { (hour, minute) }
_last_run = {}              # { (h,m): yyyymmdd }  para evitar rodar 2× no mesmo dia

async def rtc_scheduler():
    """Verifica o DS1307 uma vez por segundo e dispara o motor nos horários agendados."""
    while True:
        (year, month, date, day, hour, minute, second, p1) = rtc.datetime()
        today = year * 10_000 + month * 100 + day

        key = (hour, minute)
        if key in schedules and _last_run.get(key) != today:
            print(f"⏰ {hour:02d}:{minute:02d} ⇒ motor")
            asyncio.create_task(run_motor_cw(1/2))
            _last_run[key] = today

        await asyncio.sleep(1)

# ======== UART helpers =========
async def readline_async(uart, eol=b'\n'):
    buf = bytearray()
    while True:
        if uart.any():
            ch = uart.read(1)
            if ch in (b'\n', b'\r'):
                if buf:
                    return buf.decode().strip()
            else:
                buf.extend(ch)
        else:
            await asyncio.sleep_ms(20)

MENU = (
    "\n=== MENU ===\n"
    "1) Rodar motor agora\n"
    "2) Agendar horário fixo diário (hh:mm)\n"
    "3) Listar horários\n"
    "4) Apagar horário\n"
    "0) Sair do menu\n"
)

# ======== Sessão de menu =========
connected = False

async def menu_session():
    uart.write(MENU)
    while connected:
        try:
            opt = await readline_async(uart)
        except asyncio.CancelledError:
            return

        if opt == "1":
            uart.write("Rodando motor...\n")
            await run_motor_cw(1/2)
            uart.write("Feito!\n")

        elif opt == "2":
            uart.write("Formato hh:mm ? ")
            try:
                t = await readline_async(uart)
                hh, mm = map(int, t.split(":"))
                assert 0 <= hh < 24 and 0 <= mm < 60
                schedules.add((hh, mm))
                uart.write(f"Agendado {hh:02d}:{mm:02d} diariamente.\n")
            except Exception:
                uart.write("Hora inválida.\n")

        elif opt == "3":
            if not schedules:
                uart.write("Nenhum horário agendado.\n")
            else:
                for h, m in sorted(schedules):
                    uart.write(f"- {h:02d}:{m:02d}\n")

        elif opt == "4":
            uart.write("Qual hora remover (hh:mm)? ")
            t = await readline_async(uart)
            try:
                hh, mm = map(int, t.split(":"))
                schedules.discard((hh, mm))
                uart.write("Removido (se existia).\n")
            except:
                uart.write("Formato inválido.\n")

        elif opt == "0":
            uart.write("Fechando menu.\n")
            break

        else:
            uart.write("Opção desconhecida.\n")

        uart.write(MENU)

# ======== Monitor HC-05 =========
async def bluetooth_monitor():
    global connected

    while True:
        state = bt_state_pin.value()
        if state and not connected:
            connected = True
            print("Bluetooth conectado")
        elif not state and connected:
            connected = False
            print("Bluetooth desconectado")
        await asyncio.sleep_ms(200)

# ======== Loop principal =========
async def main():
    asyncio.create_task(bluetooth_monitor())
    asyncio.create_task(rtc_scheduler()) # scheduler sempre ativo

    menu_task = None
    while True:
        if connected and menu_task is None:
            menu_task = asyncio.create_task(menu_session())

        if not connected and menu_task is not None:
            menu_task.cancel()
            menu_task = None

        await asyncio.sleep_ms(100)

# ======== Inicia o programa =======
if __name__ == "__main__":
    led.high()
    asyncio.run(main())