from math import ceil


class SolarCalculationService:

    POWER_FACTOR = 0.8
    SAFETY_MARGIN = 1.25
    PANEL_SIZE = 200  # watts

    @classmethod
    def calculate(cls, calculation):
        appliances = calculation.appliances.all()

        total_watts = sum(
            a.quantity * a.watts for a in appliances
        )

        adjusted_load = total_watts * cls.SAFETY_MARGIN

        daily_energy = sum(
            a.quantity * a.watts * a.hours_per_day
            for a in appliances
        )

        inverter_kva = round(adjusted_load / (1000 * cls.POWER_FACTOR), 2)

        battery_ah = (
            adjusted_load * calculation.backup_hours
        ) / calculation.system_voltage

        panel_total_watts = daily_energy / calculation.sunlight_hours
        panel_qty = ceil(panel_total_watts / cls.PANEL_SIZE)

        return {
            "total_watts": total_watts,
            "adjusted_load": adjusted_load,
            "daily_energy": daily_energy,
            "inverter_kva": inverter_kva,
            "battery_ah": battery_ah,
            "panel_total_watts": panel_total_watts,
            "panel_qty": panel_qty,
        }
