import os, sys, io, time, math
import M5
from M5 import *
from hardware import Pin, I2C
from unit import ENVUnit

SAMPLING_INTERVAL = 2000
start_time = time.time()
last_sample_time = 0
current_page = 0
screen_on = True

max_t, max_h, max_p = -999.0, -999.0, -999.0
last_p = 0.0
trend_str = "="

env3_0 = None
labels = {}

def setup():
    global env3_0
    M5.begin()
    M5.Display.setRotation(0)
    M5.Display.setBrightness(200)
    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    env3_0 = ENVUnit(i2c=i2c0, type=3)
    init_ui()

def calculate_heat_index(t, h):
    if t < 20: return t
    return 0.5 * (t + 61.0 + ((t - 68.0) * 1.2) + (h * 0.094))

def calculate_dew_point(t, h):
    a, b = 17.27, 237.7
    gamma = ((a * t) / (b + t)) + math.log(h / 100.0)
    return (b * gamma) / (a - gamma)

def draw_degree_symbol(x, y, color=0xFFFFFF):
    M5.Display.drawCircle(x, y, 2, color)

def update_battery_bar():
    level = M5.Power.getBatteryLevel()
    color = 0x00FF00 if level > 30 else 0xFF0000
    M5.Display.fillRect(0, 0, 135, 4, 0x333333)
    M5.Display.fillRect(0, 0, int((level / 100) * 135), 4, color)

def init_ui():
    global labels
    M5.Display.fillScreen(0x000000)
    labels = {}

    if current_page == 0:
        # --- PAGINA 0: LIVE DATA ---
        # y=5: barra batteria (4px) + 1px gap
        labels['title'] = Widgets.Label(
            "LIVE DATA", 20, 6, 1.0,
            0x00BFFF, 0x000000, Widgets.FONTS.DejaVu12)

        # --- TEMPERATURA (y=22) ---
        Widgets.Label("TEMPERATURE", 5, 22, 1.0,
            0x777777, 0x000000, Widgets.FONTS.DejaVu12)
        labels['temp'] = Widgets.Label(
            "--.-", 5, 36, 1.0,
            0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu24)
        draw_degree_symbol(98, 38, 0xFFFFFF)
        Widgets.Label("C", 103, 36, 1.0,
            0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)

        M5.Display.drawLine(0, 66, 135, 66, 0x333333)

        # --- DEW POINT (y=70) ---
        Widgets.Label("DEW POINT", 5, 70, 1.0,
            0x777777, 0x000000, Widgets.FONTS.DejaVu12)
        labels['dew'] = Widgets.Label("--.-- C", 5, 84, 1.0,
            0x00BFFF, 0x000000, Widgets.FONTS.DejaVu12)

        # --- FEELS LIKE (y=102) ---
        Widgets.Label("FEELS LIKE", 5, 102, 1.0,
            0x777777, 0x000000, Widgets.FONTS.DejaVu12)
        labels['feels'] = Widgets.Label("--.-- C", 5, 116, 1.0,
            0x00FF00, 0x000000, Widgets.FONTS.DejaVu12)

        M5.Display.drawLine(0, 134, 135, 134, 0x333333)

        # --- HUMIDITY (y=138) ---
        Widgets.Label("HUMIDITY", 5, 138, 1.0,
            0x777777, 0x000000, Widgets.FONTS.DejaVu12)
        labels['hum'] = Widgets.Label("--%", 5, 152, 1.0,
            0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)

        M5.Display.drawLine(0, 178, 135, 178, 0x333333)

        # --- PRESSURE (y=182) ---
        Widgets.Label("PRESSURE", 5, 182, 1.0,
            0x777777, 0x000000, Widgets.FONTS.DejaVu12)
        labels['press'] = Widgets.Label("---- hPa", 5, 196, 1.0,
            0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu12)
        labels['trend'] = Widgets.Label("=", 110, 196, 1.0,
            0xFFFF00, 0x000000, Widgets.FONTS.DejaVu18)

        Widgets.Label("A:pg  B:rst", 5, 226, 1.0,
            0x444444, 0x000000, Widgets.FONTS.DejaVu12)

    elif current_page == 1:
        # --- PAGINA 1: RECORDS ---
        labels['title'] = Widgets.Label(
            "MAX RECORDS", 5, 6, 1.0,
            0xFFD700, 0x000000, Widgets.FONTS.DejaVu12)

        M5.Display.drawLine(0, 24, 135, 24, 0x333333)

        # --- MAX TEMP (y=28) ---
        Widgets.Label("MAX TEMP", 5, 28, 1.0,
            0x777777, 0x000000, Widgets.FONTS.DejaVu12)
        labels['max_t'] = Widgets.Label("--.-", 5, 44, 1.0,
            0x00FF00, 0x000000, Widgets.FONTS.DejaVu24)
        draw_degree_symbol(88, 48, 0x00FF00)
        Widgets.Label("C", 93, 44, 1.0,
            0x00FF00, 0x000000, Widgets.FONTS.DejaVu18)

        M5.Display.drawLine(0, 78, 135, 78, 0x333333)

        # --- MAX HUMIDITY (y=82) ---
        Widgets.Label("MAX HUMIDITY", 5, 82, 1.0,
            0x777777, 0x000000, Widgets.FONTS.DejaVu12)
        labels['max_h'] = Widgets.Label("--%", 5, 98, 1.0,
            0x00BFFF, 0x000000, Widgets.FONTS.DejaVu24)

        M5.Display.drawLine(0, 132, 135, 132, 0x333333)

        # --- MAX PRESSURE (y=136) ---
        Widgets.Label("MAX PRESSURE", 5, 136, 1.0,
            0x777777, 0x000000, Widgets.FONTS.DejaVu12)
        labels['max_p'] = Widgets.Label("---- hPa", 5, 152, 1.0,
            0xFFFF00, 0x000000, Widgets.FONTS.DejaVu18)

        Widgets.Label("A:pg  B:rst", 5, 226, 1.0,
            0x444444, 0x000000, Widgets.FONTS.DejaVu12)

    elif current_page == 2:
        # --- PAGINA 2: SYSTEM ---
        labels['title'] = Widgets.Label(
            "SYSTEM INFO", 5, 6, 1.0,
            0x00BFFF, 0x000000, Widgets.FONTS.DejaVu12)

        M5.Display.drawLine(0, 24, 135, 24, 0x333333)

        # --- BATTERY (y=28) ---
        Widgets.Label("BATTERY", 5, 28, 1.0,
            0x777777, 0x000000, Widgets.FONTS.DejaVu12)
        labels['bat_pct'] = Widgets.Label("--%", 5, 44, 1.0,
            0x00FF00, 0x000000, Widgets.FONTS.DejaVu24)

        M5.Display.drawLine(0, 84, 135, 84, 0x333333)

        # --- UPTIME (y=88) ---
        Widgets.Label("UPTIME", 5, 88, 1.0,
            0x777777, 0x000000, Widgets.FONTS.DejaVu12)
        labels['uptime'] = Widgets.Label("00:00:00", 5, 104, 1.0,
            0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)

        M5.Display.drawLine(0, 134, 135, 134, 0x333333)

        # --- INTERVAL (y=138) ---
        Widgets.Label("INTERVAL", 5, 138, 1.0,
            0x777777, 0x000000, Widgets.FONTS.DejaVu12)
        Widgets.Label("{} ms".format(SAMPLING_INTERVAL), 5, 154, 1.0,
            0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu12)

        Widgets.Label("A:pg  B:rst", 5, 226, 1.0,
            0x444444, 0x000000, Widgets.FONTS.DejaVu12)

    update_battery_bar()

def loop():
    global last_sample_time, current_page, max_t, max_h, max_p
    global screen_on, last_p, trend_str

    M5.update()

    if M5.BtnA.wasHold():
        if screen_on:
            screen_on = False
            M5.Display.setBrightness(0)
        else:
            screen_on = True
            M5.Display.setBrightness(200)
            init_ui()
    elif M5.BtnA.wasClicked():
        if screen_on:
            current_page = (current_page + 1) % 3
            init_ui()

    if M5.BtnB.wasHold():
        max_t, max_h, max_p = -999.0, -999.0, -999.0
        M5.Speaker.tone(2000, 100)
        if screen_on:
            init_ui()

    now_ms = time.ticks_ms()
    if time.ticks_diff(now_ms, last_sample_time) > SAMPLING_INTERVAL:
        last_sample_time = now_ms
        try:
            t = env3_0.read_temperature()
            h = env3_0.read_humidity()
            p_raw = env3_0.read_pressure()
            p = p_raw / 100 if p_raw > 5000 else p_raw

            feels = calculate_heat_index(t, h)
            dew   = calculate_dew_point(t, h)

            up_sec = int(time.time() - start_time)
            uptime_str = "{:02}:{:02}:{:02}".format(
                up_sec // 3600, (up_sec % 3600) // 60, up_sec % 60)

            if last_p > 0:
                trend_str = ("^" if p > last_p + 0.05
                             else "v" if p < last_p - 0.05
                             else "=")
            last_p = p

            if t > max_t: max_t = t
            if h > max_h: max_h = h
            if p > max_p: max_p = p

            if screen_on:
                update_battery_bar()
                if current_page == 0:
                    labels['temp'].setText("{:.1f}".format(t))
                    labels['dew'].setText("{:.1f} C".format(dew))
                    labels['feels'].setText("{:.1f} C".format(feels))
                    labels['hum'].setText("{:.0f}%".format(h))
                    labels['press'].setText("{:.0f} hPa".format(p))
                    labels['trend'].setText(trend_str)
                elif current_page == 1:
                    labels['max_t'].setText("{:.1f}".format(max_t))
                    labels['max_h'].setText("{:.0f}%".format(max_h))
                    labels['max_p'].setText("{:.0f} hPa".format(max_p))
                elif current_page == 2:
                    labels['bat_pct'].setText(
                        "{}%".format(M5.Power.getBatteryLevel()))
                    labels['uptime'].setText(uptime_str)
        except:
            pass

if __name__ == '__main__':
    setup()
    while True:
        loop()