from datetime import datetime, timedelta


DIAS = {
    "L": 0,  # lunes
    "M": 1,  # martes
    "X": 2,  # miércoles
    "J": 3,  # jueves
    "V": 4,  # viernes
    "S": 5,  # sábado
    "D": 6,  # domingo
}


def semana_del_mes(fecha):
    """
    Semana del mes en bloques de siete días: 1-7, 8-14, etc.
    Devuelve 1,2,3,4,5...
    """
    return ((fecha.day - 1) // 7) + 1


def dentro_ventana(fecha_hora, ventana):
    partes = ventana.strip("#").split("#")

    rango_horas = partes[0]
    dias = partes[1].split(",")
    semanas = [int(s[1:]) for s in partes[2].split(",")]

    hora_inicio, hora_fin = map(int, rango_horas.split("-"))

    # Ventana normal (ej: 01-07)
    if hora_inicio <= hora_fin:
        semana = semana_del_mes(fecha_hora)

        if semana not in semanas:
            return False

        if fecha_hora.weekday() not in [DIAS[d] for d in dias]:
            return False

        return hora_inicio <= fecha_hora.hour < hora_fin

    # Ventana que cruza medianoche (ej: 07-03)
    else:
        dias_permitidos = [DIAS[d] for d in dias]

        # mismo día desde hora_inicio hasta 23:59
        semana_actual = semana_del_mes(fecha_hora)

        if (
            fecha_hora.weekday() in dias_permitidos
            and semana_actual in semanas
            and fecha_hora.hour >= hora_inicio
        ):
            return True

        # día siguiente hasta hora_fin
        dia_anterior = fecha_hora - timedelta(days=1)
        semana_anterior = semana_del_mes(dia_anterior)

        if (
            dia_anterior.weekday() in dias_permitidos
            and semana_anterior in semanas
            and fecha_hora.hour < hora_fin
        ):
            return True

        return False